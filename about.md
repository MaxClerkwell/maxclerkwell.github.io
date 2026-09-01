---
layout: about
title: "About MaxClerkwell — Engineer & Physicist"
description: "Background, projects and contact details of Stephan Bökelmann (MaxClerkwell): embedded systems, FPGA development, DAQ and detector instrumentation."
last_modified_at: 2026-09-01
permalink: /about/
profile: true
---

# About Stephan Bökelmann

I'm an engineer, physicist, and freelance consultant based in Bochum, Germany, online as **MaxClerkwell**, and as **施泓杰** in the Chinese tech community. My work spans the full vertical stack of engineering: from silicon-level measurement systems and embedded firmware through monitoring infrastructure, data platforms, and application-layer software. The common thread is **decentralised data acquisition and observability**: getting reliable measurements out of complex systems, whether that system is a particle detector, a production line, or a distributed software stack.

## Work With Me

I'm available as a **freelancer** through my company **nabla B** for engineering projects: embedded firmware and microcontroller work, PCB design and bring-up, FPGA development, measurement and DAQ systems, and the monitoring infrastructure around them. From feasibility study to serial product, from "we need a prototype" to "our toolchain is holding us hostage": write to [stephan@boekelmann.net](mailto:stephan@boekelmann.net).

For **social media collaborations** (sponsored boards and tools, conference coverage, video and article partnerships under the MaxClerkwell brand), reach out via [collaboration@maxclerkwell.tech](mailto:collaboration@maxclerkwell.tech). Editorial independence is non-negotiable: sponsors never get a say in what I write.

## Background

My education runs the whole way up the stack, from the workbench to the cleanroom: I'm a trained mechanic and a trained electrician, hold a Bachelor's degree in electrical engineering and a Master's degree in information technology / computer engineering, and am currently working on my PhD thesis in experimental hadron physics at the **Institut für Experimentalphysik I** at Ruhr-Universität Bochum, developing **HV-MAPS ASICs for minimum ionizing particle detection**, as part of the **PANDA luminosity detector** experiment at [FAIR](https://fair-center.eu) (Facility for Antiproton and Ion Research) in Darmstadt. This work touches silicon detector R&D, including [HV-MAPS sensor characterisation](/posts/hv-maps-energy-loss-simulation-may-2026/), as part of a broader interest in DAQ systems and signal chain design from the sensor up.

My engineering career started in 2007. In 2009 I co-founded a diagnostics workshop with Stephan "Stegen" Freye, doing hands-on measurement and repair work; that business was later acquired by AUTO INTERN. Between 2010 and 2011 I worked as a junior consultant at **PROLAB Produkt + Produktion** under Prof. Gereon Kortenbruck at TFH Bochum (now THGA), alongside Lukas Jakubczyk, advising manufacturing companies in the Ruhrgebiet. From 2011 to 2014 I was at **Puls Plasmatechnik** in Dortmund, where I worked on measurement and power systems for research facilities, including projects for DESY, CERN, and GSI. That work led me into accelerator-adjacent instrumentation and the world of large-scale physics infrastructure.

In 2014 I joined **AUTO INTERN**, and together with Odin Holmes helped transform it into a sought-after contract developer for process diagnostics in industry and science. I'm now self-employed as managing director of **nabla B**, consulting on the development and use of digital measuring instruments and training engineers in digital measurement technology and data acquisition, and I continue to work closely with AUTO INTERN on contract, most visibly as system architect of the [skAInet Edge-Compute](https://edge-compute.skainet.io/) platform.

I'm a **lecturer** at **THGA Bochum** (University of Applied Sciences Georg Agricola Bochum), where I lecture on programming, object-oriented design, and databases, and build supplementary teaching material for students.

## Community

**emBO++**: I'm the principal organiser of the International Technical Symposium for Embedded Systems Development, held annually in Bochum. The conference brings together engineers from across Europe for deep-technical talks on modern C++ patterns for embedded and real-time systems. Read more about [why I think conferences matter](/posts/why-conferences-march-2026/).

**KiCon Europe**: what started as a local KiCad conference in Bochum has grown into KiCon Europe. I'm one of the organisers. In 2025 I also spoke at [KiCon Asia in Shenzhen](/posts/kicon-asia-2025/) on wire bonding for silicon detector chips.

**Practical DataScience Congress (PDSC)**: I co-organise this practitioner-focused event at the intersection of machine learning, measurement systems, and industry applications.

**Bochum AI-Gruppe**: together with Odin Holmes I co-lead this meetup group for engineers working with machine learning in production and science contexts.

**pottCPP**: I've been organising the Ruhr C++ user group since 2017.

I'm also a member of the **examination board of the Chamber of Commerce** (IHK Mittleres Ruhrgebiet) for IT specialists, since 2020.

## Teaching

- **Einführung in die Programmierung** — THGA Bochum, every winter term since WS 2019
- **Objektorientierte Programmierung** — THGA Bochum, every summer term since SS 2019
- **Einführung in DBMS** — THGA Bochum, since SS 2026
- **Moderne Webtechnologien 2** — Hochschule Bochum, SS 2025
- **Einführung in die hardwarenahe Programmierung** (for Cybersecurity and Applied Computer Science) — Ruhr-Universität Bochum, summer terms 2023–2025
- **Azubi-Zusatzkurs Fachinformatiker Anwendungsentwicklung** — online course via nabla B, since 2022

Course material is not public; external accounts for the THGA courses can be requested at [moodle.thga.de](https://moodle.thga.de).

See also: [Publications, Patents & Software](/publications/) and [Talks & Conference Appearances](/talks/).

## FAQ

**What is Stephan Bökelmann an expert in?**
Decentralised data acquisition (DAQ) and observability for industry and research: getting measurements reliably out of physical systems and into usable infrastructure — from the sensor through embedded firmware and PCB design up to the monitoring platform.

**What is decentralised data acquisition, and why prefer it over a central DAQ system?**
Decentralised DAQ puts measurement intelligence where the data originates — at the machine, the test stand, the detector — instead of routing every signal to a central measurement PC. That buys scalability (add a node, not a rack), fault tolerance (one failed node does not blind the whole system), short analogue cable runs, and timestamps taken at the source. A central system still wins when you need tight channel-to-channel synchronisation in one place; knowing when that is the case is part of the job.

**What freelance projects does he take on?**
Embedded firmware (microcontrollers, bare-metal and RTOS), PCB design and bring-up, FPGA development, measurement and DAQ systems, and the monitoring infrastructure around them — from feasibility study to serial product. Commissioned work goes through [office@nabla-b.engineering](mailto:office@nabla-b.engineering).

**Does he take on PCB design as a standalone project?**
Yes. Schematic and layout in KiCad, bring-up, EMC preparation, and handover to manufacturing — including supply-chain experience with Chinese board and cable manufacturers.

**How do I know my company has a data-acquisition problem?**
Typical symptoms: measurement data living in Excel islands, USB instruments tied to single lab PCs, no shared time base across measurements, and exactly one colleague who understands the measurement setup. If that sounds familiar, the measurement chain — not the analysis — is usually the bottleneck.

**What qualifies him?**
Professionally active since 2007, trained from the workbench up: mechanic, electrician, B.Eng., M.Eng., PhD work on DAQ for the PANDA experiment at FAIR, projects for CERN, DESY and GSI, a granted German patent ([DE 10 2020 128 143](/publications/)), and lecturing at three universities. See [Publications](/publications/) and [Talks](/talks/).

**What is nabla B?**
nabla B Ingenieurbüro und Dienstleistungs-UG (haftungsbeschränkt) is his engineering office in Bochum (Amtsgericht Bochum HRB 18817, founded 2020) — the legal home of the freelance work. It is part of the AI-Gruppe umbrella brand.

**Who do I contract with when I hire Stephan Bökelmann?**
With nabla B UG (Bochum, HRB 18817). Collaboration with Auto-Intern GmbH and the other AI-Gruppe companies adds capacity when a project needs it — the contract and the responsibility stay with nabla B.

**How do I reach him?**
Commissioned engineering work: [office@nabla-b.engineering](mailto:office@nabla-b.engineering). Social-media collaborations under the MaxClerkwell brand: [collaboration@maxclerkwell.tech](mailto:collaboration@maxclerkwell.tech). Everything else: [stephan@boekelmann.net](mailto:stephan@boekelmann.net).

## Citing me

Not to be confused with the UK agency Clerkswell, the musician Stephan Bodzin, or the actor Ludger Bökelmann. If your keyboard lacks an "ö": *Stephan Boekelmann*.

> **Stephan Bökelmann** — ORCID [0000-0002-2119-0064](https://orcid.org/0000-0002-2119-0064) — https://maxclerkwell.tech

## Projects

**[skAInet Edge-Compute](https://edge-compute.skainet.io/)**: Auto-Intern's programmable M12-PoE switch, router and Linux compute module for industrial edge data acquisition; one WAN port, seven sealed PoE ports, an 8-core ARM compute module and a Yocto Linux with documented SBOM. The platform under most of the monitoring projects below; my role is system architect: I contributed the PoE-first architecture, the M12 cabling specification and the system architecture of the reflow-oven monitor built on it. [Background on the blog](/posts/skainet-edge-compute-september-2026/).

**[OmnAIScope](/posts/omnaiscope-august-2025/)**: a simplified digital oscilloscope that turns waveform diagnostics into something an automotive workshop can actually use day to day. Grown out of the aw4null research programme, patent pending, and the hardware story behind it is [on the blog](/posts/omnaiscope-august-2025/).

**aw4null (autowerkstatt4null)**: a BMWK-funded, federated AI ecosystem for independent car workshops. Measurement data from off-board diagnostics feeds machine-learning models that help workshops diagnose faults without sending their data to a central silo.

**[MSU-EIS](/posts/msu-eis-2024/)**: embedded instrumentation for electrochemical impedance spectroscopy in the field, built with Montana State University. A resonance spectroscope that detects biofilms in river systems across the continental US.

<details class="about-projects" markdown="1">
<summary>Positions and selected R&amp;D projects over the years</summary>

**Positions**

| Years | Position |
|-------|----------|
| since 2021 | **Managing director, nabla B**: engineering office focused on data acquisition and physical measurement systems, embedded hardware, and custom development projects at the interface of industry and research |
| 2023 – 2025 | **Research associate, Forschungszentrum Nachbergbau** (post-mining research), geomonitoring department, THGA Bochum: multi-sensor geomonitoring and data fusion |
| 2020 – 2025 | **Research associate, Chair of Experimental Hadron Physics** (Prof. Dr. Miriam Fritsch), Ruhr-Universität Bochum: mixed-signal silicon detectors and high-throughput DAQ for PANDA/FAIR, luminosity detector design and construction, HV-MAPS characterisation with GSI Darmstadt |
| since 2018 | **Lecturer** at THGA Bochum, Hochschule Bochum, and Ruhr-Universität Bochum |
| 2018 – 2021 | **Chief Operating Officer, AI-Gruppe**: operational responsibility for the group, product line strategy, scalable manufacturing, international certification and development projects (incl. China) |
| 2016 – 2018 | **Head of development, Auto-Intern GmbH**: led the development team, responsible for system architecture of diagnostics and monitoring systems for automotive and rail infrastructure |
| 2014 – 2016 | **Developer, Auto-Intern GmbH**: hardware and software for vehicle diagnostics and condition monitoring, incl. for DB Netz AG |
| foundings | Kfz-Technik Bökelmann (2012, merged into Auto-Intern 2014) · CCD Car Diagnostics UG (2017, co-founder) · nerd_force1 UG (2018, co-founder) · nabla B UG (2020, co-founder) |

**Selected R&amp;D projects**

| Years | Project |
|-------|---------|
| 2026 | PCB design for an **embedded vision system with AI acceleration**, customer under NDA |
| since 2026 | **Zynq bitstream deployment pipeline**: open-source path from JTAG bring-up to a REST API for FPGA bitstreams on an Alinx AX7020 ([blog series](/posts/zynq-bitstream-deployment-concept-august-2026/)) |
| ongoing | **HORUS Monitoring**: production-grade observability and telemetry infrastructure (Kurtz Ersa / GlobalPoint) |
| ongoing | **HORUS Profiling**: performance profiling stack for embedded and distributed systems |
| ongoing | **STEMgraph**: STEM education tooling |
| ongoing | **ultraSonic**: ultrasonic measurement systems |
| 2026 | **Dual-uplink office networking**: Starlink failover and load balancing for a 15-person office on plain Linux routing ([write-up](/posts/dual-uplink-load-balancing-july-2026/)) |
| 2024 – 2026 | Building up a **wire-bonding production line** for HV-MAPS silicon detectors, Ruhr-Universität Bochum ([talk at KiCon Asia](/posts/kicon-asia-2025/)) |
| 2023 – 2026 | **Electrical resonance spectroscope for biofilm assessment** in rivers across the continental US, with Prof. Warnat, Montana State University ([field report](/posts/msu-eis-2024/)) |
| 2016 – 2026 | **skAInet Edge-Compute**: M12-PoE edge platform of Auto-Intern GmbH, from the DIANA gateway prototype to the v1.5 product; system architect: PoE-first architecture, M12 cabling specification, EMC certification ([product site](https://edge-compute.skainet.io/), [write-up](/posts/skainet-edge-compute-september-2026/)) |
| 2022 – 2026 | Integrated **monitoring system for predictive assessment of solder quality factors** on reflow machines, Kurtz Ersa ([EMC certification story](/posts/dongguan-emc-march-2026/)) |
| 2020 – 2026 | Multiple **test stands for characterising HV-MAPS sensors** for minimum ionizing particles (PANDA/FAIR) ([Geant4 simulation post](/posts/hv-maps-energy-loss-simulation-may-2026/)) |
| 2025 | **Big-data storage cluster** based on CephFS, THGA Bochum |
| 2023 – 2025 | **MineBerry-LoRa**: structural stability assessment of mine shaft closures, RAG &amp; Forschungszentrum Nachbergbau |
| 2020 – 2025 | **skAInet / PowerSense**: monitoring of critical infrastructure, incl. DB Netz AG ([ten-year retrospective](/posts/skainet-powersense-jan-2026/)) |
| 2024 | Multi-level **soil moisture sensor "Smart Green City"** with LoRa connectivity |
| 2022 – 2024 | Battery-powered **temperature profiling system** with WiFi, modern frontend, and cloud integration, Kurtz Ersa |
| 2020 – 2024 | **Digital oscilloscope** developed in autowerkstatt4null (2nd research phase, patent pending) ([OmnAIScope](/posts/omnaiscope-august-2025/)) |
| 2023 | **Infrared interferometry camera** for remote assessment of air-fin-cooler fouling, Kelvion |
| 2022 | **Enclosureless housings** for PCB cavities (patent pending) ([how it works](/posts/enclosureless-cases-april-2026/)) |
| 2020 – 2022 | **Vibration analysis of asynchronous machines** from electromagnetic signatures, DB Netz AG |
| 2021 | Measurement and analysis system for observing and predicting **heavy rain cells**, with PoE, 25square (patent pending) |
| 2019 – 2020 | Mechanical simulation and implementation of the **positioning mechanism for the luminosity tracking detector** of the PANDA experiment |
| 2017 – 2020 | **ML-based diagnostics approach** in autowerkstatt4null (BMWK-funded) |
| 2016 – 2020 | Co-development of the **IDS current sensor** for intelligent railway switch diagnostics in Deutsche Bahn's DIANA system |
| 2018 – 2019 | **Structure-borne sound sensor and analysis method** for plastic injection moulding machines |
| 2015 – 2016 | Co-development of a **lean/kanban production line** for the HEX-V2, Auto-Intern GmbH |

</details>

## Writing

This blog is the canonical home for longform writing, usually one post per week. I cover **decentralised DAQ and monitoring systems**, **university lecture material** from THGA Bochum, **particle physics instrumentation**, and **firsthand visits to manufacturing sites, labs, and accelerator facilities** around the world.

## Contact

<div class="about-contact">
  <a class="u-email" href="mailto:stephan@boekelmann.net">
    <i class="fas fa-envelope"></i> stephan@boekelmann.net <span style="opacity:0.6;">(freelance &amp; projects)</span>
  </a>
  <a class="u-email" href="mailto:collaboration@maxclerkwell.tech">
    <i class="fas fa-handshake"></i> collaboration@maxclerkwell.tech <span style="opacity:0.6;">(social media collaborations)</span>
  </a>
  <a class="u-url" href="https://linkedin.com/in/accelerator-stephan" target="_blank" rel="me noopener noreferrer">
    <i class="fab fa-linkedin"></i> linkedin.com/in/accelerator-stephan
  </a>
  <a class="u-url" href="https://x.com/maxclerkwell" target="_blank" rel="me noopener noreferrer">
    <i class="fab fa-x-twitter"></i> @MaxClerkwell
  </a>
  <a class="u-url" href="https://github.com/maxclerkwell" target="_blank" rel="me noopener noreferrer">
    <i class="fab fa-github"></i> github.com/maxclerkwell
  </a>
  <a class="u-url" href="https://www.researchgate.net/profile/Stephan-Boekelmann" target="_blank" rel="me noopener noreferrer">
    <i class="fas fa-flask-vial"></i> ResearchGate profile
  </a>
  <a class="u-url" href="https://orcid.org/0000-0002-2119-0064" target="_blank" rel="me noopener noreferrer">
    <i class="fab fa-orcid"></i> ORCID 0000-0002-2119-0064
  </a>
  <a class="u-url" href="https://inspirehep.net/authors/2177110" target="_blank" rel="me noopener noreferrer">
    <i class="fas fa-atom"></i> INSPIRE-HEP author record
  </a>
  <a class="u-url" href="https://arxiv.org/a/0000-0002-2119-0064.html" target="_blank" rel="me noopener noreferrer">
    <i class="fas fa-scroll"></i> arXiv listing
  </a>
</div>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "@id": "https://maxclerkwell.tech/about/#faq",
  "about": { "@id": "https://maxclerkwell.tech/#person" },
  "inLanguage": "en",
  "mainEntity": [
    { "@type": "Question", "name": "What is Stephan Bökelmann an expert in?", "acceptedAnswer": { "@type": "Answer", "text": "Decentralised data acquisition (DAQ) and observability for industry and research: getting measurements reliably out of physical systems and into usable infrastructure, from the sensor through embedded firmware and PCB design up to the monitoring platform." } },
    { "@type": "Question", "name": "What is decentralised data acquisition, and why prefer it over a central DAQ system?", "acceptedAnswer": { "@type": "Answer", "text": "Decentralised DAQ puts measurement intelligence where the data originates instead of routing every signal to a central measurement PC. That buys scalability, fault tolerance, short analogue cable runs, and timestamps taken at the source. A central system still wins when tight channel-to-channel synchronisation in one place is needed." } },
    { "@type": "Question", "name": "What freelance projects does Stephan Bökelmann take on?", "acceptedAnswer": { "@type": "Answer", "text": "Embedded firmware (microcontrollers, bare-metal and RTOS), PCB design and bring-up, FPGA development, measurement and DAQ systems, and monitoring infrastructure, from feasibility study to serial product. Commissioned work: office@nabla-b.engineering." } },
    { "@type": "Question", "name": "Does he take on PCB design as a standalone project?", "acceptedAnswer": { "@type": "Answer", "text": "Yes. Schematic and layout in KiCad, bring-up, EMC preparation, and handover to manufacturing, including supply-chain experience with Chinese board and cable manufacturers." } },
    { "@type": "Question", "name": "How do I know my company has a data-acquisition problem?", "acceptedAnswer": { "@type": "Answer", "text": "Typical symptoms: measurement data living in Excel islands, USB instruments tied to single lab PCs, no shared time base across measurements, and exactly one colleague who understands the measurement setup. Then the measurement chain, not the analysis, is usually the bottleneck." } },
    { "@type": "Question", "name": "What qualifies him?", "acceptedAnswer": { "@type": "Answer", "text": "Professionally active since 2007: trained mechanic and electrician, B.Eng., M.Eng., PhD work on DAQ for the PANDA experiment at FAIR, projects for CERN, DESY and GSI, a granted German patent (DE 10 2020 128 143), and lecturing at three universities." } },
    { "@type": "Question", "name": "What is nabla B?", "acceptedAnswer": { "@type": "Answer", "text": "nabla B Ingenieurbüro und Dienstleistungs-UG (haftungsbeschränkt) is Stephan Bökelmann's engineering office in Bochum (Amtsgericht Bochum HRB 18817, founded 2020), the legal home of his freelance work, and part of the AI-Gruppe umbrella brand." } },
    { "@type": "Question", "name": "Who do I contract with when I hire Stephan Bökelmann?", "acceptedAnswer": { "@type": "Answer", "text": "With nabla B UG (Bochum, HRB 18817). Collaboration with Auto-Intern GmbH and the other AI-Gruppe companies adds capacity when a project needs it; the contract and the responsibility stay with nabla B." } },
    { "@type": "Question", "name": "How do I reach Stephan Bökelmann?", "acceptedAnswer": { "@type": "Answer", "text": "Commissioned engineering work: office@nabla-b.engineering. Social-media collaborations under the MaxClerkwell brand: collaboration@maxclerkwell.tech. Everything else: stephan@boekelmann.net." } }
  ]
}
</script>
