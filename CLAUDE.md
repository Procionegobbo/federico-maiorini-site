# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a multilingual Hugo static site for Federico Maiorini's personal website (https://procionegobbo.it). It uses the `hugo-theme-ananke` theme (migrated from Stack) with custom layout overrides. The site supports Italian (default) and English content.

## Getting Started

1. Clone the repository with submodules: `git clone --recurse-submodules <repo-url>` or after cloning run `git submodule update --init`.
2. Ensure Hugo extended version 0.125.6 or compatible is installed.
3. Run `hugo server` to start the local development server.

## Common Development Tasks

- **Local development server**: `hugo server`
- **Production build**: `hugo build`
- **Build with minification** (as used in CI): `hugo --minify`
- **Deployment**: The site is automatically deployed to GitHub Pages via the `.github/workflows/deploy.yml` workflow on pushes to `main`. Uses Hugo extended version 0.125.6.

## Architecture

### Content Structure
- Content is organized by language (`content/it/`, `content/en/`) and section (`blog`, `gdr`, `scrittura`).
- Italian is the default language (`defaultContentLanguage = "it"`).
- Main sections differ per language: Italian includes blog, gdr, scrittura; English includes only blog.
- Each content file is typically a directory with `index.md` and assets.

### Configuration
- Primary config file: `config.toml` (the `config.yaml` file is empty).
- Defines multilingual setup, menu structure, theme parameters, Google Analytics.
- Menu entries are defined per language with different weights and labels.

### Layouts and Customizations
- Custom layout overrides are in `layouts/`
- Key custom partials:
  - `layouts/partials/sidebar-custom.html`
  - `layouts/partials/latest-articles-blog.html`
  - `layouts/partials/ultimi-articoli.html`
  - `layouts/partials/article-list/default.html`, `tile.html`, `compact.html`
  - `layouts/partials/sidebar/left.html`
  - `layouts/shortcodes/tony-loffa.html`
  ## Migrazione e validazione
  La migrazione è documentata in `specs/001-theme-migration/` con checklist, script di test e report Lighthouse.
  - `layouts/partials/head/custom.html` – adds favicon and Iubenda cookie consent script.
  - Various article-list partials (`default.html`, `tile.html`, `compact.html`) are also customized.
- Custom shortcodes:
  - `layouts/shortcodes/tony-loffa.html` – styled card for Tony Loffa content.
- Theme files are in `themes/hugo-theme-stack/` (Git submodule). Do not edit theme files directly; override in `layouts/`.

### Static Assets
- Static files (images, favicon, etc.) are in `static/`.
- The avatar image is referenced as `/images/ProcionegobboSmall.png`.

## CI/CD

The GitHub Actions workflow (`.github/workflows/deploy.yml`):
1. Checks out repo with submodules
2. Installs Hugo extended 0.125.6
3. Runs `hugo --minify`
4. Deploys `public/` directory to GitHub Pages using `peaceiris/actions-gh-pages`.

## Important Notes

- The `public/` directory contains the built site and is tracked in git (unusual for Hugo sites; typically ignored).
- Custom domain `procionegobbo.it` is configured via `public/CNAME`.
- The theme is a Git submodule; to update it, use `git submodule update --remote themes/hugo-theme-stack`.
- The theme requires attribution: "Theme Stack designed by Jimmy" must remain in the footer.
- Google Analytics ID is set in config (`G-7T0LHSKHVD`).
- The site uses goldmark renderer with `unsafe = true` to allow raw HTML in markdown.
- Custom sidebar avatar is enabled with local=false and src pointing to `/images/ProcionegobboSmall.png`.
- The `_default` directory exists but is currently empty; base templates are inherited from the theme.

## Active Technologies
- Hugo extended version 0.125.6 (as per constitution) + hugo-theme-stack (current), hugo-theme-ananke (new), GitHub Pages deployment, Iubenda cookie consent script, Google Analytics (001-theme-migration)
- N/A (static site with content files in `content/` directory) (001-theme-migration)

## Recent Changes
- 001-theme-migration: Added Hugo extended version 0.125.6 (as per constitution) + hugo-theme-stack (current), hugo-theme-ananke (new), GitHub Pages deployment, Iubenda cookie consent script, Google Analytics
