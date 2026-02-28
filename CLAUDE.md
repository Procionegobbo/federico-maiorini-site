# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a multilingual Hugo static site for Federico Maiorini's personal website (https://procionegobbo.it). It uses the Ananke theme with custom layout overrides. The site supports Italian (default language) and English content.

## Getting Started

1. Clone the repository with submodules: `git clone --recurse-submodules <repo-url>` or after cloning run `git submodule update --init`.
2. Ensure Hugo extended version 0.156.0 or compatible is installed.
3. Run `hugo server` to start the local development server.

## Common Development Tasks

- **Local development server**: `hugo server`
- **Local development with drafts**: `hugo server -D`
- **Production build**: `hugo` (produces output in `public/` directory)
- **Build with minification** (as used in CI): `hugo --minify`
- **Deployment**: Automatically triggered on pushes to `main` via GitHub Actions (`.github/workflows/gh-pages.yml`). Runs `hugo --minify` and deploys to GitHub Pages.

## Architecture

### Content Structure
- Content is organized by language: `content/it/` (Italian) and `content/en/` (English).
- Italian is the default language (`defaultContentLanguage = "it"`).
- Main sections per language:
  - **Italian**: `blog`, `gdr` (role-playing games), `scrittura` (writing)
  - **English**: `blog` only
- Each content file is typically a directory with `index.md` and associated assets.

### Configuration
- Primary config file: `config.toml` (the `config.yaml` file is empty and unused).
- Key configuration elements:
  - Multilingual setup with language-specific content directories and menus
  - Table of Contents enabled globally (`toc = true`)
  - Callout shortcode support (`enableCallout = true`)
  - Disqus comments enabled (`shortname = 'procionegobbo-it'`)
  - Google Analytics enabled (ID: `G-7T0LHSKHVD`) with "Do Not Track" respect
  - Custom logo/favicon and Ananke color scheme settings
  - Menu entries per language with different labels (e.g., "GDR" in Italian, "RPG" in English)

### Layouts and Customizations
- Custom layout overrides are in `layouts/` (organized as `layouts/partials/` and `layouts/shortcodes/`)
- **Theme submodule**: `themes/ananke/` (Git submodule). Do not edit theme files directly; override in `layouts/`.
- To update the Ananke theme: `git submodule update --remote themes/ananke`
- Custom shortcodes in `layouts/shortcodes/` extend Ananke's built-in shortcodes
- The `_default/` directory exists but base templates are inherited directly from the theme

### Static Assets
- Static files in `static/`:
  - Logo/avatar: `/images/ProcionegobboSmall.png`
  - Favicon: `/favicon.png`
  - Other images and resources
- Hugo's resource pipeline caches processed assets in `resources/` directory

## CI/CD

The GitHub Actions workflow (`.github/workflows/gh-pages.yml`):
1. Triggered on pushes to `main` branch
2. Checks out repo with submodules (`fetch-depth: 0` for full history)
3. Installs Hugo extended version 0.156.0
4. Runs `hugo --minify` to build and minify the site
5. Deploys `public/` directory to GitHub Pages using `peaceiris/actions-gh-pages`

## Important Notes

- The `public/` directory contains the built site and is tracked in git (unusual for Hugo sites; typically this directory is ignored).
- Custom domain `procionegobbo.it` is configured via `public/CNAME`.
- The Ananke theme is a Git submodule in `themes/ananke/`. Do not modify theme files directly; use `layouts/` overrides instead.
- The site uses goldmark renderer with `unsafe = true` to allow raw HTML in markdown content (enables shortcodes and custom HTML).
- Colors in light mode are configurable via `params.colorScheme` in `config.toml` (currently: light mode, toggle disabled).
- Copyright notice is in footer: "Federico Maiorini" with custom footer text.
- The site has been recently migrated from Stack theme to Ananke theme, maintaining all URLs and content.
