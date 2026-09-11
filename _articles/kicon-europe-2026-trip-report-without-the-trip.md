---
title: "KiCon Europe 2026: Trip Report without the Trip"
date: 2026-09-11
author: "Stephan Bökelmann"
description: "Three days of KiCon Europe 2026 at Gleis 9 in Bochum from the organiser's chair: KiCad 11 previews from Wayne Stambaugh, ngspice 47, open source test rigs, rigid-flex in space, a browser KiCad I am not sold on, and Seth Hillbrand's eight-hour training. Plus what changes for 2027."
tags: [kicad, conferences, open-source, pcb, bochum, skunkforce]
keywords: "KiCon Europe 2026, KiCad conference Bochum, Gleis 9, KiCad 11, ngspice 47, Open Skunkforce, Seth Hillbrand, Wayne Stambaugh, trip report"
image: /assets/posts/kicon-europe-2026-trip-report-without-the-trip/audience-selfie.jpg
hire_cta: "KiCad or PCB design"
---

In April 2019 I flew to Chicago for the very first KiCon and wrote a
[brief trip report](/posts/kicon-2019-a-brief-trip-report/) on the way
home. It ended with the sentence "It almost looks like we will be organizing
some sort of event like this in Germany." Seven years later I no longer
have a trip to report on. The conference comes to me. From 7 to 9 September
2026 [KiCon Europe](https://kicon.kicad.org/europe2026/) took place at
[Gleis 9](https://gleis-neun.de/) in Bochum, organised by
[KiCad Services Corporation](https://www.kipro-pcb.com/) together with
[Open Skunkforce e.V.](https://skunkforce.org/), which in practice means
[Seth Hillbrand](https://www.linkedin.com/in/sethhillbrand/) and me.

<figure>
  <img src="/assets/posts/kicon-europe-2026-trip-report-without-the-trip/audience-selfie.jpg" alt="Selfie in the main hall of Gleis 9 with the KiCon Europe 2026 audience behind me" loading="lazy">
  <figcaption>Organiser's view from the back row of the main hall at Gleis 9.</figcaption>
</figure>

## What KiCad is, for the people who landed here by accident

[KiCad](https://www.kicad.org/) is a free and open source suite for
[electronic design automation](https://en.wikipedia.org/wiki/Electronic_design_automation). You draw a schematic, assign footprints, lay
out the printed circuit board, run design rule checks, simulate with [SPICE](https://en.wikipedia.org/wiki/SPICE),
and export the manufacturing data. It started as a one-person project by
Jean-Pierre Charras in 1992, was picked up by [CERN](https://home.cern/) around 2013 when they
needed a tool they could audit and extend for open hardware, and has since
grown into a professional-grade package with a full-time developer team.
The [Zynq deployment concept](/posts/zynq-bitstream-deployment-concept-august-2026/),
the [OmnAIScope](/posts/omnaiscope-august-2025/) and every board I have
shown on this blog were drawn in it. The project is funded by donations and
by commercial support through KiCad Services Corporation, and KiCon is the
place where the developers and the users meet in person.

## How we got here

This was the third KiCon Europe in Bochum, after
[2024](/posts/kicon-europe-2024/) and 2025. Before that I had already run
KiCon Bochum in 2021, 2022 and 2023, without any institutional backing from
the KiCad project. Those were community events in the most literal sense:
a room, a projector, whoever showed up. The idea for all of it came from
Chicago 2019, when [Chris Gammell](https://chrisgammell.com/) invited me
to the first KiCon at [mHub](https://mhubchicago.com/). Since 2024 the project itself has been the
co-organiser, which changes a lot about the budget and nothing about the
atmosphere.

On our side, every one of these events runs through
[Open Skunkforce e.V.](https://skunkforce.org/), the non-profit
association we founded in Bochum for exactly this purpose. It is the legal
entity behind KiCon Bochum, KiCon Europe, [emBO++](https://embo.io/) and the
[Practical Data Science Conference](/posts/pdsc4k-may-2026/): it signs the
venue contract, holds the storage room with the crates, and makes sure the
tickets cover the costs rather than a profit margin. No sponsor money goes
anywhere except into the next event.

If you want the earlier chapters, they are all on this blog:
[KiCon 2019 in Chicago](/posts/kicon-2019-a-brief-trip-report/),
[KiCon Europe 2024](/posts/kicon-europe-2024/), the first edition with the
project on board, and [KiCon Asia 2025 in Shenzhen](/posts/kicon-asia-2025/),
where I was on the other side of the lectern for once. Why I keep doing
this at all is in [Ten Years of Conferences](/posts/why-conferences-march-2026/).

This year: two days of conference and one day of training. Programme from
nine in the morning until six in the evening on all three days, then a wind
down and a cold beer.

## Day one

Day one is always the stressful one for an organiser. Be there early.
Attendees show up much earlier than the schedule suggests. The coffee has
to be ready before the first one walks in, not after. Name badges, power
strips, the projector adapter that someone always needs. This year, thanks
to Hasan from Gleis 9 and his team, everything ran on rails. It was the most
relaxed conference I have ever run, and I have been doing this since 2014.

<figure>
  <img src="/assets/posts/kicon-europe-2026-trip-report-without-the-trip/registration-desk.jpg" alt="Seth Hillbrand at the registration and merchandise desk at the Gleis 9 bar" loading="lazy">
  <figcaption>Registration desk at the bar. Seth handing out KiCon shirts.</figcaption>
</figure>

Once everybody had found the breakfast buffet, Seth gave a short welcome
talk, and then [Wayne Stambaugh](https://gitlab.com/stambaughw), KiCad's
lead developer, went straight into the hard stuff: the feature set for
[KiCad 11](https://forum.kicad.info/t/post-v10-new-features-and-development-news/66611).
My two highlights were the visual overlay for skew matching, which shows you
on the board where a differential pair or a bus is out of tolerance instead
of burying it in a DRC list, and the improvements to the
[IPC API](https://dev-docs.kicad.org/en/apis-and-binding/ipc-api/). I still
wonder why it has to be [protobuf](https://protobuf.dev/) over [NNG](https://nng.nanomsg.org/) rather than a plain REST or
WebSocket server. A network-facing interface would make it much easier to
write plugins in whatever language, or to build entirely different user
front-ends on top of the same core. But fine. The IPC as it is today is good
enough for the plugins I want to write.

Next up was **prod-to-go** by Magnus Axelsson and Simon Lindh from
[Elektronikutvecklingsbyrån (EUB)](https://www.eub.se/en/solutions/) in
Sweden. They built their own toolchain that takes a KiCad board and
generates the test and flashing rig for it semi-automatically: cradle, [pogo
pin](https://en.wikipedia.org/wiki/Pogo_pin) positions, plungers, camera mount. Everything open source. If you have
ever spent a week building a [bed of nails](https://en.wikipedia.org/wiki/Bed_of_nails_tester) for a board that changed the next
week, this is the talk for you. There is a
[video of the workflow](https://youtu.be/rJKvEdpKSwc) on YouTube.

<figure>
  <img src="/assets/posts/kicon-europe-2026-trip-report-without-the-trip/eub-test-rig.jpg" alt="Magnus Axelsson and Simon Lindh from EUB on stage with a red 3D-printed test rig on the lectern" loading="lazy">
  <figcaption>EUB with the rig itself on the lectern.</figcaption>
</figure>

After that, Raphael Specht, field application engineer at
[Würth Elektronik](https://www.we-online.com/), gave a short demo of his 3D
workflow between KiCad and [FreeCAD](https://www.freecad.org/). I always find it worthwhile to watch how
other people actually use their tools. You pick up a shortcut or a habit
every time.

<figure>
  <img src="/assets/posts/kicon-europe-2026-trip-report-without-the-trip/raphael-specht-wuerth-3d-models.jpg" alt="Raphael Specht of Würth Elektronik presenting KiCad 3D models" loading="lazy">
  <figcaption>Raphael Specht, Würth Elektronik: 3D models in the design workflow.</figcaption>
</figure>

After a long lunch break in the courtyard,
[Prof. Holger Vogt](https://www.linkedin.com/in/holger-vogt-737ba5a8/)
presented the latest [ngspice](https://ngspice.sourceforge.io/), the
simulation engine behind KiCad's simulator. I have played with ngspice on
and off for years but never used it seriously in production. Maybe I
should. The feature in version 47 that got me is black-box models from
S-parameter files: characterise a real device under test with a [VNA](https://en.wikipedia.org/wiki/Network_analyzer_(electrical)), drop
the [Touchstone file](https://en.wikipedia.org/wiki/Touchstone_file) into the simulation, done. What impresses me even more
is Holger himself. He has long since retired and could sit back. Instead he
keeps maintaining one of the most important open source simulators there
is, and shows up in Bochum to talk about it. An icon of the open source
community, in my book.

<figure>
  <img src="/assets/posts/kicon-europe-2026-trip-report-without-the-trip/lunch-courtyard-gleis9.jpg" alt="Lunch break in the covered courtyard of Gleis 9 with deck chairs and the Würth Elektronik stand" loading="lazy">
  <figcaption>Lunch in the courtyard. Würth Elektronik had the stand by the container.</figcaption>
</figure>

Then [KiCAD-Prism](https://github.com/krishna-swaroop/KiCAD-Prism). Krishna
Swaroop Dhulipalla and Matteo Parenti have built a complete, self-hosted
project management platform for KiCad teams: git-native, online board and
schematic viewer, design reviews, parts library governance. Wild what the two
of them have put together.

After the coffee break, Kuan-Chung Chiu presented
[Kikakuka](https://github.com/buganini/Kikakuka), his workspace tool.
Panelisation is one of the things he has genuinely solved with it. The
other is live bidirectional sync with FreeCAD: change the edge cut in KiCad
and the board re-renders in FreeCAD; move a connector on the board in
FreeCAD and the footprint position updates in KiCad. That second direction
is the one mechanical engineers have been asking for.

[Marco Straubel](https://www.linkedin.com/in/marco-straubel-0ab74529/)
then showed how he uses KiCad at [DLR](https://www.dlr.de/en) to build the [rigid-flex](https://en.wikipedia.org/wiki/Printed_circuit_board#Rigid-flex) harnesses for
their deployable carbon fibre booms, the kind that unroll in orbit. Export
from [CATIA](https://www.3ds.com/products/catia), refinement in KiCad, and the result has flown. I never stop
being amazed by how much outrageous hardware is designed in KiCad. I am
looking forward to visiting Marco in the coming days.

Same theme right after: [Manuel Gonzalez](https://apc.u-paris.fr/~mgonzalez/cv/)
works on astroparticle and neutrino experiments at [APC](https://apc.u-paris.fr/) in Paris and wanted
to predict and optimise flex PCB shapes for space electronics. He
succeeded, is the short version.

Tom Elliot closed the day with a genuinely neat AI agent for KiCad work.
His framing, that AI PCB tools keep trying to automate the fun part while
the boring half stays manual, was the right one.

The evening wound down at Gleis 9 while Swaroop and the EUB team gave live
demos of their projects.

## Day two

Day two started with [Petr Hodina](https://github.com/phodina) and an open
hardware [USB/IP](https://usbip.sourceforge.net/) bridge. The problem he is solving is a nice one: in a
hardware CI lab you used to drop a cheap Linux SoC next to every device
under test, and the DRAM shortage killed that. His answer is a board around
a [RISC-V](https://riscv.org/) microcontroller that runs entirely from on-chip memory, no DDR at
all, but still carries USB 3.0, Gigabit Ethernet and a secure element so the
lab can verify each bridge is genuine before trusting it. Three demanding
subsystems on one small board, all routed in KiCad. His day job is mobile
Linux, and listening to him I decided I should finally put mobile Linux on
my own phone.

[Dominik Wernberger](https://github.com/Werni2A/OpenOrCadParser) then
walked through the reverse-engineering journey behind OpenOrCadParser,
starting from scratch in 2021. Discovering that OrCAD's DSN and OLB files
are [Microsoft Compound File Binary](https://en.wikipedia.org/wiki/Compound_File_Binary_Format) containers, pulling out the individual
streams, getting the alignment right with a hex editor, and then decoding
what each byte actually means. An enormous amount of work, and fascinating
to watch it laid out step by step. I did catch myself wondering how
important this kind of task will be in a few years, since large language
models are getting rather good at exactly this sort of pattern hunting. Or
are they? I am honestly not sure.

Tjark Gaudich talked about product lifecycle management in KiCad, driven by
ISO 22163, which demands PLM down to the component level. His approach is a
custom editor for KiCad database libraries so the workflow plugs into the
existing archival and ordering process without a separate PLM suite. That
much I got from the abstract. I had to step out for some fresh air during
his slot, so I honestly cannot tell you more. The recording will.

[Peter Kämmerling](https://www.fz-juelich.de/profile/kaemmerling_p) from
[JCNS](https://www.fz-juelich.de/en/jcns) instrument technology at Forschungszentrum Jülich asked whether
scientific electronics development in Germany is transitioning to KiCad. He
introduced [SEI](https://www.helmholtz-berlin.de/projects/sei/), the
conference of the scientific instrumentation study group, and pitched to its
members that they should contribute to KiCad and its libraries rather than
just consume them. It is good to see, again, that the German physics
community keeps moving to KiCad. In the evening Peter and I had a long
conversation about neutron experiments, in particular how you guide a
neutron beam from the source to the instrument. Genuinely exciting. I have
been to Jülich often enough myself, back when [COSY](https://en.wikipedia.org/wiki/COSY) was still running and we
tested [HV-MAPS](/posts/hv-maps-energy-loss-simulation-may-2026/) there.

[cpresser](https://ca.rstenpresser.de/blag/) shared his workshop concept
for teaching KiCad to beginners. He estimates somewhere between 500 and
1000 people have gone through one of his workshops by now, and the whole
thing fits on a single printed page: an astable multivibrator from
schematic to Gerber, with the keyboard shortcuts inline. It sounded a lot
like my own workshops, so I am reassured for now.

<figure>
  <img src="/assets/posts/kicon-europe-2026-trip-report-without-the-trip/cpresser-workshop-talk.jpg" alt="cpresser on stage with his one-page Design a Circuit Board with KiCad handout on the screen" loading="lazy">
  <figcaption>cpresser's one-page workshop handout: astable multivibrator, schematic to Gerber.</figcaption>
</figure>

After lunch, [Viktor Váczi](https://www.pcbjam.com/) presented PCBJam,
KiCad in the browser, with [Figma](https://www.figma.com/)-style collaboration on top: other people's
cursors and selections, comments, shared libraries. I don't know. Maybe in
a few years. So far I have not worked out what it is for. The access
problem in concurrent editing of a layout is not trivial at all, meaning
who is allowed to change what, and when, and how you keep two people from
routing through the same via. And interactive routing needs serious compute
if you want complex DRC evaluated live while you drag a trace. Interesting to see where
it goes, but for my daily work it does not solve a problem I have yet.

Sigurd Henriksen of [WCP Electronics](http://www.wcp-electronics.com/) is a
wild one. His talk on miniaturising designs went from the KiCad features
that help, through the tricks the designer has to drive by hand, to hacks
that openly challenge good design practice when there simply is no room
left. The amount of time he has put into making boards tiny is absurd. We
had a really good conversation afterwards and he gave me some tips for my
freelance work. If anyone needs really small PCBs, Sigurd is your man.

One thing he mentioned in passing stuck with me: embedded resistors. Instead
of placing a discrete 0402 on the surface, you pattern a resistive foil
laminated onto an inner layer, the kind of material
[Ticer](https://www.ticer.com/) and Ohmega make, and the resistor becomes
part of the stack-up. No footprint, no pick-and-place, no solder joint,
and the top layer is free for what actually needs to be there. Taken
further, you design an inner copper layer so that its geometry is the
component, much like you would lay out passives in silicon design rather
than buying them. I am wondering whether I should try that on a real board.
The fab options are limited and the tolerances are not what you get from a
thin-film part, but for pull-ups, terminations and the like it might be
exactly the right trade.

Artemis M showed five levels of documentation and annotation, all inside
KiCad, from plain text boxes up to proper graphs, with examples from real
projects. The philosophy part at the start, the how, what and why of
documenting a circuit at all, was as good as the demos. The documentation
symbols in particular appealed to me. I think I will prepare a
documentation talk for KiCon Asia.

Damjan Prerad, new on the KiCad team, explained pin-to-pad mapping in
KiCad 11. One part, many packages, and every package numbers its pins its
own way. Until now that meant a copy of the symbol per pinout. In 11 you
keep one symbol and a small table tells each footprint where the pins go.
A quiet feature that will save a lot of library maintenance.

Dennis Yaskevich closed the day with [datasheets.md](https://datasheets.md/),
a wiki for datasheets: PDFs parsed into one structured page per component,
pin tables turned into symbols, footprints matched against the stock KiCad
libraries, plus an API and an [MCP](https://modelcontextprotocol.io/) server for AI tools. A product pitch for
his website, basically. I was not impressed.

The evening again ended comfortably with a beer. Many good conversations,
but at some point I was properly exhausted.

## Day three: training

On the third day Seth ran his advanced KiCad training. I am genuinely
impressed by how he carries an eight-hour workshop. Perfectly prepared,
USB sticks, printed handouts, no dead time. If you want to book Seth for
training, I believe these are the best KiCad courses money can buy.

<figure>
  <img src="/assets/posts/kicon-europe-2026-trip-report-without-the-trip/workshop-seth-day3.jpg" alt="Training day at Gleis 9: attendees at laptops following Seth Hillbrand through a KiCad schematic" loading="lazy">
  <figcaption>Training day. Every laptop on the same schematic.</figcaption>
</figure>

<figure>
  <img src="/assets/posts/kicon-europe-2026-trip-report-without-the-trip/workshop-seth-lectern.jpg" alt="Seth Hillbrand at the lectern with the KiCad schematic editor on the screen" loading="lazy">
  <figcaption>Seth Hillbrand, hour six of eight.</figcaption>
</figure>

Teardown went surprisingly fast. Sorting everything back into storage is
always hell.

<figure>
  <img src="/assets/posts/kicon-europe-2026-trip-report-without-the-trip/storage-crates.jpg" alt="Yellow crate labelled KiCon on top of boxes of thermos pots in the storage room" loading="lazy">
  <figcaption>The KiCon crate, back in the storage room until next year.</figcaption>
</figure>

<figure>
  <img src="/assets/posts/kicon-europe-2026-trip-report-without-the-trip/storage-shelf.jpg" alt="Storage shelf with mugs, glasses and flight cases after the conference" loading="lazy">
  <figcaption>Mugs, glasses, flight cases. Conference infrastructure at rest.</figcaption>
</figure>

## What is next

All in all a successful event. Let's see how we organise 2027. The
conference may move to Munich and be hosted by Würth Elektronik, but that
will only become clear in the next few weeks. Next goal on my list:
prepare a documentation talk for [KiCon Asia](https://kicon.kicad.org/asia2026/) in Shenzhen, where I
[spoke about wire bonding](/posts/kicon-asia-2025/) last year.

The full programme with abstracts is on
[pretalx](https://pretalx.kicad.org/kicon-europe-2026/schedule/). Recordings
will appear on the KiCad YouTube channel as they are cut.
