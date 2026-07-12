---
title: "spec-to-code: from pipeline to plugin, and the bug I almost ignored"
date: 2026-07-12
description: "For months I've been using a pipeline of Claude Code agents to take a feature from idea to code. I built Chimera Forge, a kobold-generating API and a Discord bot with it: I packaged it into an installable plugin and, by actually testing it on a real Go project, I found a bug no static check would ever have caught."
categories: ["programming", "ai"]
tags:
  - ClaudeCode
  - AI
  - CodingAgents
  - Plugin
  - SpecToCode
featured_image: "spec-to-code.jpg"
slug: "spec-to-code-plugin-claude-code"
draft: false
toc: false

meta:
  image: "spec-to-code.jpg"
  title: "spec-to-code: from pipeline to plugin, and the bug I almost ignored"
  description: "For months I've been using a pipeline of Claude Code agents to take a feature from idea to code. I built Chimera Forge, a kobold-generating API and a Discord bot with it: I packaged it into an installable plugin and, by actually testing it on a real Go project, I found a bug no static check would ever have caught."
  author: "Federico Maiorini"
  type: "article"
---

*This post was translated from Italian with the help of Claude.*

For a few months now I've been using a pipeline of four Claude Code agents to take a feature from idea to implemented code: `stories-init` creates the workspace, `spec-builder` expands a rough idea into a complete spec, `story-creator` slices it into INVEST user stories, `laravel-feature-builder` implements a story in Laravel. It's not a weekend experiment: I built [Chimera Forge](https://chimera-forge.it) with it, a playful kobold-generating API ([kaas.procionegobbo.it](https://kaas.procionegobbo.it)) and a Discord bot ([kichand.procionegobbo.it](https://kichand.procionegobbo.it)). It's tested, it works, and right now it fully fits my way of doing agentic coding.

It had two practical limits, though. Adding support for a new stack (Go, Python, whatever was needed) was a manual copy-paste-adapt job. And installing the pipeline into another repo meant copying files by hand into `.claude/`. In one work session I solved both problems, found and fixed a latent bug, and tested the whole thing on a real Go project. Here's the write-up, including the parts that didn't work on the first try.

## A skill that builds agents

The first thing I added is `create-feature-builder`, a skill that, run inside any repo, detects the stack from the configuration files (and asks for confirmation), explores the code to understand the real test command, the formatter, the architecture and the features already written as precedents, and generates a `<stack>-feature-builder` agent tailored to that repo.

I made it a skill and not an agent for a specific reason: a skill runs inline in the conversation and can stop to ask for confirmation on the detected stack, a subagent runs autonomously and can't ask anything. "Agents that build agents" sounds like a gimmick, but in practice it's needed precisely because the human confirmation step is what avoids generating an agent tuned to the wrong stack.

The design idea I liked most is layered specialization. The generated agent encodes the stable things as authoritative directives, the test, formatting and static analysis commands, but the volatile things, like folder paths or example files, it emits as dated "seed hints", under an explicit "detect, don't assume" step. It's there to avoid the trap of the generated agent confidently pointing at paths that have since moved.

## From copy-paste to a single command

The repo became a Claude Code plugin (`spec-to-code`) and at the same time its own marketplace (`my-agents`). Installation went from "copy these files into `.claude/`" to:

```
/plugin marketplace add Procionegobbo/my-agents
/plugin install spec-to-code@my-agents
```

Versioned, updatable with `/plugin update`, usable in any project without touching files by hand.

## The bug I almost dismissed with a "probably fine"

This is the part worth telling in full. I had the plan reviewed by a second Anthropic model (Fable), which flagged that the agents' YAML frontmatter looked risky. The first check, a strict Python YAML parser, seemed to disagree, and for a moment I dismissed it with a "the runtime is probably more permissive".

Then I ran `claude plugin validate`, the official tool, and the verdict was clear: the `description` field was an unquoted YAML scalar containing `": "` sequences, which doesn't parse and silently drops the entire frontmatter at load time: name, model, everything. The bug was latent and affected all four agents. I fixed it by quoting the descriptions properly.

My fault: I had assumed the IDE's warning about the invalid frontmatter was down to the fact that I was editing an agent file and the IDE didn't quite recognize the syntax. The review flagged the problem and the official validator proved it.

## The test that found what static checks don't see

After installing the plugin, I ran it on a real project: RabbitLogger, a Go consumer that reads from RabbitMQ and writes to Postgres. Two problems surfaced that no static validation could ever have caught.

`stories-init` hallucinated the stack. An agent whose only job is to create the workspace folder, and which has no reason to inspect the technology stack, volunteered, wrongly, to guess the project's language and nature, calling a Go repo a "Python RabbitMQ logger project". The repo name, RabbitLogger, almost certainly seeded the wrong assumption. I fixed it by constraining the agent to its actual job.

The second problem was redundant and contradictory guidance in the generated agent's implementation step: two overlapping lists of things to watch out for, one generic and one stack-specific, that contradicted each other in one spot: "enforce authorization for every action" in the generic list versus "authorization: not applicable" in the Go-specific one. I fixed it by making the stack-specific notes the single source of truth.

The part that did work well: the generated `go-feature-builder` was accurate. Correct commands (`go test ./...`, `gofmt`, `go vet`), real `internal/…` paths as dated hints, correct recognition of the absence of a frontend and of an authentication layer ("don't invent one"), and genuine Go idioms (parameterized queries, graceful shutdown, `fmt.Errorf("…: %w")`) with no trace of Laravel vocabulary.

Three small releases in the same session, each for a problem found by using the tool for real: v3.0.0 with the plugin, marketplace, skill and the frontmatter fix; v3.0.1 with `stories-init` no longer guessing the stack; v3.0.2 with the contradictory concern list removed. Three PRs, each validated with `claude plugin validate` before merging.

## What I take away

The plugin had already passed static validation at v3.0.0. It was the first real run on a Go repo that surfaced the hallucination and the contradiction. Neither would have come up by reading the YAML or running the validator. Static validation tells you the tool is well-formed; only actually using it tells you whether it does what it's supposed to.

It holds for my pipeline in general too: I've already used it to build Chimera Forge, the kobold API and the Discord bot, and that's exactly why I trust where it's solid. It's also why I noticed right away when something was off in the new Go run.

One clarification, to stay honest about the boundaries of what I actually verified: I reviewed the generated `go-feature-builder` and confirmed it correct and valid, but I haven't yet used it to implement a real feature on that project: the full cycle, from spec to stories to code, hasn't been exercised end-to-end on Go yet. "I generated a correct, repo-tailored agent" is the right claim, "I built a Go feature" would not be.

---

### The code is on [github.com/Procionegobbo/my-agents](https://github.com/Procionegobbo/my-agents)
