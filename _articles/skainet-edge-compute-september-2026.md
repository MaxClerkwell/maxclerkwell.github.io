---
title: "skAInet Edge-Compute: The Box We Kept Rebuilding Now Has a Product Page"
date: 2026-09-01
author: "Stephan Bökelmann"
description: "Auto-Intern's skAInet Edge-Compute is now a product with its own site: a sealed M12-PoE switch, router and 8-core Linux compute module for industrial edge data acquisition. What it is, where it came from, and where I fit in."
tags: [electronics, embedded, linux, monitoring, engineering]
image: "https://edge-compute.skainet.io/img/edge-branded.jpg"
about_id: "https://edge-compute.skainet.io/#product"
hire_cta: "data-acquisition or monitoring"
---

For about ten years, every monitoring system I helped build at
[Auto-Intern](https://auto-intern.de) had the same thing sitting in the
middle of it: a small Linux box with one uplink, a handful of PoE ports, and
enough compute to make sense of the sensors hanging off it. It was never the
product. The product was the PowerSense, or the reflow oven monitor, or
whatever the customer had actually asked for. The box was the thing we
rebuilt each time to make the product work.

That box now has a name, a version number, and its own website:
[**skAInet Edge-Compute v1.5**](https://edge-compute.skainet.io/).

<figure>
  <img src="https://edge-compute.skainet.io/img/edge-branded.jpg" alt="skAInet Edge-Compute: anodized aluminium enclosure with sealed M12 connectors" loading="lazy">
  <figcaption>One block of anodized aluminium, every port sealed. Photo: Auto-Intern GmbH.</figcaption>
</figure>

## What it is

In one sentence: a programmable M12-PoE switch, router, and compute module
for industrial edge applications, built in Germany by Auto-Intern GmbH.

The parts that matter, in the order I care about them:

- **Two separate Ethernet interfaces.** One M12 WAN port joins the upstream
  company network. An internal 8-port switch fans out to **seven M12 LAN
  ports**, each with PoE Class 3, on which the device spans its own DHCP
  network. Sensors, PLCs, cameras and skAInet measurement devices hang on the
  LAN side; only what you choose to forward leaves through the WAN side.
- **Real compute.** An 8-core 64-bit ARM at 1.5 GHz, 8 GB LPDDR4-3200,
  32 GB eMMC. Enough to buffer, pre-process and analyse measurement data
  where it is produced, rather than shipping raw samples upstream and hoping.
- **A compute module you can swap.** The heart is pin-compatible with the
  Raspberry Pi Compute Module family and sits on a skAInet carrier board. A
  faster or cheaper module can be fitted later; enclosure, carrier and ports
  stay the same.
- **48 to 72 V DC in over M12.** One cable powers the module and all seven
  attached PoE devices.
- **Sealed.** Anodized aluminium enclosure, sealed M12 connectors, rated for
  operation under water up to 1 bar. That is not a marketing number; the
  same design was on the bench for the
  [EMC campaign in Dongguan](/posts/dongguan-emc-march-2026/), where the
  anodized housing nearly broke the shield path at the M12 connectors.
- **Yocto Linux with a documented SBOM.** Full Linux, SSH access, write your
  data mappers and aggregators in C++ or Python. The software bill of
  materials is there because the EU Cyber Resilience Act will ask for it,
  and because a customer running critical infrastructure should be able to
  read it before we do.

Upstream, it speaks whatever your systems already speak: REST, WebSocket,
webhooks, MQTT, OPC UA, Modbus-TCP, EPICS, gRPC, AMQP, CoAP, SNMP,
Prometheus, InfluxDB, SFTP and rsync. Downstream, it collects, polls and
receives from anything with a network port.

Pricing starts at USD 299, and the
[technical specifications](https://edge-compute.skainet.io/docs/specifications)
and a [getting-started guide](https://edge-compute.skainet.io/docs/getting-started)
are public.

## Where it came from

The lineage is documented on this blog, in pieces:

- The [PowerSense retrospective](/posts/skainet-powersense-jan-2026/) shows
  the DIANA Edge Computer Gateway, a DB-branded rack-mount prototype from
  the switching-station days. The "PoE first" rule and "digitise as close to
  the source as possible" both come from that project.
- The [Dongguan EMC story](/posts/dongguan-emc-march-2026/) describes the
  reflow oven monitor for Kurtz Ersa: a compact Linux box with one WAN port
  and a seven-port PoE switch, auto-detecting attached measurement modules
  and serving REST, WebSocket and MQTT upstream. That is the Edge-Compute
  before it had the name.
- The [AX7020 bring-up article](/posts/alinx-bring-up-jtag-detected-without-power-august-2026/)
  shows the M12 adapter and the cables we specified together with GH
  Electronic in Dongguan; the same cables ship with the Edge-Compute.

Ten years of rebuilding the same thing is a strong hint that it wants to be
a product. Version 1.5 and its predecessors have been running 365/24/7 in
plants collecting data, operating measurement devices and delivering results
for long enough that the "product" step was mostly a matter of writing it
all down.

## Where I fit in

I joined Auto-Intern in 2014, was head of development from 2016 to 2018,
which is when the PoE-first architecture became the house style, and have
been Chief Operating Officer since 2018. In parallel I run
[nabla B](https://nabla-b.engineering/), my own engineering office. The
Edge-Compute is the platform underneath most of the monitoring projects
listed on my [about page](/about/). My role on it is system architect: I was system architect on the reflow oven monitor
built on top of it, co-developed the M12 adapter, and specified the
cabling. [Odin Holmes](https://x.com/odinthenerd) owns
hardware and firmware, [Tabea Bökelmann](https://x.com/tabeatheunicorn)
owns software and the APIs; the whole team is on the
[team page](https://edge-compute.skainet.io/team).

If you want an Edge-Compute in your plant, the product side is Auto-Intern:
[info@auto-intern.de](mailto:info@auto-intern.de) or the
[contact page](https://edge-compute.skainet.io/contact). If you need
someone to design the measurement chain that hangs off its seven PoE ports,
or to get your own sensor onto that network, that is the part I do
freelance; see [/hire](/hire/).
