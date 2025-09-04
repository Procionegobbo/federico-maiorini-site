---
title: "Confronto tra ReadRune, ReadBytes, ReadString e ReadLine in Go"
date: 2025-08-18
tags: ["golang", "bufio", "io", "guide tecniche"]
categories: ["programmazione", "golang"]
description: "Tabella comparativa e diagramma di flusso per scegliere il metodo corretto di bufio.Reader in Go, con esempio pratico"
draft: false
image: bufioreader.jpeg
toc: true
---

# 📚 Confronto metodi di `bufio.Reader` in Go


## Introduzione

Recentemente sto studiando [Go](https://go.dev/), linguaggio interessante e per me è un ritorno (ho iniziato a programmare col C) ad un tipo di programmazione profondamente diversa da quella che ho praticato negli ultimi anni specializzandomi su PHP/Laravel.
Una delle cose che mi interessano è come leggere e scrivere da uno stream quindi, con l'aiuto di una IA mi sono fatto un veloce riepilogo delle differenze tra alcuni metodi della libreria `bufio`.

I metodi **`ReadRune`**, **`ReadBytes`**, **`ReadString`** e **`ReadLine`** sono molto simili ma solo in apparenza. 
Ecco una guida rapida per capire le differenze.

---

## Tabella comparativa

| Metodo | Firma | Cosa legge | Tipo restituito | Include `\n`? | Note pratiche |
|--------|-------|------------|-----------------|----------------|---------------|
| **ReadRune()** | `(r rune, size int, err error)` | **Un singolo carattere Unicode** (1 rune) | `rune` (+size+err) | N/A (legge solo 1 carattere) | Utile per analizzare caratteri uno alla volta (UTF-8 safe). |
| **ReadBytes(delim byte)** | `([]byte, error)` | Fino a `delim` incluso | `[]byte` | ✅ sì | Restituisce slice di byte, ottimo per parsing binario o testo grezzo. |
| **ReadString(delim byte)** | `(string, error)` | Fino a `delim` incluso | `string` | ✅ sì | Comodo se sai di leggere testo, meno efficiente di `ReadBytes`. |
| **ReadLine()** | `([]byte, isPrefix bool, error)` | Una riga (senza `\n`) | `[]byte` + `isPrefix` + `err` | ❌ no | Se la riga è troppo lunga, la restituisce a pezzi (`isPrefix = true`). Serve loop per ricomporla. Più basso livello. |

---

## 🔀 Diagramma di flusso decisionale

```text
                     ┌──────────────────────────────┐
                     │ Vuoi leggere 1 carattere?    │
                     └───────────────┬──────────────┘
                                     │
                           ┌─────────▼─────────┐
                           │ Usa ReadRune()    │
                           └───────────────────┘

                                     │
                                     ▼
                     ┌──────────────────────────────┐
                     │ Vuoi leggere fino a un       │
                     │ delimitatore (es. '\n')?     │
                     └───────────────┬──────────────┘
                                     │
                   ┌─────────────────┼─────────────────┐
                   │                 |                 │
        ┌──────────▼──────────┐      |      ┌──────────▼───────────┐
        │ Ti serve un []byte? │      |      │ Ti serve una stringa?│
        └──────────┬──────────┘      |      └───────────┬──────────┘
                   │                 |                  │
        ┌──────────▼──────────┐      |      ┌───────────▼───────────┐
        │ Usa ReadBytes()     │      |      │ Usa ReadString()      │
        └─────────────────────┘      |      └───────────────────────┘
                                     │
                                     │
                                     ▼
                     ┌──────────────────────────────┐
                     │ Devi gestire linee molto     │
                     │ lunghe (buffer a pezzi)?     │
                     └───────────────┬──────────────┘
                                     │
                           ┌─────────▼─────────┐
                           │ Usa ReadLine()    │
                           └───────────────────┘
```

## Esempio pratico

```go
package main

import (
	"bufio"
	"bytes"
	"fmt"
	"strings"
)

func main() {
	text := "café\nseconda linea\nterza linea senza newline finale"

	// --- ReadRune(): legge un singolo carattere Unicode alla volta ---
	fmt.Println("== ReadRune() ==")
	r := bufio.NewReader(strings.NewReader(text))
	for i := 0; i < 4; i++ { // leggo le prime 4 rune: c, a, f, é
		ru, size, err := r.ReadRune()
		if err != nil {
			fmt.Println("Errore ReadRune:", err)
			break
		}
		fmt.Printf("rune=%q size=%d\n", ru, size)
	}
	fmt.Println()

	// --- ReadBytes('\n'): legge fino al delimitatore incluso e restituisce []byte ---
	fmt.Println("== ReadBytes('\\n') ==")
	r = bufio.NewReader(strings.NewReader(text))
	b, err := r.ReadBytes('\n')
	if err != nil {
		fmt.Println("Errore ReadBytes:", err)
	}
	fmt.Printf("ReadBytes: %q (len=%d)\n", b, len(b))
	fmt.Println()

	// --- ReadString('\n'): stesso comportamento ma restituisce string ---
	fmt.Println("== ReadString('\\n') ==")
	r = bufio.NewReader(strings.NewReader(text))
	s, err := r.ReadString('\n')
	if err != nil {
		fmt.Println("Errore ReadString:", err)
	}
	fmt.Printf("ReadString: %q (len=%d)\n", s, len(s))
	fmt.Println()

	// --- ReadLine(): NON include '\n' e può restituire porzioni (isPrefix=true) ---
	// Forziamo una linea più lunga del buffer per vedere isPrefix=true.
	fmt.Println("== ReadLine() con buffer piccolo e isPrefix ==")
	longLine := "abcdefghij\n" // 10 caratteri + '\n'
	smallBuf := bufio.NewReaderSize(strings.NewReader(longLine), 8)

	var parts [][]byte
	for {
		line, isPrefix, err := smallBuf.ReadLine()
		if err != nil {
			// fine input o errore
			break
		}
		// Copia difensiva del frammento letto
		parts = append(parts, append([]byte(nil), line...))
		fmt.Printf("chunk=%q isPrefix=%v\n", line, isPrefix)
		if !isPrefix {
			break
		}
	}
	recombined := bytes.Join(parts, nil)
	fmt.Printf("Ricomposta: %q (pezzi=%d)\n", recombined, len(parts))
	fmt.Println()

	// --- Esempio classico di ReadLine su testo normale (senza superare il buffer) ---
	fmt.Println("== ReadLine() normale ==")
	r = bufio.NewReader(strings.NewReader(text))
	line, isPrefix, err := r.ReadLine()
	if err == nil {
		fmt.Printf("line=%q isPrefix=%v (niente '\\n')\n", line, isPrefix)
	}
}

```

## Conclusioni

### In sintesi veloce:

- `ReadRune` → analisi carattere-per-carattere, sicuro su UTF-8.
- `ReadBytes` → legge fino al delimitatore e restituisce `[]byte` (ottimo per parsing binario/grezzo).
- `ReadString` → come sopra ma restituisce string (più comodo, più allocazioni).
- `ReadLine` → non include `\n`, gestisce linee molto lunghe a pezzi con `isPrefix`.

### Insidie comuni da ricordare:

- Fine riga su Windows è `\r\n`: rimuovi il `\r` finale se leggi fino a `\n`.
- `bufio.Scanner` ha un limite di token (≈64 KB) che va aumentato per righe grandi.
- Le allocazioni: `ReadString` crea sempre una nuova stringa; con `ReadBytes` puoi restare su `[]byte` finché serve.

### Cosa usare quando:

- Parsing binario o attenzione alle allocazioni → `ReadBytes`.
- Input testuale “line-oriented” → `ReadString` (oppure Scanner).
- Analisi fine di rune (accenti/emoji) → `ReadRune`.
- Log/file con righe enormi → `ReadLine` (ricomponi quando `isPrefix` == true).