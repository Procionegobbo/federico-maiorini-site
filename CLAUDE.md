# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Repository type
- Hugo static site (theme: hugo-theme-stack)

Common commands
- Build site (local draft-free production build): hugo -D -v
- Serve locally with live reload (development): hugo server -D
- Serve with specific base URL: hugo server -D --baseURL "http://localhost:1313/"
- Clean public output: rm -rf public/ && mkdir public

How to run tests / linters
- This repository contains no language-specific test harness; use Hugo to validate templates by running hugo server and visiting pages.

High-level architecture
- content/: site content organized by language (content/it, content/en). Markdown files are canonical source of pages (front matter + body).
- layouts/: Hugo templates and partials used by the theme and to render content. Key files:
  - layouts/index.html: main page wrapper and language-specific article partials (line 1)
  - layouts/partials/: small template fragments (head/custom.html, latest-articles-blog.html, ultimi-articoli.html)
- config.toml: site configuration and i18n settings (languages.it, languages.en). This file contains a commented problematic line and language menu definitions (config.toml:83).
- public/: generated static output (can be committed to deploy). Treat as build artifact.
- static assets and images are stored under content/... or public/ when generated.

Notes and important repo-specific quirks
- config.toml contains a commented line marked "🔽 RIMUOVI QUESTA RIGA (causa del problema)" above an incorrectly placed languages.en.menu.main table (config.toml:83). Be careful when editing language menu sections to follow Hugo's config structure.
- The theme provides components; prefer modifying layouts/partials over editing the theme unless needed.

When making edits
- Read the relevant file(s) before editing (use Read tool). Prefer editing existing files rather than creating new ones.
- Do not modify files in public/ except to deploy; public/ is generated output.

When adding new content
- Place content under content/{lang}/ (eg. content/it/blog/my-post.md) with appropriate front matter (title, date, tags, categories, draft).

References to files
- config.toml:1-109
- layouts/index.html:1
- layouts/partials/latest-articles-blog.html:1-6
- layouts/partials/ultimi-articoli.html:1-6

