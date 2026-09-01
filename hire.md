---
layout: default
title: "Hire Me — Freelance FPGA, Zynq, PCB & DAQ Engineering | Stephan Bökelmann"
description: "Freelance embedded engineering from Bochum, Germany: FPGA and Zynq development, PCB design and bring-up in KiCad, embedded Linux (Yocto, U-Boot), and data-acquisition systems. Feasibility study to serial product, on-site in DACH or remote."
permalink: /hire/
last_modified_at: 2026-08-31
---

<div class="post-layout">
<article class="post-content" markdown="1">

# Freelance FPGA, Zynq, PCB & DAQ Engineering

I take on **freelance engineering projects** through my company
[nabla B](https://nabla-b.engineering/) in Bochum, Germany — on-site in the
DACH region, remote worldwide, in English or German. From feasibility study
to serial product, from "we need a prototype" to "our vendor toolchain is
holding us hostage".

**Start a project:** [office@nabla-b.engineering](mailto:office@nabla-b.engineering?subject=Project%20inquiry%20via%20maxclerkwell.tech)
· [LinkedIn](https://www.linkedin.com/in/accelerator-stephan/)
· Direct: [stephan@boekelmann.net](mailto:stephan@boekelmann.net)

## What I do

**FPGA & Zynq development.** HDL design in VHDL/Verilog, Zynq-7000 PS/PL
systems and AXI integration, board bring-up without vendor lock-in
(mainline U-Boot SPL instead of FSBL, JTAG/OpenOCD), open toolchains
(Yosys, nextpnr) as well as Vivado/Vitis where they are the right tool. The
[open Zynq bitstream pipeline](/posts/zynq-bitstream-deployment-concept-august-2026/)
on this blog shows the working style in public.

**PCB design & bring-up.** Schematic and layout in KiCad, multilayer,
signal integrity, EMC preparation and certification support, hand-off to
manufacturing — including supply-chain work with board and cable
manufacturers in China and Europe, and wire bonding for bare-die
prototypes.

**Embedded firmware & Linux.** Microcontroller firmware (bare-metal and
RTOS), embedded Linux with Yocto, mainline U-Boot and mainline kernels,
device trees, secure remote update paths, board support from power-on to
SSH prompt.

**Data acquisition & monitoring.** Decentralised DAQ from the analog
front-end through ADC and transport up to the server: sensor signal
chains, high-throughput acquisition, time-stamping at the source, and the
monitoring infrastructure that keeps production and research systems
observable.

## Typical deliverables

- Schematic, layout, Gerber and assembly data, plus a bring-up report
- A board that boots: bootloader, kernel, BSP, update mechanism — documented and reproducible
- FPGA designs with constraints, testbenches and a CI-able build
- A DAQ chain with defined accuracy, calibration procedure and data interface
- Training for your team: I lecture at three universities and train engineers in digital measurement technology

## Selected projects

- **Open Zynq bitstream deployment pipeline** — JTAG bring-up to
  self-updating Yocto Linux on an ALINX AX7020, documented as a
  [public series](/posts/zynq-bitstream-deployment-concept-august-2026/) (since 2026)
- **PCB design for an embedded vision system with AI acceleration** — customer under NDA (2026)
- **[skAInet Edge-Compute](https://edge-compute.skainet.io/)** — M12-PoE switch, router and
  Linux compute module for industrial edge DAQ by Auto-Intern; system architect,
  M12 cabling specification and EMC campaign ([write-up](/posts/skainet-edge-compute-september-2026/)) (2016–2026)
- **Reflow-oven monitoring for predictive solder-quality assessment** —
  Kurtz Ersa, including [EMC certification in China](/posts/dongguan-emc-march-2026/) (2022–2026)
- **Electrochemical impedance spectroscope for biofilm detection** in US
  rivers — with Montana State University ([field report](/posts/msu-eis-2024/)) (2023–2026)
- **HV-MAPS silicon-detector test stands and wire-bonding line** —
  PANDA/FAIR, Ruhr-Universität Bochum (2020–2026)
- **skAInet / PowerSense critical-infrastructure monitoring** — incl. DB
  Netz AG ([ten-year retrospective](/posts/skainet-powersense-jan-2026/)) (2015–2025)

## How working with me works

You contract with **nabla B UG** (Amtsgericht Bochum, HRB 18817). When a
project needs more capacity, I bring in the AI-Gruppe companies I work
with — the contract and the responsibility stay with nabla B. Professionally
active since 2007; the full background, credentials and FAQ are on the
[about page](/about/), publications and patents on the
[publications page](/publications/).

## Get in touch

Write a few lines about your project — current state, what "done" looks
like, timeline:

- **[office@nabla-b.engineering](mailto:office@nabla-b.engineering?subject=Project%20inquiry%20via%20maxclerkwell.tech)** — commissioned engineering work
- **[stephan@boekelmann.net](mailto:stephan@boekelmann.net)** — everything else, including "is this even a project yet?"

</article>
</div>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "@id": "https://maxclerkwell.tech/hire/#webpage",
      "url": "https://maxclerkwell.tech/hire/",
      "name": "Hire Stephan Bökelmann — Freelance FPGA, Zynq, PCB & DAQ Engineering via nabla B",
      "inLanguage": "en",
      "isPartOf": { "@id": "https://maxclerkwell.tech/#website" },
      "about": { "@id": "https://nabla-b.engineering/#organization" },
      "mainEntity": { "@id": "https://nabla-b.engineering/#organization" },
      "author": { "@id": "https://maxclerkwell.tech/#person" },
      "breadcrumb": {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://maxclerkwell.tech/" },
          { "@type": "ListItem", "position": 2, "name": "Hire" }
        ]
      }
    },
    {
      "@type": ["Organization", "ProfessionalService"],
      "@id": "https://nabla-b.engineering/#organization",
      "name": "nabla B",
      "url": "https://nabla-b.engineering/",
      "email": "mailto:office@nabla-b.engineering",
      "founder": { "@id": "https://maxclerkwell.tech/#person" },
      "employee": { "@id": "https://maxclerkwell.tech/#person" },
      "areaServed": [
        { "@type": "Country", "name": "Germany" },
        { "@type": "Country", "name": "Austria" },
        { "@type": "Country", "name": "Switzerland" },
        { "@type": "Place", "name": "Remote / worldwide" }
      ],
      "knowsLanguage": ["de", "en"],
      "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "@id": "https://maxclerkwell.tech/hire/#offers",
        "name": "Engineering services offered through nabla B",
        "itemListElement": [
          { "@type": "Offer", "offeredBy": { "@id": "https://nabla-b.engineering/#organization" }, "itemOffered": { "@type": "Service", "name": "FPGA and Zynq development", "provider": { "@id": "https://nabla-b.engineering/#organization" }, "description": "HDL design (VHDL/Verilog), Zynq-7000 PS/PL systems, AXI integration, board bring-up with mainline U-Boot, open toolchains (Yosys, nextpnr) and Vivado/Vitis." } },
          { "@type": "Offer", "offeredBy": { "@id": "https://nabla-b.engineering/#organization" }, "itemOffered": { "@type": "Service", "name": "PCB design and bring-up", "provider": { "@id": "https://nabla-b.engineering/#organization" }, "description": "Schematic and layout in KiCad, multilayer, signal integrity, EMC preparation, manufacturing hand-off, supply-chain work with manufacturers in China and Europe, wire bonding." } },
          { "@type": "Offer", "offeredBy": { "@id": "https://nabla-b.engineering/#organization" }, "itemOffered": { "@type": "Service", "name": "Embedded firmware and Linux", "provider": { "@id": "https://nabla-b.engineering/#organization" }, "description": "Microcontroller firmware (bare-metal, RTOS), embedded Linux with Yocto, mainline U-Boot and kernel, device trees, remote update paths." } },
          { "@type": "Offer", "offeredBy": { "@id": "https://nabla-b.engineering/#organization" }, "itemOffered": { "@type": "Service", "name": "Data acquisition and monitoring systems", "provider": { "@id": "https://nabla-b.engineering/#organization" }, "description": "Decentralised DAQ from analog front-end through ADC and transport to server infrastructure: sensor signal chains, high-throughput acquisition, monitoring platforms." } }
        ]
      }
    }
  ]
}
</script>
