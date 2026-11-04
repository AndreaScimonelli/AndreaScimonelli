# Survey IBPA 2026/2027 – End User Grandi e grandissime imprese: file per Qualtrics

Fonte: `Survey_IBPA_2026-2027_EndUser_Grandi_FINALE_v4.docx`

## File

| File | A cosa serve |
|---|---|
| `Survey_IBPA_2026-2027_EndUser_Grandi.qsf` | Il questionario da importare in Qualtrics, con blocchi, survey flow, branch e display logic |
| `build_qsf.py` | Script che genera il QSF dai testi del Word: serve a rigenerarlo dopo eventuali modifiche |
| `LEGGIMI.md` | Questo documento |

## Come importare

Qualtrics → **Crea nuovo progetto** → **Sondaggio** → *Come vuoi iniziare?* → **Importa un file QSF** → seleziona il file `.qsf` → **Crea progetto**.
In inglese: *Create new project → Survey → Import a QSF file*.

Il QSF è un JSON con la stessa struttura dei file esportati da Qualtrics. L'import non l'ho potuto provare su Qualtrics; ho controllato la struttura su export reali e ho simulato il survey flow con 30.000 rispondenti casuali. In tutti i casi il percorso coincide con le note operative del Word. Prima di distribuire la survey, fai comunque i controlli della checklist qui sotto.

## Come sono implementati i filtri del Word

| Filtro nel Word | Implementazione in Qualtrics |
|---|---|
| 1.6 = Public Administration → esce | Branch nel survey flow → `screen_out = "Public Administration"` → Fine survey |
| 1.7 = Fino a 49 dipendenti → esce | Branch → `screen_out = "Fino a 49 dipendenti"` → Fine survey |
| 2.4 solo se alla 2.3, riga 1, non ha risposto «No» | Display logic sulla 2.4 |
| 3.3 e 3.4 non mostrate a chi ha risposto d) alla 3.1 | Display logic su 3.3, 3.4A, 3.4B |
| Sezione 5 saltata da chi ha 3.1 = d) **e** 4.1 = h) | Branch «adopter»: 3.1 d) non selezionata **oppure** 4.1 h) non selezionata |
| 5.2: solo le famiglie con almeno una delle prime tre colonne alla 5.1; se ne resta una sola si salta la 5.2 e si mostra direttamente la matrice; se nessuna si passa alla sezione 6 | Embedded data `elig_AFC`, `elig_ACQ`, `elig_OPS`, `elig_CS` (1 = famiglia selezionabile) ed `elig_pattern`. La 5.2 compare solo se le famiglie selezionabili sono almeno 2, e mostra solo quelle. Ogni matrice 5.3 compare se la famiglia è scelta alla 5.2 oppure se era l'unica selezionabile |
| 6.2 non mostrata a chi ha risposto a), b) o c) alla 6.1 | Display logic sulla 6.2 |
| 7.1 a tutti; 7.2–7.6 saltate da chi ha 3.1 = d) e 4.1 = h) | Blocco 7.1 fuori dai branch; blocco 7.2–7.6 nel branch «adopter» |
| 7.3 solo se 7.2 = b), c) o d) | Display logic |
| 7.4 non mostrata a chi alla 7.3 ha risposto a) | Display logic «7.3 a) non selezionata». Quindi la vede anche chi non ha visto la 7.3 |
| 7.5 solo se 7.2 = da f) a i) | Display logic |
| Sezione 8 saltata da chi ha 3.1 = d) e 4.1 = h) | Nel branch «adopter», dopo il blocco 7.2–7.6 |
| 8.2 solo se 8.1 = a) o b) | Display logic |
| Sezione 9 saltata da chi ha 3.1 = d) oppure non ha selezionato alla 5.1 alcuna casella nelle colonne «Automazione intelligente» e «Agenti AI autonomi» | Due branch annidati: 3.1 d) non selezionata → almeno una delle 22 caselle (11 righe × 2 colonne) selezionata |
| 9.2 solo se alla 9.1 almeno una riga è «peggio» o «molto peggio del previsto» | Display logic (14 condizioni in OR) |
| 10.3 e 10.4 solo se 10.2 = da b) a i) | Branch sul blocco 10.3–10.4 |
| 10.6 non mostrata a chi risponde d) o e) alla 10.5 | Display logic «10.5 = a), b) o c)» su 10.6a e 10.6b |

## Scelte di programmazione da conoscere

1. **10.1, barriere**: la tabella 17 × 3 è diventata **tre domande a risposta multipla**, una per pagina: automazione tradizionale, intelligente, agentica. In questo modo Qualtrics applica da solo il limite di 3 barriere per colonna e l'esclusività di «Nessuna barriera rilevante». Nella domanda sull'automazione tradizionale non compaiono le righe 15 («Affidabilità e prevedibilità degli output…») e 16 («Assenza di responsabilità chiare…»), come chiede la nota («disattivare la prima colonna»). I codici delle opzioni coincidono con il numero di riga del Word (1–17) e sono uguali nelle tre domande, quindi il confronto per colonna con la serie storica resta immediato.
2. **10.3 e 10.6**: ogni riga della tabella è una domanda a risposta singola (`Q10.3a`/`Q10.3b`, `Q10.6a`/`Q10.6b`), perché le etichette cambiano da riga a riga. «Non so» e «Non applicabile» sono l'ultima opzione. Per la regola «compili almeno una delle due righe»: chi alla riga in euro sceglie «Non applicabile» non trova «Non applicabile» nella riga FTE, quindi deve indicare una fascia. Per questo 10.6a e 10.6b stanno su due pagine.
3. **10.4**: in alto c'è la casella «Non siamo in grado di stimare la ripartizione» (`Q10.4_ns`), sotto il campo percentuali a somma costante con totale 100 (`Q10.4`). Se si spunta la casella, il campo percentuali scompare. La casella sta sopra i campi perché Qualtrics nasconde una domanda solo in base a una domanda che la precede sulla stessa pagina.
4. **3.4**: è divisa in due domande (`Q3.4A`, `Q3.4B`) sulla stessa pagina.
5. **Obbligatorietà**: il Word non la indica, salvo «Facoltativo» per 5.2 e 5.3. Ho reso obbligatorie tutte le altre domande (*Force response*). Facoltative restano la 5.2, le 5.3 e la casella della 10.4.
6. **Opzioni esclusive**: 4.1 h), 7.3 h), 8.1 f), 10.1 «Nessuna barriera rilevante», le ultime due colonne della 5.1. Ho aggiunto io l'esclusività di 6.2 k), «Non ho abbastanza informazioni per rispondere», che il Word non indica.
7. **Randomizzazione**: 4.1 da a) a g), con h) sempre in fondo; righe della 5.1.
8. **Testi**: i numeri di domanda non compaiono al rispondente, perché con i filtri salterebbero (per esempio da 3.1 a 4.1). Sono negli *export tag* (`Q1.1` … `Q10.7`), visibili nell'editor e nel dataset. All'inizio di ogni sezione compare il titolo. Le note operative (riquadri gialli) non sono visibili al rispondente. I riquadri grigi sì: definizione di Process Automation, introduzione alla sezione 5, esempi della 8.1, introduzione alla sezione 9. La nota su BPMN/swimlane/SIPOC compare sotto la 2.3.
9. **1.5 «JT»** è diventato «Job title:».
10. **Precompilazione**: Nome, Cognome ed E-mail si precompilano con i dati del contatto (`${m://FirstName}`, `${m://LastName}`, `${m://Email1}`) quando la survey è inviata dalle liste contatti di Qualtrics. Con il link anonimo restano vuoti. Il rispondente può modificarli. L'e-mail ha la validazione di formato.
11. **Screen-out**: i rispondenti esclusi restano nel dataset con la variabile `screen_out` valorizzata, così puoi filtrarli.

### Variabili aggiuntive nel dataset (embedded data)

- `screen_out`: «Public Administration» o «Fino a 49 dipendenti». Vuota per chi prosegue.
- `elig_AFC`, `elig_ACQ`, `elig_OPS`, `elig_CS`: 1 se alla 5.1 la famiglia (Amministrazione/finanza, Acquisti, Operations, Customer service) ha almeno una delle prime tre colonne.
- `elig_pattern`: concatenazione dei quattro flag (per esempio `P1010`), usata dalla logica 5.2/5.3.

## Da controllare dopo l'import (circa 10 minuti)

1. **Anteprima dei percorsi principali**:
   - a) settore «Public Administration» → la survey termina subito;
   - b) 3.1 «Non applichiamo la Process Automation» + 4.1 «Nessuno di questi» → dalla 4.1 si passa alla 6.1, poi 7.1 e sezione 10 (senza 5, 7.2–7.6, 8 e 9);
   - c) azienda che automatizza almeno due famiglie tra Amministrazione, Acquisti, Operations e Customer service → compaiono la 5.2 (solo con quelle famiglie) e le matrici 5.3 scelte;
   - d) una sola di queste famiglie automatizzata → niente 5.2, compare direttamente la sua matrice 5.3.
2. **Limiti sul numero di scelte**: in 5.2 (max 2), 7.5 (max 2), 8.2 (max 3), 10.1a/b/c (max 3) e 10.7 (max 3) controlla che ci sia la validazione *Answers range / Intervallo risposte*. Se manca: *Requisiti di risposta → Aggiungi validazione → Intervallo risposte*.
3. **10.4**: controlla che la somma costante abbia *Must total = 100*. Prova anche che spuntando «Non siamo in grado…» il campo percentuali scompaia.
4. **Messaggio di fine survey**: il Word chiude con «Fine del questionario. La ringraziamo per il tempo dedicato.». Impostalo come messaggio personalizzato in *Opzioni sondaggio → Fine del sondaggio*. Se vuoi un messaggio diverso per gli screen-out, impostalo negli elementi *Fine sondaggio* dei due branch iniziali del survey flow.
5. **Informativa privacy / benvenuto**: nel Word non c'è. Se serve, aggiungila nel primo blocco, prima dei dati anagrafici.
6. **Opzioni sondaggio impostate**: pulsante Indietro attivo; *Save & continue* attivo; barra di avanzamento senza testo; risposte parziali chiuse dopo 1 settimana (per una survey B2B di 22 minuti valuta 2 settimane o più); accesso pubblico (valuta *Solo su invito* se distribuisci solo alle liste contatti); tema grafico = quello predefinito del vostro account.

## Punti aperti e incongruenze nel Word (da decidere con il team)

1. **Chi risponde d) alla 3.1.** La nota sotto la 3.1 dice che chi risponde d) salta le sezioni 5, 7, 8 e 9. Le note di sezione (4, 5, 7 e 8) fanno invece saltare 5, 7.2–7.6 e 8 solo a chi ha **3.1 = d) e 4.1 = h)**, il «doppio controllo sulla 3.1». **Ho seguito le note di sezione**: chi dichiara di non applicare la Process Automation ma indica almeno uno strumento alla 4.1 vede le sezioni 5, 7 e 8. Non vede la 9, che si filtra sulla sola 3.1 = d). Per applicare invece la regola della 3.1, nei due branch «adopter» del survey flow va tolta la condizione su Q4.1.
2. **3.2.** Nel Word non ha filtri, quindi la vedono tutti, anche chi risponde d) alla 3.1. Leggendo la nota della 3.1 («prosegue dalla Sezione 4») si potrebbe pensare il contrario.
3. **2.3.** La nota dice che l'ultima riga è l'inventario dei bot e dei flussi in esercizio. L'ultima riga attuale però è «Un repository centrale di processi, procedure e linee guida operative». O manca una riga o la nota è da aggiornare.
4. **1.7.** «Da 250 a 999» e «Oltre 1.000» lasciano scoperto il valore esatto di 1.000 dipendenti. Inoltre lo screen-out esclude solo le aziende fino a 49 dipendenti, quindi entrano anche le medie (50–249) anche se il questionario è per le grandi imprese. Da confermare.
5. **Commenti ancora aperti nel Word, non applicati**:
   - 10.2: «Aggiungiamo: non si consideri spesa per personale interno dedicato» (Irene Di Deo, 29/10);
   - 5.1: dubbio se togliere la riga «Strategia, governance e organizzazione»;
   - 10.1: «tabellona troppo pesante». Ora è già su tre pagine, vedi scelta 1. La versione «per differenza» rispetto alle barriere dell'automazione tradizionale non è implementata.
6. Il Word conta 38 domande. In Qualtrics le domande sono 47 per le suddivisioni descritte sopra (3.4, 5.3, 10.1, 10.3, 10.4, 10.6), più 5 testi descrittivi.

## Appendice – Mappa di blocchi, pagine e logiche (generata dal QSF)

- 🏷️ Embedded data: `elig_AFC` = `0`, `elig_ACQ` = `0`, `elig_OPS` = `0`, `elig_CS` = `0`
- 📦 **Blocco «S1 - Anagrafica»**
  - Pagina 1:
    - **INTRO** — testo descrittivo
    - **Q1.1** — testo (obbligatoria)
    - **Q1.2** — testo (obbligatoria)
    - **Q1.3** — testo (obbligatoria; formato e-mail)
    - **Q1.4** — testo (obbligatoria)
    - **Q1.5** — testo (obbligatoria)
  - Pagina 2:
    - **Q1.6** — scelta singola (obbligatoria)
    - **Q1.7** — scelta singola (obbligatoria)
- 🔀 **Branch** — prosegue nel ramo solo se: Q1.6 q) «Public Administration» selezionata
  - 🏷️ Embedded data: `screen_out` = `Public Administration`
  - ⛔ **Fine survey** (screen-out)
- 🔀 **Branch** — prosegue nel ramo solo se: Q1.7 a) «Fino a 49 dipendenti» selezionata
  - 🏷️ Embedded data: `screen_out` = `Fino a 49 dipendenti`
  - ⛔ **Fine survey** (screen-out)
- 📦 **Blocco «S2 - Maturità digitale e gestione per processi»**
  - Pagina 1:
    - **Q2.1** — scelta singola (obbligatoria)
    - **Q2.2** — scelta singola (obbligatoria)
  - Pagina 2:
    - **Q2.3** — matrice una risposta per riga (obbligatoria)
    - **Q2.3_NOTA** — testo descrittivo
  - Pagina 3:
    - **Q2.4** — scelta singola (obbligatoria)
      - *Mostrata se:* Q2.3 riga 1 «Un inventario o mappa dei processi aziendali » → colonna «No» NON selezionata
- 📦 **Blocco «S3 - Approccio alla Process Automation»**
  - Pagina 1:
    - **S3_DEF** — testo descrittivo
    - **Q3.1** — scelta singola (obbligatoria)
  - Pagina 2:
    - **Q3.2** — matrice una risposta per riga (obbligatoria)
    - **Q3.3** — scelta singola (obbligatoria)
      - *Mostrata se:* Q3.1 d) «Non applichiamo la Process Automation.» NON selezionata
  - Pagina 3:
    - **Q3.4A** — scelta singola (obbligatoria)
      - *Mostrata se:* Q3.1 d) «Non applichiamo la Process Automation.» NON selezionata
    - **Q3.4B** — scelta singola (obbligatoria)
      - *Mostrata se:* Q3.1 d) «Non applichiamo la Process Automation.» NON selezionata
- 📦 **Blocco «S4 - Tecnologie di automazione»**
  - Pagina 1:
    - **Q4.1** — scelta multipla (obbligatoria; ordine casuale (ultima fissa); esclusiva: h))
- 🔀 **Branch** — prosegue nel ramo solo se: Q3.1 d) «Non applichiamo la Process Automation.» NON selezionata **OPPURE** Q4.1 h) «Nessuno di questi» NON selezionata
  - 📦 **Blocco «S5 - Mappatura processi (5.1)»**
    - Pagina 1:
      - **S5_INTRO** — testo descrittivo
      - **Q5.1** — matrice risposta multipla (obbligatoria; ordine casuale delle righe; esclusiva: col. «Nessuna automazione», col. «Non applicabile»)
  - 🏷️ Embedded data: `elig_AFC` = `0`, `elig_ACQ` = `0`, `elig_OPS` = `0`, `elig_CS` = `0`
  - 🔀 **Branch** — prosegue nel ramo solo se: Q5.1 riga 8 «Amministrazione, finanza e controllo (contabi» → colonna «Automazione tradizionale» selezionata **OPPURE** Q5.1 riga 8 «Amministrazione, finanza e controllo (contabi» → colonna «Automazione intelligente (AI)» selezionata **OPPURE** Q5.1 riga 8 «Amministrazione, finanza e controllo (contabi» → colonna «Agenti AI autonomi» selezionata
    - 🏷️ Embedded data: `elig_AFC` = `1`
  - 🔀 **Branch** — prosegue nel ramo solo se: Q5.1 riga 5 «Acquisti e gestione dei fornitori (strategie » → colonna «Automazione tradizionale» selezionata **OPPURE** Q5.1 riga 5 «Acquisti e gestione dei fornitori (strategie » → colonna «Automazione intelligente (AI)» selezionata **OPPURE** Q5.1 riga 5 «Acquisti e gestione dei fornitori (strategie » → colonna «Agenti AI autonomi» selezionata
    - 🏷️ Embedded data: `elig_ACQ` = `1`
  - 🔀 **Branch** — prosegue nel ramo solo se: Q5.1 riga 6 «Operations, produzione, logistica e fulfillme» → colonna «Automazione tradizionale» selezionata **OPPURE** Q5.1 riga 6 «Operations, produzione, logistica e fulfillme» → colonna «Automazione intelligente (AI)» selezionata **OPPURE** Q5.1 riga 6 «Operations, produzione, logistica e fulfillme» → colonna «Agenti AI autonomi» selezionata
    - 🏷️ Embedded data: `elig_OPS` = `1`
  - 🔀 **Branch** — prosegue nel ramo solo se: Q5.1 riga 7 «Customer service e gestione della relazione c» → colonna «Automazione tradizionale» selezionata **OPPURE** Q5.1 riga 7 «Customer service e gestione della relazione c» → colonna «Automazione intelligente (AI)» selezionata **OPPURE** Q5.1 riga 7 «Customer service e gestione della relazione c» → colonna «Agenti AI autonomi» selezionata
    - 🏷️ Embedded data: `elig_CS` = `1`
  - 🏷️ Embedded data: `elig_pattern` = `P${e://Field/elig_AFC}${e://Field/elig_ACQ}${e://Field/elig_OPS}${e://Field/elig_CS}`
  - 📦 **Blocco «S5 - Approfondimento famiglie (5.2-5.3)»**
    - Pagina 1:
      - **Q5.2** — scelta multipla (facoltativa; max 2 scelte)
        - *Mostrata se:* embedded `elig_pattern` ≠ `P0000` **E** embedded `elig_pattern` ≠ `P1000` **E** embedded `elig_pattern` ≠ `P0100` **E** embedded `elig_pattern` ≠ `P0010` **E** embedded `elig_pattern` ≠ `P0001`
        - *Opzione a) «Amministrazione, finanza e controllo» visibile se:* embedded `elig_AFC` = `1`
        - *Opzione b) «Acquisti e gestione dei fornitori» visibile se:* embedded `elig_ACQ` = `1`
        - *Opzione c) «Operations, produzione, logistica e fulfillment» visibile se:* embedded `elig_OPS` = `1`
        - *Opzione d) «Customer service e gestione della relazione con il» visibile se:* embedded `elig_CS` = `1`
    - Pagina 2:
      - **Q5.3a** — matrice una risposta per riga (facoltativa)
        - *Mostrata se:* Q5.2 a) «Amministrazione, finanza e controllo» selezionata **OPPURE** embedded `elig_pattern` = `P1000`
    - Pagina 3:
      - **Q5.3b** — matrice una risposta per riga (facoltativa)
        - *Mostrata se:* Q5.2 b) «Acquisti e gestione dei fornitori» selezionata **OPPURE** embedded `elig_pattern` = `P0100`
    - Pagina 4:
      - **Q5.3c** — matrice una risposta per riga (facoltativa)
        - *Mostrata se:* Q5.2 c) «Operations, produzione, logistica e fulfillment» selezionata **OPPURE** embedded `elig_pattern` = `P0010`
    - Pagina 5:
      - **Q5.3d** — matrice una risposta per riga (facoltativa)
        - *Mostrata se:* Q5.2 d) «Customer service e gestione della relazione con il cliente» selezionata **OPPURE** embedded `elig_pattern` = `P0001`
- 📦 **Blocco «S6 - Agentic Automation»**
  - Pagina 1:
    - **Q6.1** — scelta singola (obbligatoria)
  - Pagina 2:
    - **Q6.2** — scelta multipla (obbligatoria; esclusiva: k))
      - *Mostrata se:* Q6.1 a) «Non ho mai sentito il termine.» NON selezionata **E** Q6.1 b) «Conosco personalmente il tema, ma non è mai stato discusso i» NON selezionata **E** Q6.1 c) «Abbiamo discusso del tema in azienda, ma non abbiamo ancora » NON selezionata
- 📦 **Blocco «S7 - Organizzazione e competenze (7.1, tutti)»**
  - Pagina 1:
    - **Q7.1** — scelta singola (obbligatoria)
- 🔀 **Branch** — prosegue nel ramo solo se: Q3.1 d) «Non applichiamo la Process Automation.» NON selezionata **OPPURE** Q4.1 h) «Nessuno di questi» NON selezionata
  - 📦 **Blocco «S7 - Organizzazione e competenze (7.2-7.6)»**
    - Pagina 1:
      - **Q7.2** — scelta singola (obbligatoria)
    - Pagina 2:
      - **Q7.3** — scelta multipla (obbligatoria; esclusiva: h))
        - *Mostrata se:* Q7.2 b) «Esistono due presidi distinti, che lavorano su iniziative co» selezionata **OPPURE** Q7.2 c) «Esistono due presidi distinti, che si coordinano caso per ca» selezionata **OPPURE** Q7.2 d) «Esistono due presidi distinti, che operano in modo sostanzia» selezionata
    - Pagina 3:
      - **Q7.4** — scelta singola (obbligatoria)
        - *Mostrata se:* Q7.3 a) «Un budget unico per i due presidi» NON selezionata
    - Pagina 4:
      - **Q7.5** — scelta multipla (obbligatoria; max 2 scelte)
        - *Mostrata se:* Q7.2 f) «Esiste un presidio sull’AI, ma non sull’automazione dei proc» selezionata **OPPURE** Q7.2 g) «Non abbiamo un team dedicato: le competenze sono distribuite» selezionata **OPPURE** Q7.2 h) «Non abbiamo competenze interne dedicate: ci affidiamo a forn» selezionata **OPPURE** Q7.2 i) «Non esiste alcun presidio strutturato sull’automazione e AI» selezionata
    - Pagina 5:
      - **Q7.6** — scelta singola (obbligatoria)
  - 📦 **Blocco «S8 - Esternalizzazione»**
    - Pagina 1:
      - **Q8.1** — scelta multipla (obbligatoria; esclusiva: f))
    - Pagina 2:
      - **Q8.2** — scelta multipla (obbligatoria; max 3 scelte)
        - *Mostrata se:* Q8.1 a) «Abbiamo riportato completamente all’interno alcune attività » selezionata **OPPURE** Q8.1 b) «Abbiamo parzialmente ridotto il ricorso a fornitori esterni,» selezionata
- 🔀 **Branch** — prosegue nel ramo solo se: Q3.1 d) «Non applichiamo la Process Automation.» NON selezionata
  - 🔀 **Branch** — prosegue nel ramo solo se: Q5.1 riga 1 «Strategia, governance e organizzazione (piani» → colonna «Automazione intelligente (AI)» selezionata **OPPURE** Q5.1 riga 1 «Strategia, governance e organizzazione (piani» → colonna «Agenti AI autonomi» selezionata **OPPURE** Q5.1 riga 2 «Risorse umane e sviluppo delle persone (selez» → colonna «Automazione intelligente (AI)» selezionata **OPPURE** Q5.1 riga 2 «Risorse umane e sviluppo delle persone (selez» → colonna «Agenti AI autonomi» selezionata **OPPURE** Q5.1 riga 3 «Ricerca, sviluppo e innovazione dell’offerta » → colonna «Automazione intelligente (AI)» selezionata **OPPURE** Q5.1 riga 3 «Ricerca, sviluppo e innovazione dell’offerta » → colonna «Agenti AI autonomi» selezionata **OPPURE** Q5.1 riga 4 «Marketing, vendite e canali commerciali (anal» → colonna «Automazione intelligente (AI)» selezionata **OPPURE** Q5.1 riga 4 «Marketing, vendite e canali commerciali (anal» → colonna «Agenti AI autonomi» selezionata **OPPURE** Q5.1 riga 5 «Acquisti e gestione dei fornitori (strategie » → colonna «Automazione intelligente (AI)» selezionata **OPPURE** Q5.1 riga 5 «Acquisti e gestione dei fornitori (strategie » → colonna «Agenti AI autonomi» selezionata **OPPURE** Q5.1 riga 6 «Operations, produzione, logistica e fulfillme» → colonna «Automazione intelligente (AI)» selezionata **OPPURE** Q5.1 riga 6 «Operations, produzione, logistica e fulfillme» → colonna «Agenti AI autonomi» selezionata **OPPURE** Q5.1 riga 7 «Customer service e gestione della relazione c» → colonna «Automazione intelligente (AI)» selezionata **OPPURE** Q5.1 riga 7 «Customer service e gestione della relazione c» → colonna «Agenti AI autonomi» selezionata **OPPURE** Q5.1 riga 8 «Amministrazione, finanza e controllo (contabi» → colonna «Automazione intelligente (AI)» selezionata **OPPURE** Q5.1 riga 8 «Amministrazione, finanza e controllo (contabi» → colonna «Agenti AI autonomi» selezionata **OPPURE** Q5.1 riga 9 «Legal, contrattualistica e gestione degli ass» → colonna «Automazione intelligente (AI)» selezionata **OPPURE** Q5.1 riga 9 «Legal, contrattualistica e gestione degli ass» → colonna «Agenti AI autonomi» selezionata **OPPURE** Q5.1 riga 10 «IT, dati e cybersecurity (strategia e archite» → colonna «Automazione intelligente (AI)» selezionata **OPPURE** Q5.1 riga 10 «IT, dati e cybersecurity (strategia e archite» → colonna «Agenti AI autonomi» selezionata **OPPURE** Q5.1 riga 11 «Risk management, compliance e sostenibilità (» → colonna «Automazione intelligente (AI)» selezionata **OPPURE** Q5.1 riga 11 «Risk management, compliance e sostenibilità (» → colonna «Agenti AI autonomi» selezionata
    - 📦 **Blocco «S9 - Aspettative e risultati»**
      - Pagina 1:
        - **S9_INTRO** — testo descrittivo
        - **Q9.1** — matrice una risposta per riga (obbligatoria)
      - Pagina 2:
        - **Q9.2** — scelta singola (obbligatoria)
          - *Mostrata se:* Q9.1 riga 1 «Qualità e completezza dei dati disponibili» → colonna «Peggio del previsto» selezionata **OPPURE** Q9.1 riga 1 «Qualità e completezza dei dati disponibili» → colonna «Molto peggio del previsto» selezionata **OPPURE** Q9.1 riga 2 «Affidabilità e prevedibilità degli output pro» → colonna «Peggio del previsto» selezionata **OPPURE** Q9.1 riga 2 «Affidabilità e prevedibilità degli output pro» → colonna «Molto peggio del previsto» selezionata **OPPURE** Q9.1 riga 3 «Sforzo di progettazione e messa a punto delle» → colonna «Peggio del previsto» selezionata **OPPURE** Q9.1 riga 3 «Sforzo di progettazione e messa a punto delle» → colonna «Molto peggio del previsto» selezionata **OPPURE** Q9.1 riga 4 «Facilità di integrazione con i sistemi aziend» → colonna «Peggio del previsto» selezionata **OPPURE** Q9.1 riga 4 «Facilità di integrazione con i sistemi aziend» → colonna «Molto peggio del previsto» selezionata **OPPURE** Q9.1 riga 5 «Tempo necessario per portare la soluzione a r» → colonna «Peggio del previsto» selezionata **OPPURE** Q9.1 riga 5 «Tempo necessario per portare la soluzione a r» → colonna «Molto peggio del previsto» selezionata **OPPURE** Q9.1 riga 6 «Adozione da parte degli utenti» → colonna «Peggio del previsto» selezionata **OPPURE** Q9.1 riga 6 «Adozione da parte degli utenti» → colonna «Molto peggio del previsto» selezionata **OPPURE** Q9.1 riga 7 «Beneficio economico effettivamente ottenuto» → colonna «Peggio del previsto» selezionata **OPPURE** Q9.1 riga 7 «Beneficio economico effettivamente ottenuto» → colonna «Molto peggio del previsto» selezionata
- 📦 **Blocco «S10 - Barriere e spesa (10.1-10.2)»**
  - Pagina 1:
    - **Q10.1a** — scelta multipla (obbligatoria; max 3 scelte; esclusiva: riga 17)
  - Pagina 2:
    - **Q10.1b** — scelta multipla (obbligatoria; max 3 scelte; esclusiva: riga 17)
  - Pagina 3:
    - **Q10.1c** — scelta multipla (obbligatoria; max 3 scelte; esclusiva: riga 17)
  - Pagina 4:
    - **Q10.2** — scelta singola (obbligatoria)
- 🔀 **Branch** — prosegue nel ramo solo se: Q10.2 b) «Inferiore a 10.000 euro» selezionata **OPPURE** Q10.2 c) «Tra 10.000 e 25.000 euro» selezionata **OPPURE** Q10.2 d) «Tra 25.001 e 50.000 euro» selezionata **OPPURE** Q10.2 e) «Tra 50.001 e 100.000 euro» selezionata **OPPURE** Q10.2 f) «Tra 100.001 e 250.000 euro» selezionata **OPPURE** Q10.2 g) «Tra 250.001 e 500.000 euro» selezionata **OPPURE** Q10.2 h) «Tra 500.001 e 1 milione di euro» selezionata **OPPURE** Q10.2 i) «Oltre 1 milione di euro» selezionata
  - 📦 **Blocco «S10 - Dinamica e ripartizione spesa (10.3-10.4)»**
    - Pagina 1:
      - **Q10.3a** — scelta singola (obbligatoria)
      - **Q10.3b** — scelta singola (obbligatoria)
    - Pagina 2:
      - **Q10.4_ns** — scelta multipla (facoltativa)
      - **Q10.4** — somma costante (obbligatoria; totale = 100)
        - *Mostrata (nella stessa pagina) se:* Q10.4_ns a) «Non siamo in grado di stimare la ripartizione» NON selezionata
- 📦 **Blocco «S10 - Benefici e prossimi passi (10.5-10.7)»**
  - Pagina 1:
    - **Q10.5** — scelta singola (obbligatoria)
  - Pagina 2:
    - **Q10.6a** — scelta singola (obbligatoria)
      - *Mostrata se:* Q10.5 a) «Sì, con una metodologia strutturata, applicata sistematicame» selezionata **OPPURE** Q10.5 b) «Sì, con una metodologia strutturata applicata dal team di au» selezionata **OPPURE** Q10.5 c) «Solo per alcuni progetti, con stime ad hoc» selezionata
  - Pagina 3:
    - **Q10.6b** — scelta singola (obbligatoria)
      - *Mostrata se:* Q10.5 a) «Sì, con una metodologia strutturata, applicata sistematicame» selezionata **OPPURE** Q10.5 b) «Sì, con una metodologia strutturata applicata dal team di au» selezionata **OPPURE** Q10.5 c) «Solo per alcuni progetti, con stime ad hoc» selezionata
      - *Opzione h) «Non applicabile» visibile se:* Q10.6a l) «Non applicabile» NON selezionata
  - Pagina 4:
    - **Q10.7** — scelta multipla (obbligatoria; max 3 scelte)
