---
title: "Testare le GitHub Actions in locale con act"
date: 2025-08-28
description: "Come testare le GitHub Actions in locale utilizzando act per velocizzare il debugging dei workflow, ottimizzare il ciclo di sviluppo e ridurre i tempi di attesa."
tags:
  - GitHubActions
  - ACT
  - CI/CD
  - DevOps
  - Automation
categories: ["programmazione", "devops"]
image: "act.jpg"
featured_image: "act.jpg"
slug: "testare-github-actions-in-locale-act"
toc: true
draft: false

# Open Graph / LinkedIn / Twitter meta
images:
  - "act.jpg"
ogTitle: "Testare le GitHub Actions in locale con act"
ogDescription: "Scopri come usare act per testare e debuggare le GitHub Actions in locale, accelerando il ciclo di sviluppo e risolvendo i problemi più velocemente."
twitterTitle: "Testare le GitHub Actions in locale con act"
twitterDescription: "Come testare e debuggare le GitHub Actions localmente usando act, per velocizzare il debugging e ottimizzare il ciclo di sviluppo."
---


Chi usa GitHub prima o poi si scontra con i workflow. Di recente stiamo affrontando una sfida solo all'apparenza banale: migrare alcuni dei nostri repo su Github e implementare le actions necessarie alle necessità di CI/CD.

Di base sarebbe banale, in rete ci sono gazilioni di esempi, template, guide e perfino wizard che, in teoria, ti forniscono gli script già pronti.

Migrando uno degli ultimi repo però mi è successa una cosa particolare. Stavo usando per il workflow da eseguire sulle pull-request lo stesso script usato con successo in altri repo (sono tutti sistemi basati su Laravel). Questa volta però non andava, errori di connessione al db, test che fallivano in maniera inaspettata.

Tentavo le correzioni, push su GitHub, interminabile attesa che il workflow girasse per esaminare gli errori.

Un modo mooolto lento di procedere.

## Installare e usare act per testare le GitHub Actions

Per fortuna c'è un'alternativa: [**act** - https://nektosact.com/](https://nektosact.com/)
questa fantastica utility scritta in Go permette di eseguire le actions di GitHub in locale grazie alla creazione al volo di una serie di container (nel mio caso uso [Podman](https://podman.io/) invece di Docker).

L'installazione è banale, nel mio caso su Mac

```shell
brew install act
```

Dopodiché basta avere il servizio Docker (o Podman) attivo e lanciare l'utility.

Ecco un esempio completo di comando, con tutti i parametri che uso nel mio ambiente:

```shell
act \
  --workflows ".github/workflows/main.yml" \
  --secret-file .secrets \
  --var-file .vars \
  --pull=false \
  --container-architecture linux/arm64 \
  -P ubuntu-latest=catthehacker/ubuntu:act-latest \
  -P self-hosted=catthehacker/ubuntu:act-latest
```

## Configurare act: i parametri principali

Vi spiego i vari parametri:

| Parametro                  | Descrizione                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| `--workflows`             | Path del file `.yml` del workflow da eseguire                                |
| `--secret-file`           | Variabili **SECRET** in formato `NOME=valore` (una per riga)                 |
| `--var-file`              | Variabili **VARIABLE** in formato `NOME=valore` (una per riga)               |
| `--pull`                  | Se `false`, evita di scaricare ogni volta l’immagine del container           |
| `--container-architecture`| Architettura da usare per i container (es. `linux/arm64`)                     |
| `-P`                      | Specifica l’immagine da usare per il container che eseguirà il workflow      |

Nel mio caso per il container ho scelto `catthehacker/ubuntu:act-latest` rispetto a `catthehacker/ubuntu:full-latest` perché quest'ultima, anche se ha la massima compatibilità integrando praticamente tutti i tool necessari, è enorme (60Gb una volta estratta) e non era necessaria.


## Conclusioni: perché usare act

Utilizzare `act` mi ha permesso di testare molto più velocemente il workflow, individuare i problemi e correggerlo in una frazione del tempo rispetto al classico 
`edit->commit->push->execute action->repeat`

Un'ultima cosa. Una volta messo a punto il workflow, girava perfettamente su act, è successo che alcuni test fallissero una volta che il workflow veniva eseguito su GitHub. La spiegazione è tanto banale quanto insidiosa: `act`, ma anche un banale `php artisan test` useranno il vostro file `.env` se presente. Tenetene conto quando scrivete il workflow.

> **Nota importante ⚠️**  
> `act` utilizza il file `.env` locale per eseguire i test, mentre GitHub Actions potrebbe avere un contesto diverso.  
> Assicurati di configurare correttamente le variabili d’ambiente nel workflow per evitare comportamenti inattesi.


## Link utili

- [Documentazione ufficiale di act](https://nektosact.com/)
- [Documentazione ufficiale GitHub Actions](https://docs.github.com/en/actions)
