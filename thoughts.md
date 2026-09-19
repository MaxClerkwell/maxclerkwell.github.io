---
layout: default
title: "Thoughts"
description: "The essays on maxclerkwell.tech: philosophy, epistemology of physics, consciousness, and the occasional argument about how to live and work."
permalink: /thoughts/
---
{% include get-sections.html %}
<section class="blog-archive">
  <h1>Thoughts</h1>
  <p class="archive-intro">{{ thoughts_posts.size }} essays on ideas rather than hardware: what physics can and cannot explain, autonomous will, consciousness, and why posting the wrong answer works. Newest first. The engineering writing lives under <a href="{{ '/tech/' | relative_url }}">Tech</a>; <a href="{{ '/blog/' | relative_url }}">all posts</a> together are also one list. Feed: <a href="{{ '/feed-thoughts.xml' | relative_url }}">feed-thoughts.xml</a>.</p>
  <div class="post-list h-feed">
    {% for post in thoughts_posts %}{% include post-card.html post=post %}{% endfor %}
  </div>
</section>
