---
title: "From Bitstream to Idea: An Inverse Guide to FPGAs"
date: 2026-07-08
tags: [fpga, ice40, ghdl, yosys, nextpnr, icestick, toolchain, hardware, digital-design]
description: "The ghdl-yosys-nextpnr toolchain for an iCE40, walked backward: starting from a blinking LED and tracing every transformation back to the idea that caused it."
keywords: "FPGA toolchain, ghdl, yosys, nextpnr, icepack, iceprog, iCE40, iCEstick, netlist, bitstream, place and route, technology mapping"
---

Most FPGA tutorials, including [my own](/posts/fpga-blinky-vhdl-icestick-may-2026/), go forward: idea, block diagram, VHDL, simulate, synthesize, place and route, flash, done. That order makes sense for building something. It makes less sense for understanding the toolchain, because forward explanations tend to gloss over exactly the step you are standing on. You are told "now run synthesis" and you run it, and the tool produces a file, and you move to the next command.

This post goes the other direction. I want to start at the thing you can actually observe, an LED blinking on a [Lattice iCEstick](https://www.latticesemi.com/icestick), and walk backward through every transformation until we arrive at the idea that caused it. Every program in this chain is a transformer: it takes a dataset and a configuration, and it produces a different dataset. Nothing in the chain does anything else. Once you see it that way, the toolchain stops being a sequence of magic incantations and becomes a pipeline of well-defined functions.

If you have not read [WTF are FPGAs](/posts/wtf-are-fpgas-june-2026/), that post covers the architecture: logic cells, routing fabric, why FPGAs exist at all. This one assumes you know roughly what an FPGA is and cares only about what happens between your idea and the moment it becomes silicon behavior.

---

## The Chain, Backward

```
Running gateware on the iCEstick
  ^ iCE40 self-boot (chip reads flash as SPI master on power-up)
Bitstream sitting in external SPI flash
  ^ iceprog
Bitstream (.bin)
  ^ icepack
Placed & routed design (.asc)
  ^ nextpnr-ice40
Technology-mapped netlist (JSON)
  ^ yosys (synth_ice40)
Generic netlist (GHDL internal)
  ^ ghdl -e (elaborate)
Analyzed design units in a library
  ^ ghdl -a (analyze)
VHDL code
  ^ a human, not a program
Block diagram
  ^ a human, not a program
Flip-flops, logic gates, wires: the idea
```

Two of those arrows are not tool invocations. That is not an oversight, it is the point: every arrow in this chain is a transformer with a configuration, except the two closest to the idea. I will come back to that.

---

## 1. The Running Gateware, and What "Flashing" Actually Means

The LED is blinking because the iCE40 is currently holding a specific pattern in its configuration SRAM: which routing multiplexers are closed, what each LUT's truth table is, what each flip-flop's reset behavior is. That pattern is volatile. Remove power and it is gone.

This is the detail that trips people up: "flashing an FPGA" does not mean writing directly into the chip's active configuration memory, at least not permanently. On the iCEstick, `iceprog` writes the bitstream into an external SPI flash chip on the board, using the second channel of the onboard FTDI dual-UART/SPI chip as a SPI master. While it does this, it holds the iCE40 in reset, so the two devices are not fighting over the same SPI bus.

On every power-up, the iCE40 does something you do not initiate: it pulls its `CDONE` pin low, becomes a SPI master itself, reads the bitstream out of that same external flash, and writes it byte by byte into its own configuration cells. Once that finishes, `CDONE` goes high and your design starts running. "Flashing" means feeding the source the chip will read from at its next boot, not writing to the chip directly.

**Transformer:** `iceprog`
**Input:** bitstream (`.bin`), flash configuration (SPI mode, flash offset)
**Output:** gateware on the board's external flash, loaded into the FPGA on the next boot
**Implicit requirement:** exclusive access to the FTDI channel; under Linux, udev rules that let a non-root user talk to the chip at all (see the permissions section in the [Zero to One VHDL post](/posts/fpga-blinky-vhdl-icestick-may-2026/) if you have not set that up yet).

---

## 2. The Bitstream, and Why icepack Cannot Fail on Resource Shortage

Before `iceprog` had anything to write, something had to produce the `.bin` file. That is `icepack`, and it does exactly one thing: it takes the human-readable `.asc` file that nextpnr produced and serializes it into the binary format the iCE40's configuration loader expects.

`icepack` makes no design decisions. The `.asc` file already contains, for every tile in the chip, whether that tile is used and exactly what its configuration bits should be: logic cell truth tables, DFF reset-type bits, routing mux selections. `icepack`'s job is to know, for a given iCE40 device (a `1k`, an `8k`, whichever), the exact bit position in the linear output stream that corresponds to each tile's configuration cell, a mapping that the IceStorm project reverse-engineered because Lattice never published it. It writes those bits at the right positions, pads unused regions with the device's required defaults, and appends the sync words and CRC that the chip's own bootloader expects to see.

This is why "not enough logic cells" can never be an `icepack` error. By the time `icepack` runs, every cell already has a confirmed physical home. If the design did not fit, the failure happened one step earlier.

**Transformer:** `icepack`
**Input:** placed and routed design (`.asc`, text)
**Output:** bitstream (`.bin`, binary)
**Note:** pure format conversion, no capacity checking, no optimization.

---

## 3. Placed and Routed Design: Where nextpnr Decides Location, Not Identity

Here is the step people most often describe imprecisely, myself included until I actually traced through it: **nextpnr does not decide what a piece of logic becomes. It decides where a piece of logic goes.**

By the time nextpnr runs, every cell in the design is already a concrete iCE40 primitive: `SB_LUT4`, some flavor of `SB_DFF`, `SB_CARRY`, `SB_IO`. That decision was made one step earlier, in yosys. nextpnr's job is placement and routing:

- **Placement**: assign each of those already-typed cells to one specific physical slot in the chip's grid. This runs as a simulated-annealing-style search: an initial (often rough) placement, then repeated swaps of cell positions, scored by a cost function built mostly from estimated wire length between connected cells plus a timing model for critical paths. Worse swaps are accepted early on and rejected more strictly as the search converges, which is what keeps it from getting stuck in a bad local placement.
- **Routing**: for every net, find an actual path through the chip's programmable interconnect (the "highways" from the WTF are FPGAs post) that connects the source to every sink. nextpnr uses a PathFinder-style negotiated-congestion router: paths are found somewhat independently first, then when two nets want the same wire segment, that segment's cost goes up and the losing net gets rerouted in a later iteration, until nothing conflicts.

Two inputs feed this that are easy to forget about because they are not files you generate, they are files you write by hand:

- **The PCF (Pin Constraint File)**: maps your top-level VHDL port names to physical chip pins, taken from the board's schematic. Without it, nextpnr has no way to know that your `led` signal has to land on the specific pin wired to an actual LED.
- **The chip database**: an embedded description of every physical resource in the specific iCE40 part (which LUTs, DFFs, BRAM, IO cells exist and where), which is why you tell nextpnr `--hx1k --package tq144` and not just "iCE40."

If the design genuinely does not fit, this is where it fails, with an error like "failed to place cell" or "out of bels of type ICESTORM_LC." Nothing downstream of this step can produce that failure, because nothing downstream is checking capacity anymore.

**Transformer:** `nextpnr-ice40`
**Input:** technology-mapped netlist (JSON), PCF, chip architecture database
**Output:** placed and routed design (`.asc`)
**Implicit requirement:** the JSON must already consist entirely of iCE40 primitives; nextpnr does not perform technology mapping.

---

## 4. Technology-Mapped Netlist: Where yosys Decides What Everything Becomes

This is the step where "identity" gets fixed. `synth_ice40`, the yosys script for this target, does both generic logic synthesis and technology mapping in one pass, and the order matters for understanding what "netlist" even means at each stage.

yosys reads the design (via the ghdl-yosys-plugin, more on that below) into its own internal representation, RTLIL. VHDL `process` blocks are not yet a netlist at this point, they are still procedural: `if`/`case` structures, sequential signal assignments. The `proc` pass converts that procedural description into an actual netlist: `if`/`case` becomes `$mux` cells, clocked assignments become `$dff` cells with a mux feeding their input. This is the step where "prozedurales Denken," procedural thinking, becomes pure combinational logic plus registers.

From there: generic optimization (constant folding, dead logic removal), then `techmap` breaks complex generic cells down to primitive gates, then `abc` (a separate logic synthesis tool yosys shells out to) does the actual LUT-mapping heuristic, mapping the boolean network onto 4-input LUTs because that is what an iCE40 logic cell is. A second `techmap` pass with the iCE40-specific cell library turns those generic LUT/DFF results into `SB_LUT4`, the correct `SB_DFF` variant, `SB_CARRY` for arithmetic carry chains. `iopadmap` inserts `SB_IO` cells at every top-level port, because the chip needs explicit IO buffer cells that are not implicit in a generic design.

After this point, the set of cell types in the design is frozen. nextpnr cannot introduce a new primitive type, cannot decide a signal should have been an `SB_CARRY` instead of plain LUT logic. All of that identity work happened here.

**Transformer:** `yosys` (`synth_ice40`)
**Input:** generic netlist (from GHDL, via the ghdl-yosys-plugin), iCE40 cell library
**Output:** technology-mapped netlist, written out as JSON via `write_json`
**Note:** synthesis and technology mapping are one pass here, not two separable stages.

---

## 5. The Generic Netlist: What Elaboration Actually Produces

Here is where I had to correct my own mental model mid-conversation while working this out. I originally thought of `ghdl -e` (elaborate) as "the compiler." That is not quite right, and the imprecision matters.

`ghdl -a` (analyze) compiles VHDL design units, entities, architectures, packages, independently of each other, and stores them in a library (`work-obj93.cf` or `work-obj08.cf` depending on the VHDL standard, plus associated object data). This is exactly Ada's separate-compilation model, which VHDL inherited. At this stage GHDL knows a unit type-checks and knows its public interface (ports, generics, package declarations), and it knows what other units it depends on. It does not know anything about hierarchy. Component instantiations are checked for type correctness, not resolved to a specific concrete architecture. It has no idea which unit, if any, is the top level.

`ghdl -e` picks a concrete top-level entity, binds any generic values (defaults or overrides via `-g<name>=<value>`), and recursively resolves every component instantiation to a specific entity/architecture pair, unrolling `generate` statements as it goes. What comes out the other side is a fully concrete, fully instantiated design. For simulation, GHDL turns this into an actual runnable executable. For the synthesis path specifically, GHDL additionally translates each process and concurrent signal assignment into its own internal netlist representation, gates, muxes, flip-flops, before yosys ever gets involved. That internal format is not a file. The ghdl-yosys-plugin hands it to yosys directly, in-process, which is why there is no intermediate `.v` or `.json` between GHDL and yosys when you invoke `ghdl_synth` from within a yosys script.

Why split analyze and elaborate at all, rather than doing it in one pass? Because the library that `-a` produces is reusable. If none of the already-analyzed units change, you can swap the top-level entirely, point `-e` at a different testbench architecture, say, and only re-elaborate. You never re-analyze code that has not changed. And if you change one unit, only that unit needs re-analysis; GHDL tracks this through dependency and timestamp information in the library's index file. This is the same reasoning behind incremental compilation in any language with a module system: analyze once, elaborate many times, as long as the pieces did not move.

Put in software terms, `-a` is closer to a compiler and `-e` is closer to a linker. `ghdl -a` turns each source file into an independent, type-checked unit, the VHDL equivalent of an object file, without knowing or caring what the final program looks like. `ghdl -e` is the step that takes a fixed set of those already-compiled units, resolves references between them, picks one entry point, and produces one concrete, complete artifact. You would not expect a linker to re-parse C source, and you would not expect `ghdl -e` to re-check VHDL syntax; it just wires together what `-a` already validated.

**Transformer:** `ghdl -e`
**Input:** analyzed design units from the library, chosen top-level, generic values
**Output:** generic, technology-neutral netlist (internal to GHDL, in the synthesis path)
**Implicit requirement:** every unit the top-level references transitively must already be analyzed and present in the library.

---

## 6. Analyzed Design Units: What analyze Actually Checks

`ghdl -a` produces, per design unit, an entry in the library's index and an object representation of that unit's internal typed tree. It does two things and exactly two things: type-checking (does this unit's code make sense on its own, given what it declares and what it imports via `use`), and interface recording (what ports, generics, and declarations does this unit expose, so that later units, or a later elaboration, can reference it correctly).

What it explicitly does not do: resolve hierarchy, know about a top-level, or produce any kind of gate-level structure. A `process` block at this stage is still exactly the VHDL you wrote, not yet touched by anything resembling synthesis.

One practical consequence, and this is the kind of thing that only becomes obvious once you try to break it: if you analyze files out of dependency order, a package's body before something that imports it, GHDL rejects the later file with "unit ... not found," because the referenced unit is not in the library index yet. GHDL will not reorder your build for you.

**Transformer:** `ghdl -a`
**Input:** VHDL source for one or more design units
**Output:** typed, checked units recorded in the library
**Implicit requirement:** dependency order; a package must be analyzed before anything that uses it.

---

## 7. VHDL Code: The First Non-Program Step

Every step above this line is a program with a configuration. This one is not. Going from a block diagram to VHDL is a design act performed by a person, and it is worth pausing on because it is structurally different from everything else in the chain: there is no transformer here, no dataset-plus-config producing another dataset. There is a person translating an idea into a formal language, and that translation is where actual engineering judgment lives.

It also carries an implicit requirement none of the automated steps enforce until much later: not every construct that simulates is synthesizable. `wait for 10 ns` runs fine in a testbench and means nothing to `synth_ice40`. That boundary, what is synthesizable VHDL versus what is merely simulatable VHDL, is not checked at the point you write the code. It surfaces later, at analyze or synthesis time, as an error or a silent misunderstanding of what hardware you actually described.

---

## 8. The Block Diagram, and the Idea Underneath It

Below VHDL is the block diagram: flip-flops, logic gates, wires, arranged conceptually before a single line of code exists. Like the step above it, this is not automated, and "configuration" here means something different: it means domain knowledge. Understanding what needs a clock edge and what is purely combinational. Understanding metastability well enough to know when a signal is crossing clock domains and needs synchronization. Deciding, before any tool is involved, that a given function actually belongs in hardware at all rather than in software running on a microcontroller sitting next to the FPGA.

This is the actual root of the whole chain. None of the seven transformers above it can correct a bad decision made here. They can only execute, with complete fidelity, whatever was decided at this step.

---

## Why Go Backward

Going forward, you start with intent and watch it get realized. Going backward, you start with the physical fact, an LED blinking on a piece of hardware you can hold, and you ask what had to be true one step earlier for that fact to exist. I found that more honest about where the actual decisions get made. Six of the eight steps in this chain are mechanical: given the same input and configuration, `icepack` or `nextpnr` will always produce the same output. The two steps that are not mechanical, block diagram to VHDL and idea to block diagram, are the only places where the design could have gone differently. Everything downstream of those two steps is just careful, deterministic execution.

If you want to see this chain from the other direction, with actual VHDL, a testbench, and a real LED blinking at the end, that is [Zero to One: VHDL and a Lattice iCEstick](/posts/fpga-blinky-vhdl-icestick-may-2026/). And if you want the architectural picture this post assumes, what a LUT is, why the routing fabric matters, why FPGAs exist at all, that is [WTF are FPGAs](/posts/wtf-are-fpgas-june-2026/).
