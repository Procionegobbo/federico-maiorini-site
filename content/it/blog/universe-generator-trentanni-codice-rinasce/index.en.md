---
title: "Universe Generator: Thirty Years of Code Reborn"
date: 2026-02-15
description: "The story of a space sector generator born in 1996 in Access Basic and reborn in 2026 thanks to AI coding agents. A personal journey through three decades of technology, passion for role-playing games, and coding."
tags:
  - AI
  - CodingAgents
  - AccessBasic
  - TypeScript
  - ClaudeCode
  - Deepseek
  - RetroComputing
  - RolePlaying
categories: ["programming", "AI", "personal projects"]
image: "universe-generator.jpg"
slug: "universe-generator-thirty-years-code-reborn"
toc: true
draft: false
# Open Graph / LinkedIn / Twitter meta
images:
  - "universe-generator.jpg"
ogTitle: "Universe Generator: When '96 Code Gets Reborn with AI"
ogDescription: "From 1996 to 2026: how a universe generator written in Access Basic was reborn thanks to Claude Code, Deepseek, and Gemini. An experiment on how AI changes the way we code."
twitterTitle: "Universe Generator: Thirty Years of Code Reborn"
twitterDescription: "The story of a 1996 project that was waiting for the right tools to be reborn. Access Basic, AI agents, and the magic of creating virtual universes."
---

# Universe Generator

## 1996: Access Basic and Virtual Dice

There's a piece of code I've been carrying around for thirty years. Yes, thirty years. Since 1996.
It was part of a personal project related to role-playing games, built on Microsoft Access 2.0, prehistoric stuff. In Access Basic, the scripting language that preceded VBA. For its time, it was incredibly advanced.

The system was a simple generator of space sectors based on probability tables. I found the tables on the internet, designed as aids for space-themed role-playing games. Using d6 and d100 dice, it could create star systems, their stars, and their planets. It was very simple, without many details (stellar class, planet type, diameter, and number of moons) and no pretense of realism. It was enough for me to let my imagination soar through outer space.

Mix together a passion for science fiction, role-playing games, delusions of omnipotence, having access to the company's Access licenses at the time, and the perfect storm condensed into a few nights of coding.

Back then, I wanted to reproduce the dice-based tables, so I wrote a parser in Access Basic that interpreted the notation used in role-playing games for dice rolls. For example, *1d6* means the result of rolling a six-sided die, *2d8+3* for the total of rolling two eight-sided dice plus 3, and so on. Simple perhaps, but remember that back then Stack Overflow didn't exist, the internet was just beginning, and artificial intelligence was pure science fiction. Just thick programming books, nerd friends, and lots of patience.

To the parser I added a series of functions to simulate the tables, a form to enter data (sector dimensions and number of systems to generate), Access tables to store the results, and the toy was ready: an interface to generate a galactic sector and explore it virtually, metaphorically navigating from one star to another to see what planets orbited in those systems.
```vb
' This fragment shows the planet generation logic:
' based on the orbital zone and dice result, type, diameter,
' and number of moons are assigned using formulas in RPG notation

Select Case True
    Case (dado <= 5)
      Pianeta("TipoPianeta") = "A"
      Pianeta("diametro") = 0
      Pianeta("numLune") = 0
    Case ((zona = Zona_B And dado <= 8) Or (zona = Zona_C And dado <= 75))
      Pianeta("TipoPianeta") = "G"
      TipoPianeta.FindFirst "TipoBreve = 'G'"
      formula = TipoPianeta("FormulaDiametro")
      Pianeta("diametro") = DiceParser(formula) * TipoPianeta("MoltiplicatoreDiametro")
      Pianeta("numLune") = DiceParser("2d10")
    Case ((zona = Zona_A And dado <= 60) Or (zona = Zona_B And dado <= 40) Or (zona = Zona_C And dado <= 80))
      Pianeta("TipoPianeta") = "R"
      TipoPianeta.FindFirst "TipoBreve = 'R'"
      formula = TipoPianeta("FormulaDiametro")
      Pianeta("diametro") = DiceParser(formula) * TipoPianeta("MoltiplicatoreDiametro")
      Pianeta("numLune") = Int(DiceParser("1d6") * DiceParser("1d6") / 10)
...
```

## The Long Sleep

Then life happened, work changed, and so did technologies. That Access database is long gone, but the files containing the Access Basic code have followed me ever since. Every now and then I'd pull them out and think it would be interesting to redo that project, maybe with a more modern interface, in a new language. Just to see what could come of it.

## 2026: The Experiment with AI Agents

A few days ago, the "universe generator" folder that's been sitting on my Mac desktop for years caught my attention again, and I ran an experiment: I uploaded the file to Deepseek and asked it to translate that old code into TypeScript. I could have done it myself, but I wanted to see how it would handle such ancient code. No problems at all, in seconds the fossil functions were reborn in a modern language. Again, nothing I couldn't have done myself, but the speed and ease with which I had the new code in hand was remarkable.

At that point, though, I had to do something with it. I couldn't abandon that code again until TypeScript itself became obsolete. I wanted to bring that generation system to life, and I thought it would be interesting to experiment with various coding agents to save myself the hassle of putting the pieces together.

I started with Claude Code, hooking it up to Deepseek's APIs (I had loaded €10 in credits months ago to experiment with the APIs). I prepared a detailed plan with the file containing the generation code, details for the backend (NodeJS + Express), and the frontend in Vue. Honestly, the frontend had issues: misaligned elements, various icon sizes, wobbling text. But the generation engine worked well, and for the first time in thirty years, the virtual dice rolled and generated pieces of universe.

The next step would have been to fix the frontend. But how? Since I was experimenting so much, I might as well do it right. I tried Antigravity, Google's fork of Visual Studio Code that integrates a coding agent based on Gemini. The interesting thing about Antigravity is that it uses Chrome autonomously: it opened the site, navigated it, took screenshots that it sent to Gemini for analysis, found all the frontend problems, and fixed them. Wow!
If I hadn't run out of credits in one evening, I would have continued with that.

## Expanding the Universe

Anyway, with the frontend fixed, the minimum was done. I had at least what I expected. At that point, the delusion of omnipotence struck: if I could shift my mental effort from writing code to inventing features, I could produce much more than I had in mind initially.
So switching to Copilot in WebStorm, I started making modifications:

- differentiate sectors (Extragalactic, Galactic Edge, Medium, Central Zone, Galactic Core) each with more realistic density and distribution of star types
- more planet types compared to the original eight from the tables
- a more scientifically accurate statistical distribution of planet types
- addition of planet data (diameter, mass, gravitational pull, Goldilocks zone)

Another addition compared to the initial idea was images of planets and stars. It took very little actually: in Antigravity I had it create two files containing prompts to feed to an image generator, and with Replicate's MCP it generated the images. At that point, I just had to tell it where and how to put them on the frontend.

## The Circle Closes

In the end, the system was ready. In this project, I wrote very few lines of code, mostly small corrections when something came to mind that was faster to write directly than to ask the machine.
But I can't say I didn't program; I just did it differently. Because there's nothing in the project I couldn't have done myself, but I did it in a fifth (maybe a tenth) of the time it would have normally taken.

There's something poetic about the fact that that '96 code, born in a night of enthusiasm in front of Access 2.0, had to wait thirty years to find its definitive form. It wasn't just a process of technological modernization: it was like finally giving legs to an idea that had remained closed in a folder for three decades, moved from computer to computer, waiting for the right moment. Today's tools - AI, coding agents - didn't do the work for me; they simply allowed me to focus on what I wanted to create instead of how to build it. And that's exactly what was needed to bring that old universe generator back to life.

It's a fun project, an experiment, and a small journey into my past.

[Universe Generator](https://universe-generator-xi.vercel.app)