---
title: "spec-to-code: da pipeline a plugin, e il bug che ho quasi ignorato"
date: 2026-07-12
description: "Uso da mesi una pipeline di agenti Claude Code per portare una feature da idea a codice. Ci ho costruito Chimera Forge, un'API che genera koboldi e un bot Discord: l'ho impacchettata in un plugin installabile e, testandola per davvero su un progetto Go, ho trovato un bug che nessun controllo statico avrebbe mai visto."
categories: ["programmazione", "ai"]
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
  title: "spec-to-code: da pipeline a plugin, e il bug che ho quasi ignorato"
  description: "Uso da mesi una pipeline di agenti Claude Code per portare una feature da idea a codice. Ci ho costruito Chimera Forge, un'API che genera koboldi e un bot Discord: l'ho impacchettata in un plugin installabile e, testandola per davvero su un progetto Go, ho trovato un bug che nessun controllo statico avrebbe mai visto."
  author: "Federico Maiorini"
  type: "article"
---

Da qualche mese uso una pipeline di quattro agenti Claude Code per portare una feature da idea a codice implementato: `stories-init` crea lo spazio di lavoro, `spec-builder` espande un'idea grezza in una spec completa, `story-creator` la taglia in user story INVEST, `laravel-feature-builder` implementa una storia in Laravel. Non è un esperimento da weekend: ci ho costruito [Chimera Forge](https://chimera-forge.it), una spiritosa API che genera koboldi ([kaas.procionegobbo.it](https://kaas.procionegobbo.it)) e un bot Discord ([kichand.procionegobbo.it](https://kichand.procionegobbo.it)). È testata, funziona, e al momento soddisfa in pieno il mio modo di fare agentic coding.

Aveva però due limiti pratici. Aggiungere supporto per uno stack nuovo (Go, Python, quello che serve) era un copia-incolla-adatta manuale. E installare la pipeline in un altro repo significava copiare file a mano dentro `.claude/`. In una sessione di lavoro ho risolto entrambi i problemi, trovato e corretto un bug latente, e testato il tutto su un progetto Go vero. Qui c'è il resoconto, comprese le parti che non hanno funzionato al primo colpo.

## Una skill che costruisce agenti

La prima cosa che ho aggiunto è `create-feature-builder`, una skill che, eseguita dentro un repo qualsiasi, rileva lo stack dai file di configurazione (e chiede conferma), esplora il codice per capire il vero comando di test, il formatter, l'architettura e le feature già scritte come precedenti, e genera un agente `<stack>-feature-builder` su misura per quel repo.

L'ho fatta come skill e non come agente per un motivo preciso: una skill gira inline nella conversazione e può fermarsi a chiedere conferma sullo stack rilevato, un subagent gira in autonomia e non può chiedere niente. "Agenti che costruiscono agenti" suona come un trucco, ma nella pratica serve proprio perché il passaggio di conferma umana è quello che evita di generare un agente tarato sullo stack sbagliato.

L'idea di design che mi è piaciuta di più è la specializzazione a livelli. L'agente generato codifica come direttive autoritative le cose stabili, i comandi di test, formattazione, analisi statica, ma le cose volatili, come i percorsi delle cartelle o i file di esempio, le emette come "seed hint" datati, sotto un passaggio esplicito di "rileva, non assumere". Serve a evitare la trappola dell'agente generato che punta con sicurezza a percorsi che nel frattempo si sono spostati.

## Da copia-incolla a un comando

Il repo è diventato un plugin Claude Code (`spec-to-code`) e allo stesso tempo il suo marketplace (`my-agents`). L'installazione è passata da "copia questi file dentro `.claude/`" a:

```
/plugin marketplace add Procionegobbo/my-agents
/plugin install spec-to-code@my-agents
```

Versionato, aggiornabile con `/plugin update`, utilizzabile in ogni progetto senza toccare file a mano.

## Il bug che ho quasi liquidato con un "probabilmente va bene"

Questa è la parte che vale la pena raccontare per intero. Ho fatto revisionare il piano a un secondo modello Anthropic (Fable), che ha segnalato che il frontmatter YAML degli agenti sembrava rischioso. Il primo controllo, un parser YAML Python rigoroso, sembrava non essere d'accordo, e per un momento ho liquidato la cosa con un "probabilmente il runtime è più permissivo".

Poi ho lanciato `claude plugin validate`, lo strumento ufficiale, e il verdetto è stato chiaro: il campo `description` era uno scalare YAML non quotato che conteneva sequenze `": "`, che non fa il parsing e fa cadere silenziosamente tutto il frontmatter al momento del caricamento: nome, modello, tutto. Il bug era latente e riguardava tutti e quattro gli agenti. L'ho risolto quotando correttamente le descrizioni.

Colpa mia, avevo dato per scontato che la segnalazione dell'IDE sul frontmatter invalido dipendesse dal fatto che stavo editando il file di un agent e l'IDE non riconoscesse bene la sintassi. La revisione ha segnalato il problema e il validatore ufficiale lo ha dimostrato.

## Il test che ha trovato quello che i controlli statici non vedono

Dopo aver installato il plugin, l'ho lanciato su un progetto vero: RabbitLogger, un consumer Go che legge da RabbitMQ e scrive su Postgres. Sono emersi due problemi che nessuna validazione statica avrebbe mai potuto catturare.

`stories-init` ha allucinato lo stack. Un agente che si occupa solo di creare la cartella di lavoro, e che non ha nessun motivo per ispezionare lo stack tecnologico, si è offerto volontario, sbagliando, di indovinare linguaggio e natura del progetto, chiamando un repo Go un "progetto Python RabbitMQ logger". Il nome del repo, RabbitLogger, quasi certamente ha seminato l'ipotesi sbagliata. L'ho risolto vincolando l'agente al suo compito reale.

Il secondo problema era una guida ridondante e contraddittoria nel passaggio di implementazione dell'agente generato: due liste sovrapposte di cose a cui fare attenzione, una generica e una specifica per lo stack, che in un punto si contraddicevano: "applica l'autorizzazione per ogni azione" nella lista generica contro "autorizzazione: non applicabile" in quella specifica per Go. L'ho risolto rendendo le note specifiche per lo stack l'unica fonte di verità.

La parte che invece ha funzionato bene: il `go-feature-builder` generato era accurato. Comandi corretti (`go test ./...`, `gofmt`, `go vet`), percorsi reali `internal/…` come hint datati, riconoscimento corretto dell'assenza di frontend e di un layer di autenticazione ("non inventarne uno"), e idiomi Go genuini (query parametrizzate, graceful shutdown, `fmt.Errorf("…: %w")`) senza traccia di vocabolario Laravel.

Tre release piccole nella stessa sessione, ognuna per un problema trovato usando lo strumento sul serio: v3.0.0 con plugin, marketplace, skill e il fix del frontmatter; v3.0.1 con `stories-init` che non indovina più lo stack; v3.0.2 con la lista di concern contraddittoria rimossa. Tre PR, ognuna validata con `claude plugin validate` prima del merge.

## Cosa mi porto a casa

Il plugin aveva passato la validazione statica già alla v3.0.0. È stato il primo run vero su un repo Go a far emergere l'allucinazione e la contraddizione. Nessuna delle due cose sarebbe saltata fuori leggendo lo YAML o eseguendo il validatore. La validazione statica ti dice che lo strumento è ben formato; solo usarlo per davvero ti dice se fa quello che deve fare.

Vale anche per la mia pipeline in generale: l'ho già usata per costruire Chimera Forge, l'API dei koboldi e il bot Discord, e proprio per questo mi fido di dove è solida. È anche per questo che ho notato subito quando qualcosa non tornava nel nuovo run su Go.

Una precisazione, per restare onesto sui confini di quello che ho effettivamente verificato: il `go-feature-builder` generato l'ho revisionato e confermato corretto e valido, ma non l'ho ancora usato per implementare una feature reale su quel progetto: il ciclo completo, dalla spec alle storie fino al codice, su Go non è ancora stato esercitato end-to-end. "Ho generato un agente corretto e su misura per il repo" è l'affermazione giusta, "ho costruito una feature Go" non lo sarebbe.

---

### Il codice è su [github.com/Procionegobbo/my-agents](https://github.com/Procionegobbo/my-agents)
