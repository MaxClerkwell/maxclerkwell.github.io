---
title: "Deploying Hardware Like Software: A Bitstream Pipeline for the Zynq"
date: 2026-08-23
tags: [fpga, zynq, linux, u-boot, yosys, nextpnr, open-source, embedded, rest-api, alinx]
description: "Alinx sent me an AX7020 board. Here is the plan: an open-source path from JTAG bring-up to a REST API that accepts a bitstream and loads it onto the FPGA, no vendor tools in the loop."
keywords: "Zynq 7020, AX7020, Alinx, U-Boot SPL, JTAG, TFTP, yosys, nextpnr-xilinx, openXC7, FPGA manager, bitstream, REST API, FPGA deployment"
---

A while ago, [Alinx](https://www.alinx.com/) reached out and asked whether I would like one of their boards for my content work. I said yes, and a few days later an AX7020 arrived on my desk. Full disclosure up front: the board is a sponsorship gift. Alinx has no say in what I write about it, and as you will see below, my plan involves ignoring most of the vendor-recommended workflow anyway.

This article is not a tutorial. It is the concept post for a small series: what I want to build, why I want to build it that way, and where I expect things to get uncomfortable. The follow-up articles will document each stage as it actually happens, including the parts that fail.

---

## The Board

The AX7020 is built around a Xilinx Zynq-7020, which is a curious kind of chip. Half of it is an ordinary computer: two ARM Cortex-A9 cores, a DDR3 controller, Gigabit Ethernet, USB, SD, UART. Xilinx calls this half the PS, the Processing System. The other half is FPGA fabric, the PL or Programmable Logic, sitting on the same die and wired to the processor through a set of AXI ports.

If you have read my [introduction to FPGAs](/posts/wtf-are-fpgas-june-2026/), you know that I think of an FPGA as a grid of configurable logic with a routing fabric between the cells. The Zynq takes that grid and bolts a Linux-capable computer onto it. That combination is the whole point of this project. The ARM side runs a normal operating system with a network stack, and the FPGA side is available as a resource that the operating system can reconfigure at runtime, in well under a second, as often as it likes.

Read that again, because it is the core idea: the processor can rewrite the hardware next to it while running. Most people program FPGAs the way we programmed microcontrollers in the nineties, with a cable and a vendor tool and a ritual. The Zynq allows something much closer to modern software deployment. Nobody walks to a server with a JTAG probe to update a web service. You push an artifact to an endpoint and the system takes it from there.

So that is the goal I am committing to in writing:

**A REST API running on the board itself. You POST a bitstream to it, and the FPGA next to the processor starts executing your design.**

If that sounds familiar, it is because AWS sells exactly this. Their F1 and F2 instances are servers with datacenter-grade FPGAs attached: you upload your design through an API, AWS loads it into the fabric, and your software talks to your custom hardware over PCIe. What I am building is the same idea shrunk from a datacenter rack to a 15-watt board on my desk, with one difference that matters to me: on AWS, every layer between your design and the silicon is proprietary and invisible. Here, every layer will be open and inspectable.

Deploying hardware like software. `curl -T design.bin` as the last step of a hardware CI pipeline.

---

## The Plan, Stage by Stage

Between an unboxed board and that API sit five stages. Each one is a natural checkpoint, and each one will get its own article.

### Stage 1: An open-source U-Boot, loaded over JTAG

The Zynq-7000 boot ROM knows four boot sources: JTAG, QSPI flash, NAND, and SD card. What it does not know is USB, so there is no magic first contact over a USB cable like on more modern chips. The first code on this board will therefore arrive over JTAG.

The usual path here is the Xilinx FSBL, the First Stage Boot Loader that Vivado generates for you. I am not taking that path. Mainline U-Boot has an SPL mode that replaces the FSBL entirely: a small first stage that initializes the DDR controller, the clocks, and the pin multiplexing, then loads the full U-Boot. The board-specific knowledge, which DDR chips are soldered down and which pins go where, lives in a generated file called `ps7_init_gpl.c` that can be extracted from the vendor's hardware description without ever starting Vivado. Alinx publishes their reference design [on GitHub](https://github.com/alinxalinx/AX7020_2023.1), and the file is sitting inside the XSA archive, which turns out to be a plain zip.

Mainline U-Boot has never heard of the AX7020, so this stage involves teaching it about a board it does not know: adapting a device tree from a close relative like the ZedBoard and feeding the SPL the correct initialization data for this specific board. How that goes in practice, including whatever friction the vendor tutorials do not mention, will be the subject of its own article.

Checkpoint for this stage: a U-Boot prompt on the serial console, `bdinfo` reporting 1 GB of DDR, and the QSPI flash answering to `sf probe`. Once that works, U-Boot gets written to the QSPI flash and the JTAG cable goes back in the drawer. Everything after this point happens over the network.

### Stage 2: An image server on my own network

U-Boot can fetch files over TFTP, and the Ethernet port of the AX7020 hangs directly off the processor side, so it works without any FPGA configuration at all. The plan is classic network boot, the same pattern that diskless workstations used thirty years ago: the board comes up, U-Boot asks the network for a kernel and a root filesystem, and boots what it receives.

That requires infrastructure on my side, a small image server: TFTP for U-Boot, plus something to serve rootfs images. This is deliberately part of the project rather than an annoyance. If the endgame is treating hardware deployment like software deployment, then the boot images themselves should also come from a server I can push to, not from an SD card I have to carry around. The UART stays connected during all of this as the rescue line; serial consoles are to embedded bring-up what stack traces are to software.

### Stage 3: A Linux built for this board

With netboot working, the board needs a proper operating system. PetaLinux, the vendor's offering, is a wrapper around Yocto, so I will skip the wrapper and use Yocto directly with the meta-xilinx layer, mainline kernel, mainline U-Boot. The Zynq-7000 is mature enough to be genuinely well supported upstream; the Ethernet controller, the SD controller, and, crucially for this project, the FPGA configuration interface all have mainline drivers.

The one feature this Linux absolutely must have is the kernel's FPGA manager framework. On the Zynq, the processor configures the FPGA fabric through an internal port called PCAP, and the mainline `zynq-fpga` driver exposes it in sysfs. Loading a new hardware design then degenerates into writing a filename into a sysfs node. No cable, no vendor tool, just a file write that any process with the right permissions can perform.

### Stage 4: A bitstream from the open toolchain, loaded over SSH

Now the FPGA side. The Zynq-7020 is a 7-series device, which means it is covered by the openXC7 flow: Yosys for synthesis, nextpnr-xilinx for place and route, on top of the Project X-Ray database that documents the bitstream format. I wrote about [reverse-engineering bitstreams](/posts/from-bitstream-to-idea-inverse-fpga-guide-july-2026/) before; this project is where that world becomes daily practice, because the entire pipeline from HDL to configured silicon will run without a single proprietary tool.

I want to be honest about expectations here. The open 7-series flow works, but it is not Vivado. Timing analysis is rudimentary and some hard blocks are awkward to use. For this stage the design will be deliberately boring, a blinker or a counter on AXI, because the design is not the point. The point is the pipeline: synthesize on my desk, `scp` the bitstream to the board, log in over SSH, write it into the FPGA manager, watch the LED blink. The moment that works, the full loop exists, and every piece of it is open source.

### Stage 5: The REST API

The final stage removes the human from stage 4. A small service on the board, probably a few hundred lines, accepts a bitstream over HTTP, validates it, hands it to the FPGA manager, and reports back whether the fabric came up.

Validation is the part I refuse to hand-wave. A bitstream is arbitrary hardware configuration. The service will at minimum check the sync word and the device IDCODE so that only bitstreams built for this exact chip get loaded, and the endpoint will be authenticated. There is also a sharper issue lurking here: a design containing an AXI master has full access to system memory, DMA-style. An API that loads unreviewed bitstreams is remote code execution with extra steps, hardware edition. For my lab that is an acceptable and clearly labeled risk. For anything beyond a lab it is the reason AWS wraps every customer design on their FPGA instances in a fixed shell that polices its memory access. Knowing that this problem exists, and understanding why the cloud providers solved it the way they did, is half the educational value of building the small version.

---

## Why Bother, When an SD Card Would Do

A fair question. Alinx ships a working reference image; I could have the board on the network in an afternoon by flashing a card and following the manual.

But my interest in this board is not the destination, it is the supply chain. Every stage of this plan replaces a vendor black box with an inspectable component: SPL instead of FSBL, Yocto instead of PetaLinux, Yosys and nextpnr instead of Vivado, sysfs instead of a programming cable. At the end, every byte that reaches this chip, from the first DDR register write to the configuration frames in the FPGA fabric, will have come out of a toolchain I can read the source of.

That is worth something on its own. It is worth more as content, because the failures along the way are precisely the material that vendor documentation cannot provide.

The board is on my desk, the serial adapter is plugged in, and stage 1 is already further along than this article admits. Next post: building mainline U-Boot for a board that mainline has never heard of.

---

## Work With Me

Projects like this one are what I do professionally. I work as a freelancer on embedded systems: microcontroller firmware, PCB design, FPGA development, board bring-up, and the toolchains and infrastructure around them. If you have a project in that space, from "we need a prototype" to "our vendor toolchain is holding us hostage", [get in touch](mailto:stephan@boekelmann.net).

And if you just want to talk shop: I am regularly around on my Full Stack Engineering Discord, where we discuss everything from tape-out to JavaScript. Come say hi.

<div><a href="https://discord.gg/2BXuUY6hrX" class="link-card-discord" target="_blank" rel="noopener noreferrer"><i class="fab fa-discord"></i><div class="discord-text"><span class="discord-name">Discord — Full Stack Engineering</span><span class="discord-note">Direct access to me and my colleagues. Webinars, live Q&amp;A, and community discussions for engineers across the full stack.</span><span class="discord-join">Join the server →</span></div></a></div>
