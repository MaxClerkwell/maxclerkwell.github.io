# CLAUDE.md

> **Note for Claude Code**: This project uses `AGENTS.md` as the primary instruction file for all AI coding agents.
>
> This file exists only for backward compatibility with Claude Code. Please read [AGENTS.md](AGENTS.md) instead.

All project-specific guidance for AI agents lives in `AGENTS.md`.

## SEO, JSON-LD and llms.txt (mandatory for every new article)

The site is a Jekyll blog served from GitHub Pages under the custom domain
**https://maxclerkwell.tech** (see `CNAME`); author and site owner is
**Stephan Bökelmann** (alias MaxClerkwell).

Machine readability (structured data for search engines, llms.txt for LLM
crawlers) is a first-class requirement here, not an afterthought. It is driven
entirely by post front matter, so an incomplete front matter block silently
degrades the JSON-LD and the llms.txt entry.

### Checklist "new blog post"

When creating a new post in `_articles/<kebab-slug>.md`, ALWAYS fill the
front matter completely:

```yaml
---
title: "Post Title"                     # required, becomes headline/name in JSON-LD
date: YYYY-MM-DD                        # required, ISO date, becomes datePublished
author: "Stephan Bökelmann"             # optional; falls back to site.author.name
description: "One-sentence summary."    # required, feeds JSON-LD description, post card, llms.txt
tags: [tag1, tag2]                      # optional, becomes JSON-LD keywords
keywords: "comma, separated, phrases"   # optional, used only when tags are absent
image: /assets/posts/<slug>/cover.jpg   # optional, absolute path; falls back to /slides/Avatar.jpg
last_modified_at: YYYY-MM-DD            # optional, becomes dateModified (defaults to date)
about_id: https://.../#id               # optional, @id of a site-graph entity the post is about
mentions_ids: [https://.../#id]         # optional, @ids of people/entities the post mentions (needs a stub in structured-data-slim.html)
license: https://.../                   # optional, overrides the default CC BY-SA 4.0 (see /licensing/)
video:                                  # optional, emits a VideoObject (see structured-data-video.html)
  id: YOUTUBE_ID
  name: "Video title"
  description: "One sentence."
  upload_date: YYYY-MM-DD
event:                                  # optional, emits an Event node for conference reports
  name: "KiCon Europe 2026"             # (see structured-data-event.html for all keys)
  start_date: YYYY-MM-DD
  end_date: YYYY-MM-DD
  location: "Venue"
  city: "Bochum"
  country: "DE"
  organizer_id: https://maxclerkwell.tech/#skunkforce
  role: organizer                       # organizer | performer | attendee
---
```

Notes on the actual field wiring (see `_includes/structured-data-post.html`):

- `description` is preferred; if missing, the include falls back to the
  generated `excerpt`. An explicit `description` is always better, because the
  same value is reused for the post card and for the llms.txt line.
- `image` MUST be an absolute path (`/posts/<slug>/assets/x.jpg` for legacy
  posts, `/assets/posts/<slug>/x.jpg` for new ones) or a full URL. A relative
  `assets/x.jpg` renders a 404 in JSON-LD, og:image and Twitter Card.
- `about_id`, `video` and `event` are all optional; `about` on the BlogPosting
  becomes a list when both `about_id` and `event` are set.
- `tags` win over `keywords`: if `tags` is non-empty it is joined into the
  JSON-LD `keywords` field and `keywords` is ignored.
- `layout: post` and the `/posts/<slug>/` permalink come from `_config.yml`
  (the `articles` collection plus `defaults`). Do not repeat them per post.

### What is generated automatically (never duplicate by hand)

- `_layouts/default.html` writes `<title>`, meta description, the
  `<link rel="canonical">` pointing at `site.url` (https://maxclerkwell.tech),
  and the Open Graph and Twitter Card tags by hand from the front matter.
  jekyll-seo-tag is deliberately NOT used: it emitted its own `@id`-less
  Person/WebSite JSON-LD on every page, duplicating the entities in
  `_includes/structured-data.html`. Do not reintroduce `{% seo %}`.
- Canonical entity `@id`s shared across maxclerkwell.tech,
  nabla-b.engineering and edge-compute.skainet.io (never invent local
  aliases for these): person `https://maxclerkwell.tech/#person`, nabla B
  `https://nabla-b.engineering/#organization`, Auto-Intern GmbH
  `https://www.auto-intern.de/#organization`, Meihui Huang
  `https://kathamatician.com/#person` (link her name to
  `https://kathamatician.com/`, never to GitHub), skAInet brand
  `https://www.skainet.io/#brand`, AI-Gruppe `https://gruppe.ai/#brand`,
  Edge-Compute `https://edge-compute.skainet.io/#product`. LinkedIn is
  always written as `https://www.linkedin.com/in/accelerator-stephan/`.
- Links to nabla-b.engineering and edge-compute.skainet.io open an
  interstitial (`_includes/leave-modal.html`) and get `?ref=maxclerkwell.tech`
  appended; add `data-no-leave` to an anchor to bypass it.
- `_includes/structured-data.html` holds the full site-wide schema.org
  `@graph` and is emitted only on `/`, `/about/`, `/hire/`, `/talks/` and the
  Edge-Compute article; every other page gets `structured-data-slim.html`,
  short stubs with the same canonical `@id`s (add a stub there whenever a new
  `about_id` or `organizer_id` target is introduced). The full graph (Person, nabla B, publisher Organization,
  WebSite) with stable `@id` values under `https://maxclerkwell.tech/#...`.
- `_includes/structured-data-post.html` is included only when `page.date`
  exists and emits the per-post `BlogPosting` JSON-LD, referencing the
  site-wide nodes by `@id` instead of repeating them.
- Licensing: `licensing.md` (`/licensing/`) is the single rights page. Every
  BlogPosting gets `license` (CC BY-SA 4.0 unless the front matter sets
  `license:`), `usageInfo`, `copyrightHolder` and `copyrightNotice`
  automatically; `default.html` emits `<link rel="license">`. Image files
  point at `/licensing/#images` via XMP `WebStatement`. Attribution must name
  "MaxClerkwell" and link back; keep that wording consistent with `ai.txt`.
- `llms.txt` (root, `permalink: /llms.txt`) is a Liquid template. Its
  "All writing" section is regenerated on every Jekyll build from
  `_includes/get-blog-posts.html`. Never add post entries manually.
- `sitemap.xml` (root, `layout: null`) is likewise a Liquid template and is
  rebuilt on every build. Never add URLs manually.
- `robots.txt` points crawlers at both `sitemap.xml` and `llms.txt`.

So: adding a properly filled `_articles/<slug>.md` is the ONLY manual step.
JSON-LD, canonical URL, feed, sitemap and llms.txt follow automatically.

### Relevant files

| File | Role |
| --- | --- |
| `_includes/structured-data-post.html` | per-post `BlogPosting` JSON-LD |
| `_includes/structured-data.html` | site-wide schema.org `@graph` |
| `_includes/get-blog-posts.html` | unified post list (legacy pages plus `articles`) |
| `llms.txt` | LLM-facing site summary plus auto-generated post list |
| `sitemap.xml` | auto-generated sitemap |
| `robots.txt` | crawler rules, sitemap and llms.txt pointers |
| `_config.yml` | `url`, `author`, collection and defaults, plugins |

### Repository rule

**Never commit binary files other than images that went through the image
pipeline.** Every image needs a watermarked master in `assets/images/`, a
downscaled display copy where the page uses it, and a manifest entry in
`_data/images.yml` — run `python3 scripts/images.py`, see "Images" in
`AGENTS.md`. Anything else (archives, PDFs, binaries, build artefacts) stays out
of the repository.
