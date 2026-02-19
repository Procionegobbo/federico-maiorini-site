---
title: "Universe Generator: codice che rinasce dopo trent'anni"
date: 2026-02-15
description: "La storia di un generatore di settori spaziali nato nel 1996 in Access Basic e rinato nel 2026 grazie agli AI coding agents. Un viaggio personale attraverso tre decenni di tecnologia, passione per i giochi di ruolo e coding."
tags: ["blog", "AI", "CodingAgents", "AccessBasic", "TypeScript", "ClaudeCode", "Deepseek", "RetroComputing", "GiochiDiRuolo"]
categories: ["programmazione", "AI", "progetti personali"]
image: "universe-generator.jpg"
slug: "universe-generator-trentanni-codice-rinasce"
toc: true
draft: false
# Open Graph / LinkedIn / Twitter meta
images: "universe-generator.jpg"
ogTitle: "Universe Generator: quando il codice del '96 rinasce con l'AI"
ogDescription: "Dal 1996 al 2026: come un generatore di universi scritto in Access Basic è rinato grazie a Claude Code, Deepseek e Gemini. Un esperimento su come l'AI cambia il modo di programmare."
twitterTitle: "Universe Generator: trent'anni di codice che rinasce"
twitterDescription: "La storia di un progetto del 1996 che aspettava gli strumenti giusti per rinascere. Access Basic, AI agents e la magia di creare universi virtuali."
---

## 1996: Access Basic e dadi virtuali

C'è un pezzo di codice che mi porto dietro da trent'anni. Sì, trent'anni. Dal 1996.
Era parte di un mio progetto personale legato ai giochi di ruolo, lo realizzai su Microsoft Access 2.0, preistoria. In Access Basic, il linguaggio di scripting che precedette VBA. Per l'epoca era una roba avanzatissima.

Il sistema consisteva in un generatore, semplice, di settori spaziali basato su tabelle di probabilità. Le tabelle le trovai su internet ed erano state pensate come ausilio per giochi di ruolo a tema spaziale. In pratica con l'uso di dadi da 6 e da 100 permetteva di creare sistemi stellari, le loro stelle e i loro pianeti. Era molto semplice, non c'erano molti dettagli (classe stellare, tipo di pianeta e diametro e numero di lune) e nessuna pretesa di realismo. A me bastava per far volare la fantasia nello spazio siderale.

Mischiamo la passione per la fantascienza, per il gioco di ruolo, il delirio di onnipotenza, l'avere a disposizione le licenze Access dell'azienda di allora e la tempesta perfetta si era condensata su alcune nottate di coding.

All'epoca volevo riprodurre le tabelle basate su dadi e quindi mi scrissi in Access Basic un parser che interpretava la notazione usata nei giochi di ruolo per il lancio di dadi. Per esempio *1d6* vuol dire il risultato del lancio di un dado da sei facce, *2d8+3* per il totale del lancio di due dadi a otto facce a cui viene aggiunto 3 e così via. Banale forse ma ricordiamo che all'epoca non esisteva Stackoverflow, internet era all'inizio e l'intelligenza artificiale era solo fantascienza. Solo libroni di programmazione, amici nerd e tanta pazienza.

Al parser si aggiunse una serie di funzioni per simulare le tabelle, una form dove inserire i dati (dimensioni del settore e numero di sistemi da generare), tabelle su Access per memorizzare il risultato e il giocattolo era pronto: un'interfaccia dove generare un settore galattico e esplorarlo virtualmente navigando metaforicamente tra una stella e l'altra per vedere quali pianeti orbitassero in quei sistemi.
```vb
' Questo frammento mostra la logica di generazione dei pianeti:
' in base alla zona orbitale e al risultato del dado, vengono assegnati
' tipo, diametro e numero di lune usando le formule in notazione RPG

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

## Il lungo sonno

Poi è successa la vita, il lavoro cambia, le tecnologie pure. Quel db Access è perso ormai ma i file contenenti il codice Access Basic mi hanno seguito da allora. Ogni tanto li tiravo fuori e pensavo che sarebbe stato interessante rifare quel progetto, magari con un'interfaccia più moderna, in un linguaggio nuovo. Così, per vedere cosa se ne poteva tirare fuori.

## 2026: L'esperimento con gli AI agents

Qualche giorno fa la cartella "generatore di universi" che ormai risiede sul desktop del mio Mac da anni ha attirato di nuovo la mia attenzione e ho fatto un esperimento: ho caricato il file su Deepseek e gli ho chiesto di tradurre quel vecchio codice in Typescript, avrei potuto farlo da solo ma volevo capire come se la cavasse con un codice così vecchio. Senza problemi direi, in pochi secondi le funzioni fossili sono rinate in un linguaggio moderno. Ripeto, nulla che non potessi fare da solo ma la velocità e facilità con cui ho avuto sotto mano il nuovo codice è stata notevole.

A quel punto però dovevo farci qualcosa, non potevo abbandonare di nuovo quel codice fino a quando anche Typescript non fosse divenuto obsoleto. Volevo dare vita a quel sistema di generazione e ho pensato che sarebbe stato interessante sperimentare con vari agenti di coding per sfruttarli ed evitarmi la rottura di mettere insieme i pezzi.

Ho iniziato con Claude Code, agganciandogli le API di Deepseek (avevo 10€ di credito caricati mesi fa per sperimentare con le API). Ho preparato un piano dettagliato con il file col codice di generazione, i dettagli per il backend (NodeJS + Express) e per il frontend in Vue. Sinceramente il frontend aveva problemi: allineamenti sballati, icone di dimensioni varie, testi barcollanti. Però l'engine di generazione funzionava bene e per la prima volta da trenta anni i dadi virtuali rotolavano e generavano pezzi di universo.

Il passo successivo sarebbe stato sistemare il frontend. Ma come? Visto che stavo sperimentando tanto valeva farlo bene. Ho provato con Antigravity il fork di Visual Studio Code fatto da Google che integra un coding agent basato su Gemini. La cosa interessante di Antigravity è che usa Chrome in autonomia: ha aperto il sito ha navigato, si è fatto le schermate che ha mandato a Gemini per analizzarle, ha trovato tutti i problemi del frontend e li ha corretti. Wow!
Se non avessi finito i crediti in una serata avrei continuato con quello.

## Espandere l'universo

Comunque col frontend sistemato il minimo era fatto. Avevo quantomeno quello che mi aspettavo. A quel punto il delirio di onnipotenza ha colpito, se potevo spostare il mio sforzo mentale dallo scrivere codice a inventare funzionalità potevo produrre molto di più di quanto avevo in mente all'inizio.
Quindi passando a Copilot di WebStorm ho cominciato a fare delle modifiche: 

- differenziare i settori (Extragalactic, Galactic Edge, Medium, Central Zone, Galactic Core) ognuno con densità e distribuzione dei tipi di stella più realistica
- più tipologie di pianeti rispetto agli otto delle tabelle originali
- una distribuzione statistica dei tipi di pianeti più scientificamente accurata
- aggiunta di dati relativi ai pianeti (diametro, massa, attrazione gravitazionale, goldilock)

Altra aggiunta rispetto all'idea iniziale sono state le immagini di pianeti e stelle. È bastato poco in effetti, in Antigravity mi sono fatto fare due file contenenti i prompt da dare in pasto ad un generatore di immagini e con l'MCP di Replicate ha generato le immagini, a quel punto è bastato dirgli dove e in che modo metterle sul frontend.

## Il cerchio si chiude

Alla fine il sistema era pronto. In questo progetto ho scritto pochissime righe di codice, più che altro ho fatto piccole correzioni quando mi veniva in mente qualcosa per il quale facevo prima a scriverlo direttamente che a chiederlo alla macchina. 
Ma non posso dire di non aver programmato, solo l'ho fatto in modo diverso. Anche perché nel progetto non c'è nulla che non avrei potuto fare da solo ma l'ho fatto in un quinto (forse un decimo) del tempo che ci avrei messo normalmente.  

C'è qualcosa di poetico nel fatto che quel codice del '96, nato in una notte di entusiasmo davanti a Access 2.0, abbia dovuto aspettare trent'anni per trovare la sua forma definitiva. Non è stato solo un processo di modernizzazione tecnologica: è stato come dare finalmente le gambe a un'idea che per tre decenni era rimasta chiusa in una cartella, spostata da computer a computer, aspettando il momento giusto. Gli strumenti di oggi - l'AI, gli agent di coding - non hanno fatto il lavoro al posto mio, mi hanno semplicemente permesso di concentrarmi su quello che volevo creare invece che su come costruirlo. Ed è esattamente quello che serviva per far rivivere quel vecchio generatore di universi.

È un fun project, un esperimento e un piccolo viaggio nel mio passato.

[Universe Generator](https://universe-generator-xi.vercel.app)