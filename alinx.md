---
layout: default
title: "ALINX AX7020 — The Open Bitstream Pipeline Series"
description: "A public, article-by-article build of an open-source deployment pipeline for the ALINX AX7020 Zynq-7000 board: mainline U-Boot over JTAG, Yocto Linux in QSPI, Yosys/nextpnr bitstreams, and a REST API that loads them. No vendor tools in the loop."
permalink: /alinx/
image: /assets/posts/alinx-bring-up-jtag-detected-without-power-august-2026/m12-adapter.jpg
last_modified_at: 2026-09-14
---

{% include get-blog-posts.html %}
{% assign tagged = blog_posts | where_exp: "p", "p.tags contains 'alinx'" %}
{% assign concept = blog_posts | where_exp: "p", "p.url contains 'zynq-bitstream-deployment-concept'" %}
{% assign series = tagged | concat: concept | uniq | sort: "date" %}

<!-- ── Hero ─────────────────────────────────────────────── -->
<section class="series-hero">
  <p class="series-kicker">Article series · since August 2026</p>
  <h1>Deploying hardware like software,<br>on an <span>ALINX AX7020</span></h1>
  <p class="series-lead">
    ALINX sent me a Zynq-7000 development board. Instead of following the
    vendor workflow, I am replacing every black box between power-on and a
    configured FPGA with something whose source I can read: mainline U-Boot
    instead of the FSBL, Yocto instead of PetaLinux, Yosys and nextpnr
    instead of Vivado, a sysfs node instead of a programming cable, and an
    HTTP endpoint instead of a person. Every stage is documented as it
    happens, failures included.
  </p>
  <div class="series-hero-actions">
    <a href="#articles" class="hero-hire-btn">
      <i class="fas fa-book-open"></i>
      <span class="hero-discord-text">
        <span class="discord-name">Read the series</span>
        <span class="discord-note">{{ series.size }} articles so far</span>
      </span>
    </a>
    <a href="https://github.com/MaxClerkwell/ax7020-bringup" class="hero-discord-btn" target="_blank" rel="noopener noreferrer">
      <i class="fab fa-github"></i>
      <span class="hero-discord-text">
        <span class="discord-name">ax7020-bringup</span>
        <span class="discord-note">All sources on GitHub</span>
      </span>
    </a>
  </div>
</section>

<div class="divider"><hr></div>

<!-- ── The board ────────────────────────────────────────── -->
<section class="series-board">
  <figure class="series-board-figure">
    <img src="{{ '/assets/posts/alinx-bring-up-jtag-detected-without-power-august-2026/m12-adapter.jpg' | relative_url }}"
         alt="ALINX AX7020 on the bench, connected to the lab network through an M12 adapter"
         loading="lazy">
    <figcaption>The AX7020 on the bench. No serial cable, no SD card: the board is operated over Ethernet from the first bootloader on.</figcaption>
  </figure>
  <div class="series-board-text">
    <h2>The board</h2>
    <p>
      The <a href="https://www.alinx.com/" target="_blank" rel="noopener noreferrer">ALINX</a>
      AX7020 is a compact Zynq-7000 board built around the XC7Z020: a
      dual-core Cortex-A9 processing system and an Artix-7 class FPGA fabric
      on one die. It is the kind of board a project like this needs: all
      four boot sources are jumper-selectable, the Ethernet port hangs off
      the processor side and works with an empty FPGA, and the reference
      design is public.
    </p>
    <ul class="series-features">
      <li><strong>XC7Z020-2CLG400</strong>: 2× Cortex-A9 at 766 MHz plus 85k logic cells of 7-series fabric, JTAG IDCODE <code>0x23727093</code></li>
      <li><strong>1 GiB DDR3</strong>: two MT41J256M16 on a 32-bit bus at 533 MHz</li>
      <li><strong>32 MiB QSPI flash</strong>: Winbond W25Q256, home of the maintenance Linux</li>
      <li><strong>Gigabit Ethernet</strong>: PS GEM0 with an RTL8211E PHY, usable before any bitstream exists</li>
      <li><strong>Boot from JTAG, QSPI or SD</strong>, selected by one jumper</li>
      <li><strong>USB OTG, UART, SD, four PL LEDs</strong>, a PL oscillator at 50 MHz, and two 40-pin expansion headers</li>
      <li><strong>Open reference design</strong> from ALINX, from which the DDR and pin initialisation data is extracted without starting Vivado</li>
    </ul>
    <p class="series-disclosure">
      Full disclosure: the board is a sponsorship gift. ALINX has no say in
      what I write, and the series ignores most of their recommended workflow.
    </p>
  </div>
</section>

<div class="divider"><hr></div>

<!-- ── Articles ─────────────────────────────────────────── -->
<section class="series-articles" id="articles">
  <p class="section-label">The series, in order</p>
  <ol class="series-list">
    {% for post in series %}
    <li class="series-item">
      <a href="{{ post.url | relative_url }}">
        <span class="series-num">{{ forloop.index }}</span>
        <span class="series-item-body">
          <span class="series-item-title">{{ post.title }}</span>
          <span class="series-item-date">{{ post.date | date: "%B %-d, %Y" }}</span>
          <span class="series-item-desc">{{ post.description }}</span>
        </span>
      </a>
    </li>
    {% endfor %}
  </ol>
  <p class="series-next">
    <strong>Next up:</strong> the maintenance Linux in flash fetches the
    full image on its own, and that image brings the bitstream API up as a
    service. Cold power-on to a working REST endpoint, nobody logged in.
  </p>
</section>

<div class="divider"><hr></div>

<!-- ── Vendor CTA ───────────────────────────────────────── -->
<section class="series-vendor-cta">
  <div>
    <p class="series-kicker">For board vendors</p>
    <h2>Want your board taken apart like this?</h2>
    <p>
      This series exists because a vendor sent a board and got out of the
      way. If you make development boards, modules or silicon and want an
      independent, public, warts-and-all bring-up of your hardware with
      open tools, mainline software and an engineering audience, send a
      few lines about the board and what you would like to see.
    </p>
  </div>
  <a href="mailto:collaboration@maxclerkwell.tech?subject=Board%20collaboration%20via%20maxclerkwell.tech/alinx" class="hero-hire-btn">
    <i class="fas fa-envelope"></i>
    <span class="hero-discord-text">
      <span class="discord-name">collaboration@maxclerkwell.tech</span>
      <span class="discord-note">Boards, modules, silicon</span>
    </span>
  </a>
</section>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "CollectionPage",
      "@id": "https://maxclerkwell.tech/alinx/#webpage",
      "url": "https://maxclerkwell.tech/alinx/",
      "name": "ALINX AX7020 — The Open Bitstream Pipeline Series",
      "description": "{{ page.description }}",
      "inLanguage": "en",
      "isPartOf": { "@id": "https://maxclerkwell.tech/#website" },
      "author": { "@id": "https://maxclerkwell.tech/#person" },
      "about": { "@id": "https://maxclerkwell.tech/alinx/#board" },
      "breadcrumb": {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://maxclerkwell.tech/" },
          { "@type": "ListItem", "position": 2, "name": "ALINX AX7020 series" }
        ]
      },
      "mainEntity": {
        "@type": "ItemList",
        "itemListOrder": "https://schema.org/ItemListOrderAscending",
        "numberOfItems": {{ series.size }},
        "itemListElement": [
          {% for post in series %}
          { "@type": "ListItem", "position": {{ forloop.index }}, "url": "{{ post.url | absolute_url }}", "name": {{ post.title | jsonify }} }{% unless forloop.last %},{% endunless %}
          {% endfor %}
        ]
      }
    },
    {
      "@type": "Product",
      "@id": "https://maxclerkwell.tech/alinx/#board",
      "name": "ALINX AX7020",
      "description": "Zynq-7000 development board with an XC7Z020-2CLG400, 1 GiB DDR3, 32 MiB QSPI flash and Gigabit Ethernet.",
      "brand": { "@type": "Brand", "name": "ALINX" },
      "manufacturer": { "@type": "Organization", "name": "ALINX", "url": "https://www.alinx.com/" },
      "url": "https://www.alinx.com/"
    }
  ]
}
</script>
