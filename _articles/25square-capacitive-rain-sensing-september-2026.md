---
title: "Counting Raindrops with a Capacitor: The 25square Sensor, Its STM32, and the Patent Behind It"
date: 2026-09-02
author: "Stephan Bökelmann"
description: "How Auto-Intern built the street-level rain sensors for the 25square heavy-rain nowcasting project: a capacitive impact plate instead of a piezo, an STM32 with lwIP over PoE, a LoRa variant for the lampposts, and the jointly held patent DE 10 2020 119 488 B4 with Okeanos."
tags: [daq, measurement, stm32, lwip, poe, mqtt, lora, sensors, patent, mfund, bochum, edge-compute]
image: /assets/posts/25square-capacitive-rain-sensing-september-2026/25square-sensor-impact-plate.jpg
hire_cta: "data-acquisition or monitoring"
---

When people talk about AI-based heavy-rain forecasting, the conversation
usually starts at the model: data fusion, neural networks, nowcasting. It
rarely starts where the water actually hits — at the sensor. But a model is
only as good as its ground truth, and for street-level rain nowcasting in a
city, that ground truth simply did not exist in 2020. Weather radar sees
clouds from above; a municipal network of one or two calibrated gauges sees
almost nothing of a convective cell that dumps its load on six street blocks
and misses the rest of the city entirely.

**25square** set out to fix that: a research project funded through the
[mFUND programme](https://bmdv.bund.de/DE/Themen/Digitales/mFund/Ueberblick/ueberblick.html)
of the German federal ministry of transport (our sub-project at Auto-Intern
ran under grant 19F1064B), started in August 2020 together with
[Okeanos](https://www.okeanos.ai/) — then still Okeanos Consulting, founded
by Dr. Henning Oppel and Dr. Benjamin Mewes — and the
[Bochumer Institut für Technologie](https://bo-i-t.de/). The name is the
grid: one sensor per quarter square kilometre. For Bochum's 145 km² that
meant a target of roughly 580 sensors, dense enough that a rain cell cannot
sneak between the measurement points. Okeanos built the models and the GIS
pipeline; BO-I-T ran the server infrastructure; and at
[Auto-Intern](https://www.auto-intern.de/) we built the sensors — with
**Tabea Bökelmann (then Röthemeyer) as project lead**, [Odin
Holmes](https://github.com/odinthenerd) on hardware and bare-metal firmware,
and me on system architecture and the path from the sensor into the backend.

![The 25square project team at the IUZ Sternwarte Bochum, where the first two sensors went into the ground in May 2021. Front left: Tabea, project lead at Auto-Intern.](/assets/posts/25square-capacitive-rain-sensing-september-2026/25square-inline-3.jpg)

## Why not a tipping bucket — and why not a piezo either

The classic rain gauge is a tipping bucket: water collects in a funnel, a
see-saw flips every 0.1 mm or so, a reed contact counts the flips. It is
wonderfully simple and completely unsuitable for nowcasting. It integrates —
you learn that it *has* rained, minutes late, in coarse quanta — it clogs
with leaves, and it needs cleaning on a schedule that no one who plans to
deploy 580 of them wants to think about.

So we measured the raindrops themselves. Every drop arrives with kinetic
energy, and if you let it hit a plate, that impact is a measurable event.
The obvious first idea is a piezo disc glued to the plate — drop hits,
crystal produces a voltage spike, count the spikes and weigh them by
amplitude. We ended up somewhere else: the production sensor works
**capacitively**. The impact plate is a freely oscillating plate mounted at
a defined distance above a fixed base plate; the two form a capacitor. A
drop strike makes the plate ring, the gap modulates, the capacitance
modulates with it, and an oscillator built around an op-amp stage turns that
into a **frequency shift** that the microcontroller can track with nothing
more exotic than its timers. We took that route for a plain engineering
reason: it worked considerably more stably in the field. A frequency is a
robust thing to measure — you count edges instead of shepherding a
microvolt-level charge signal through an amplifier chain that also hears
wind, hail on the mast, and every lorry on the nearby road. The
discrimination between a drizzle droplet, a fat convective drop, and a
hailstone falls out of the impulse signature; timestamping happens at the
sensor, microsecond-accurate, at the source — which regular readers will
recognise as the hill I am [happy to die on](/posts/skainet-powersense-jan-2026/)
where decentralised DAQ is concerned.

![One of the sensors up close: the impact plate on its mast, the electronics in the sealed box below, PoE via the orange cable.](/assets/posts/25square-capacitive-rain-sensing-september-2026/25square-sensor-impact-plate.jpg)

## One STM32, two ways out of the box

Electrically the sensor is deliberately boring: an STM32 does everything.
It runs the oscillator measurement, filters and classifies the impact
events, aggregates them into per-interval intensity figures, and speaks to
the outside world. What varied was the outside world, and we built two
variants:

- **PoE + Ethernet.** For sites with infrastructure — the observatory, fire
  stations, public buildings — power and data share one cable.
  The STM32 runs **lwIP** directly on the metal, no operating system
  underneath, with an MQTT client on top. Every few seconds the sensor
  publishes its aggregated event data, timestamped at the source.
- **LoRa.** For lampposts and field sites without a network drop, the same
  STM32 design instead feeds a LoRa radio, running from battery and a small
  photovoltaic panel, autonomously for months. Coarser reporting intervals,
  same measurement core.

The choice to keep the network stack tiny and deterministic was not
aesthetic. A sensor that is supposed to sit on a roof for years, through
storms it is itself reporting on, has no business running a full OS whose
failure modes nobody has enumerated.

The receiving side is a piece of history I am fond of: the gateway and
server that collected the MQTT streams were a direct evolution of the
server we had built for railway-switch diagnostics in Deutsche Bahn's DIANA
programme — and what we learned running *this* fleet fed straight into what
became the [skAInet Edge-Compute](https://edge-compute.skainet.io/). If you
put the three systems side by side you can watch the same architecture grow
up: DIANA taught us to collect decentralised measurements reliably, 25square
taught us to do it cheaply and at city scale, and the Edge-Compute is the
productised answer to both.

From the gateway onwards it was Okeanos territory: the streams land in a
geoinformation system, get fused with the DWD's radar picture, and feed the
machine-learning model that turns a field of point measurements into a
moving picture of the rain cell — where it is, how intense, and which way
it is drifting. The promise on the tin: a street-accurate warning up to
**60 minutes** ahead.

## Did it measure anything? Yes — more than the official numbers

The first two sensors went into the lawn of the [IUZ Sternwarte
Bochum](https://www.sternwarte-bochum.de/) in May 2021, with the local fire
brigade offering station roofs for the next batch; about 15 sites were
eventually equipped. The most satisfying early result came in July 2021,
when our little plates recorded around **105 l/m²** during the storms that
summer while the publicly available figure for Bochum stood at 60 l/m² —
exactly the gap between "a gauge somewhere in the city" and "a sensor on
*your* street" that the project existed to demonstrate. We never needed the
full 580: the grid of deployed sensors was enough to validate the
measurement principle, the network design, and the models against reality.

![Tabea with one of the first installed sensors at the Sternwarte.](/assets/posts/25square-capacitive-rain-sensing-september-2026/25square-sensor-sternwarte-bochum.jpg)

## The patent

The measurement principle and the spatially-resolved analysis on top of it
became a patent, and it is a genuinely joint one: **DE 10 2020 119 488 B4**,
"Verfahren und System zur Analyse von Niederschlagsereignissen sowie
Computerprogrammprodukt und Verwendung", filed on 23 July 2020, granted in
December 2022, with the opposition period passing in late 2023 without a
single objection. The named inventors are Odin Holmes, Benjamin Mewes,
Henning Oppel, Tabea Röthemeyer, and me; it is held **50/50 by
[Okeanos Smart Data Solutions](https://www.okeanos.ai/) and Auto-Intern
GmbH** — the split mirrors how the work was actually done, physics and
hardware on one side, hydrology and models on the other. Alongside the
patent there is a parallel utility model, and both are still maintained.

<p><a href="https://www.okeanos.ai/"><img
  src="/assets/posts/25square-capacitive-rain-sensing-september-2026/okeanos-logo.png"
  alt="Okeanos Smart Data Solutions" width="180" loading="lazy"></a></p>

The full patent specification is public; here it is, if you want the claims
in their bureaucratic glory (the freely oscillating plate is in claim 1):

<object
  data="/assets/posts/25square-capacitive-rain-sensing-september-2026/DE102020119488B4.pdf"
  type="application/pdf"
  width="100%" height="800">
  <p>Your browser cannot display the PDF inline. You can download it with the button below.</p>
</object>

<p>
  <a href="/assets/posts/25square-capacitive-rain-sensing-september-2026/DE102020119488B4.pdf"
     download="DE102020119488B4.pdf">
    &#11015;&#65039; Download the patent DE&nbsp;10&nbsp;2020&nbsp;119&nbsp;488&nbsp;B4 (PDF)
  </a>
  &nbsp;·&nbsp;
  <a href="https://patents.google.com/patent/DE102020119488B4/de">View on Google Patents</a>
</p>

## Who did what

Since patents and press releases both have a way of flattening teams into
logos, here is the honest version. **Tabea** led the project at Auto-Intern
— hers is the coordination that got sensors from bench to rooftop — and she
designed and built a solid part of the software along the way; she also told
the story publicly at the time in the AI-Gruppe's
[LinkedIn article](https://www.linkedin.com/pulse/25square-damit-die-regenvorhersage-kein-gl%C3%BCcksspiel-bleibt-/),
which is where the photos in this post come from. **Odin** did what Odin
does: the hardware design and the bare-metal firmware discipline that lets
an STM32 run a network stack without an OS safety net. **I** owned the
system architecture — the sensor-to-backend chain, the two connectivity
variants, the decision to timestamp at the source, and the software path
from the MQTT ingest into the storage and the interfaces Okeanos consumed:
the same decentralised-DAQ pattern I keep coming back to in
[measurement](/posts/msu-eis-2024/) [projects](/posts/skainet-powersense-jan-2026/)
since. **Benjamin and Henning** turned all of it into hydrology: the GIS
integration, the radar fusion, and the nowcasting models that made the
sensor grid mean something.

## What became of it

For us at Auto-Intern, 25square ended the way a good research project
should: we had learned everything we set out to learn. The capacitive
measurement principle was validated, the patent was granted, and the
architecture lessons were already flowing into the M12-PoE platform that
became the Edge-Compute — so when the follow-up project was taking shape, we
passed the baton and turned our attention there. Okeanos carried the mission
forward, and did it well: in **heavyRAIN**
([mFUND](https://bmdv.bund.de/DE/Themen/Digitales/mFund/Ueberblick/ueberblick.html),
September 2022 to August 2025, together with
[hydro & meteo](https://www.hydrometeo.de/), [BO-I-T](https://bo-i-t.de/projekte/heavyrain/)
and LANUK NRW) they scaled the idea to four cities — Bochum, Hagen,
Lüdenscheid and Lübeck — this time densifying the networks with compact
commercial infrared sensors on street lights, and trained the nowcasting
model on more than 7,000 real and synthetic heavy-rain events, down to
[five-minute forecasts for the next hour](https://www.th-luebeck.de/hochschule/aktuelles/neuigkeiten/beitrag/2023-07-25-forschungsvorhaben-heavyrain-verbessert-regenmessung-fuer-starkregenvorhersage-in-luebeck/).
Different sensors, same conviction: you cannot forecast what you refuse to
measure.

That, in the end, is what I take from the project — and why I keep telling
customers that their analytics roadmap starts at the transducer. The
cleverest model in the cloud is downstream of a plate in the rain, a
well-behaved oscillator, and a microcontroller that knows exactly what time
it is.
