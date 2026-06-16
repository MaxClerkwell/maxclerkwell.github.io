# AGENTS.md

This file provides guidance to AI coding agents when working with code in this repository.

## What this is

A personal Jekyll blog and linktree for Stephan Bökelmann (alias MaxClerkwell), deployed to GitHub Pages via the `master` branch. No build step is run locally — GitHub Actions handles the Jekyll build on push.

## Local development

```bash
bundle install          # install Ruby gems (first time)
bundle exec jekyll serve --livereload   # serve at http://localhost:4000
```

Jekyll requires Ruby and Bundler. The site uses `github-pages` gem to mirror the GitHub Pages build environment.

## Architecture

- `_config.yml` — site-wide settings (title, plugins, excludes, collections, defaults)
- `_layouts/default.html` — shell with nav and footer; uses Inter + JetBrains Mono from Google Fonts and Font Awesome 6 for icons
- `_layouts/post.html` — wraps `default.html`, adds back-link and post header
- `assets/css/style.css` — all styles (single file, no preprocessor)
- `index.html` — home page: hero section, linktree grid, and auto-generated post list
- `posts/<slug>/...` — **legacy** blog posts (26 existing articles). Their `.md` source files and directories must never be moved or renamed (see "Adding a blog post").
- `_articles/<slug>.md` — **new** blog posts (Jekyll `articles` collection)
- `_includes/get-blog-posts.html` — single source of truth for the unified post list (legacy pages + new collection documents)

## Adding a blog post

### Legacy posts (the 26 articles that already exist)

These live under `posts/<slug>/` (some use `index.md`, most use `<slug>.md`).  
**Do not move, rename, or delete any of these files or their directories.** External sites and tools link directly to the raw `.md` sources on GitHub; changing their paths would break those links.

They continue to work exactly as before. Their frontmatter still contains the explicit `layout` and `permalink` (harmless; the new defaults only apply to the `articles` collection).

### New posts (recommended for all future writing)

Create a file `_articles/<kebab-slug>.md` (flat file, not a directory) with **minimal** frontmatter:

```yaml
---
title: "Post Title"
date: YYYY-MM-DD
tags: [tag1, tag2]
description: "One-sentence summary shown in the post card."
---
```

- `layout: post` and `permalink: /posts/<slug>/` are supplied automatically by `_config.yml` (the `articles` collection + defaults).
- The file is named `<kebab-slug>.md` so the collection permalink `/posts/:name/` produces the clean public URL `/posts/<kebab-slug>/`.
- **Images and other media** for new posts live in `assets/posts/<kebab-slug>/` and are referenced with absolute paths, e.g.:
  ```markdown
  ![Description](/assets/posts/my-post/photo.jpg)
  ```
  (This is the new convention; the old relative `assets/...` trick only works for the legacy `posts/<slug>/` layout.)

After adding the file, the post appears automatically on the home page, in the feed, sitemap, search, tag cloud, and archive.

The unified discovery logic lives in `_includes/get-blog-posts.html` (legacy `site.pages` filter + `site.articles`). Never duplicate the old `where_exp: "item", "item.url contains '/posts/'"` pattern again.

### Content model transition note

The hybrid approach (legacy pages + new `articles` collection) was chosen so that the 26 existing article Markdown files could remain at their historical paths forever while still giving future content a clean, idiomatic Jekyll structure.

## Article series naming conventions

### Zero-to-One (ZTO) series

All Zero-to-One articles must be named with the prefix `zero-to-one-*`:

```
_articles/zero-to-one-<topic>-<optional-subtitle>-<month>-<year>.md
```

Example: `_articles/zero-to-one-python-libraries-environments-june-2026.md`

Never use `<topic>-zero-to-one-*` or any other ordering. The series prefix always comes first.

## Writing style

- **No em-dashes.** Do not use the em-dash character (—) anywhere in articles, commit messages, or documentation. Replace with a comma, semicolon, colon, or a period depending on the grammatical context.

## Deployment

Pushing to `master` triggers `.github/workflows/deploy.yml`, which builds with `actions/jekyll-build-pages` and deploys to GitHub Pages. There is no staging environment.
