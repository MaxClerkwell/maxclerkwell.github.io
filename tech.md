---
layout: default
title: "Tech"
description: "The engineering writing on maxclerkwell.tech: FPGA and embedded bring-up, PCB and chip-on-board, decentralised DAQ, embedded Linux, networking and databases."
permalink: /tech/
---
{% include get-sections.html %}
<section class="blog-archive">
  <h1>Tech</h1>
  <p class="archive-intro">{{ tech_posts.size }} articles on things that get built and measured: FPGA and embedded bring-up, PCB and chip-on-board, data acquisition, Linux and networking. Newest first. The essays live under <a href="{{ '/thoughts/' | relative_url }}">Thoughts</a>; <a href="{{ '/blog/' | relative_url }}">all posts</a> together are also one list. Feed: <a href="{{ '/feed-tech.xml' | relative_url }}">feed-tech.xml</a>.</p>
  <div class="post-list h-feed">
    {% for post in tech_posts %}{% include post-card.html post=post %}{% endfor %}
  </div>
</section>
