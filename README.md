# federico-maiorini-site

![ProcionegobboLogoHi.png](ProcionegobboLogoHi.png) Questo repository contiene il sito personale di Federico Maiorini, realizzato con Hugo.

## Migrazione tema
Il sito è stato migrato dal tema Stack al tema Hugo standard Ananke, mantenendo URL, contenuti e funzionalità custom.

## Checklist e validazione
Sono disponibili checklist di validazione in `specs/001-theme-migration/checklists/` per:
- Responsive
- Navigazione/core features
- Switch lingua
- HTML validation

## Struttura del progetto

- `content/` — Contenuti del sito suddivisi per lingua e categoria
- `layouts/` — Template e partials personalizzati
- `static/` — File statici (immagini, favicon, ecc.)
- `themes/` — Tema Hugo utilizzato
- `config.toml` / `config.yaml` — Configurazione del sito

## Comandi principali

- Avvio server locale:
  ```sh
  hugo server
  ```
- Build del sito statico:
  ```sh
  hugo build
  ```

## Note

- Per visualizzare il sito in locale, usare `hugo server`.
- Per generare la versione statica, usare `hugo build`.
- I contenuti sono organizzati per lingua (`it`, `en`) e per categoria (blog, gdr, scrittura, ecc.).

## Autore

Federico Maiorini

## Sito pubblico

Il sito è online all'indirizzo: [https://procionegobbo.it](https://procionegobbo.it)

## Copyright e proprietà dei contenuti

Tutti i contenuti presenti in questo sito (principalmente nelle cartelle `content` e `public`) sono di proprietà di Federico Maiorini e non sono riproducibili, copiati o distribuiti senza esplicita autorizzazione, salvo diversa indicazione riportata nei singoli contenuti.
