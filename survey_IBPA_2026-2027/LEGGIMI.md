# Survey IBPA 2026/2027 – End User Grandi e grandissime imprese: file per Qualtrics

- Contenuti: `Survey_IBPA_2026-2027_EndUser_Grandi_FINALE_v4.docx`
- Stile e impostazioni: `Survey_IBPA_2025.qsf`, la survey dell'anno scorso

## File

| File | A cosa serve |
|---|---|
| `Survey_IBPA_2026-2027_EndUser_Grandi.qsf` | Il questionario da importare in Qualtrics |
| `build_qsf.py` | Script che genera il QSF, utile per rigenerarlo dopo eventuali modifiche ai testi |
| `LEGGIMI.md` | Questo documento |

## Come importare

Qualtrics → **Crea nuovo progetto** → **Sondaggio** → **Importa un file QSF** → seleziona il file `.qsf` → **Crea progetto**.

Conviene importarlo nello **stesso account della survey 2025**. Il file richiama infatti due elementi di quell'account:
- il tema grafico `polimi`;
- il messaggio di fine survey della vostra libreria (`MS_1YBpMl6kYzH5CZg`).

In un altro account Qualtrics usa tema e messaggio predefiniti, e vanno reimpostati.

## Stile ripreso dal 2025

- **Struttura**: blocco «Introduzione» + blocco unico «Questionario» diviso in pagine, come nel 2025. Il survey flow contiene solo i due blocchi, uno dopo l'altro.
- **Pagina di introduzione**: è il testo 2025 (obiettivi, riservatezza dei dati, guida alla compilazione, contatto, «Perché partecipare?», consenso privacy) con tre aggiornamenti:
  - anno «2026/2027»;
  - durata «dai 20 ai 25 minuti», in base ai 22 minuti stimati nel Word;
  - **tolta la data del Convegno Finale** (era «4 marzo 2026»): va aggiunta quella del 2027.
- **Intestazioni di sezione** come testi descrittivi in grassetto a 29 px. Gli eventuali testi introduttivi (definizione di Process Automation, introduzione alla sezione 5 e alla sezione 9) sono in corsivo a 16 px.
- **Domande**: testo semplice, con l'istruzione sotto in corsivo a 16 px senza parentesi («Risposta singola», «Risposta multipla – …»). Le etichette delle opzioni sono in grassetto dove il 2025 lo faceva: strumenti della 4.1, fasi della 3.3, capacità della 6.2, famiglie della 5.1. «Prevalente» è sottolineato nella 3.4, come nel 2025.
- **Anagrafica**: un unico modulo con Nome, Cognome, E-mail aziendale (con validazione), Ragione sociale e **Job Title**. «JT» del Word è il Job Title del 2025. Il settore è a scelta singola e la dimensione aziendale è a **menu a tendina**, come nel 2025.
- **Screen-out**: come nel 2025, con skip logic dal settore «Public Administration» e dalla dimensione «Fino a 49 dipendenti» verso la pagina finale «Esclusione». Il testo è quello del 2025.
- **Barriere (10.1)**: come le domande 8.1/8.2 del 2025, una domanda per ciascuna tipologia di automazione: tradizionale, intelligente, agentica. Massimo 3 risposte, con «Nessuna barriera rilevante» esclusiva.
- **Dinamica della spesa (10.3)**: è la stessa tabella side-by-side del 2025 (colonna «Non so» + colonna «Variazione» a tendina), con le righe «Variazione rispetto al 2025» e «Previsione sul 2027».
- **Opzioni del sondaggio identiche al 2025**:
  - pulsante Indietro attivo, *Save & continue* attivo;
  - barra di avanzamento senza testo, pulsante avanti « → »;
  - risposte parziali chiuse dopo 1 settimana;
  - titolo «Sondaggio IBPA», lingua italiano.

## Pulsante Indietro: sempre disponibile

Qualtrics disattiva il pulsante Indietro sulla prima pagina del blocco che segue un branch, un embedded data o qualunque altro elemento del survey flow posto tra due blocchi. Per questo **tutti i filtri sono display logic** sulle domande o sulle opzioni, e gli screen-out sono skip logic dentro lo stesso blocco. Non c'è alcun elemento tra i blocchi, quindi il pulsante Indietro compare su ogni pagina, tranne ovviamente la prima. Se un rispondente torna indietro e cambia una risposta, le domande successive si riadattano.

> Se in futuro aggiungete elementi al survey flow tra i due blocchi (branch, randomizer, embedded data…), il pulsante Indietro sparisce sulla pagina successiva.

## Come sono implementati i filtri del Word

| Filtro nel Word | Implementazione |
|---|---|
| Settore «Public Administration» → esce | Skip logic → pagina «Esclusione» → fine |
| Fino a 49 dipendenti → esce | Skip logic → pagina «Esclusione» → fine |
| 2.4 solo se la riga 1 della 2.3 non è «No» | Display logic: riga 1 = una delle prime tre colonne |
| 3.3 e 3.4 non mostrate a chi ha 3.1 = d) | Display logic: 3.1 = a), b), c) o e) |
| Sezioni 5, 7.2–7.6 e 8 saltate da chi ha 3.1 = d) e 4.1 = h) | Display logic «adopter» su ogni domanda e intestazione delle sezioni: 3.1 diversa da d) **oppure** almeno uno strumento a)–g) alla 4.1. È lo stesso «doppio controllo» usato nel 2025 |
| 5.2: solo famiglie con almeno una delle prime tre colonne alla 5.1; con una sola famiglia si salta la 5.2; con nessuna si va alla sezione 6 | Ogni opzione della 5.2 compare solo se la sua riga 5.1 ha una delle prime tre colonne. La 5.2 compare solo se le famiglie selezionabili sono almeno due: in ogni gruppo di tre famiglie deve essercene almeno una selezionabile. Ogni matrice 5.3 compare se la famiglia è scelta alla 5.2, oppure se è l'unica selezionabile |
| 6.2 non mostrata a chi ha 6.1 = a), b) o c) | Display logic: 6.1 = d), e), f) o g) |
| 7.1 a tutti | Nessun filtro |
| 7.3 se 7.2 = b), c) o d); 7.4 se 7.3 ≠ a); 7.5 se 7.2 = da f) a i) | Display logic, sempre in combinazione con «adopter» |
| 8.2 se 8.1 = a) o b) | Display logic + «adopter» |
| Sezione 9 saltata se 3.1 = d) oppure se alla 5.1 non c'è nessuna casella intelligente/agentica | Display logic: 3.1 diversa da d) **e** almeno una delle 22 caselle (11 righe × 2 colonne) |
| 9.2 se alla 9.1 almeno una riga è «peggio» o «molto peggio» | Display logic + condizioni della sezione 9 |
| 10.3 e 10.4 se 10.2 = da b) a i) | Display logic |
| 10.4: «Non siamo in grado di stimare» | Il campo percentuali (totale 100) scompare nella stessa pagina se si spunta la casella |
| 10.6 non mostrata a chi ha 10.5 = d) o e) | Display logic su 10.6a e 10.6b |
| 10.6 «compili almeno una delle due righe» | Se la riga in euro è «Non applicabile», nella riga FTE «Non applicabile» non compare |

Senza branch ed embedded data, il dataset non ha la variabile `screen_out`. Gli esclusi si riconoscono da Q1.6 = «Public Administration» oppure Q1.7 = «Fino a 49 dipendenti».

## Scelte di programmazione da conoscere

1. **10.3**: nella tabella side-by-side le opzioni a tendina sono comuni alle due righe. Per le prime due ho usato le formule neutre del 2025, «Più che raddoppio» e «Raddoppio», al posto di «più che raddoppiata/raddoppierà» del Word. Come nel 2025, la tabella non è obbligatoria e la colonna «Non so» riporta il suggerimento di non compilare «Variazione».
2. **10.6**: le due righe hanno fasce diverse (euro e FTE), quindi sono due domande su due pagine (`Q10.6a`, `Q10.6b`).
3. **10.4**: la casella «Non siamo in grado di stimare la ripartizione» sta sopra il campo percentuali. Qualtrics infatti nasconde una domanda solo in base a una domanda che la precede sulla stessa pagina.
4. **3.4**: è divisa in due domande, A e B, sulla stessa pagina.
5. **Obbligatorietà**: tutte le domande sono obbligatorie, tranne 5.2 e 5.3 («Facoltativo» nel Word), la tabella 10.3 (come nel 2025) e la casella della 10.4.
6. **Opzioni esclusive**: quelle indicate nel Word (4.1 h, 7.3 h, 8.1 f), più «Nessuna barriera rilevante» e le ultime due colonne della 5.1. La 6.2 k) «Non ho abbastanza informazioni…» non è esclusiva, come nel 2025 e nel Word.
7. **Randomizzazione**: 4.1 da a) a g), con h) sempre in fondo; righe della 5.1.
8. **Numerazione**: come nel 2025, i numeri non compaiono al rispondente. Sono negli *export tag*:
   - `Q1` = modulo anagrafico, con i campi 1–5 nell'ordine del Word;
   - `Q1.6` … `Q10.7` = domande; `Q2` … `Q10` = intestazioni di sezione;
   - `A` = introduzione; `Esclusione` = pagina finale per gli esclusi.

## Da controllare dopo l'import (circa 10 minuti)

1. **Introduzione**: aggiungi la data del Convegno Finale 2027 e verifica la durata indicata.
2. **Messaggio di fine survey**: è quello della libreria usato nel 2025. Controlla che il testo vada bene anche quest'anno (nel Word: «Fine del questionario. La ringraziamo per il tempo dedicato.»).
3. **Anteprima dei percorsi**:
   - a) «Public Administration» → pagina di esclusione;
   - b) 3.1 «Non applichiamo» + 4.1 «Nessuno di questi» → niente sezioni 5, 7.2–7.6, 8 e 9;
   - c) due o più famiglie automatizzate tra Amministrazione, Acquisti, Operations e Customer service → 5.2 con quelle famiglie e matrici 5.3;
   - d) una sola famiglia automatizzata → niente 5.2, direttamente la sua matrice;
   - e) in tutte le pagine prova il pulsante Indietro.
4. **10.4**: controlla che la somma costante abbia *Must total = 100*. È l'unica impostazione senza precedenti nel 2025: se manca, si attiva in un clic.

## Punti aperti nel Word (da decidere con il team)

1. **Chi risponde d) alla 3.1.** La nota sotto la 3.1 dice che salta 5, 7, 8 e 9. Le note di sezione fanno saltare 5, 7.2–7.6 e 8 solo a chi ha anche h) alla 4.1. Ho seguito le note di sezione, che sono anche la logica usata nel 2025.
2. **3.2.** Nel Word non ha filtri, quindi la vede anche chi risponde d) alla 3.1.
3. **2.3.** La nota parla di un'ultima riga «inventario dei bot e dei flussi in esercizio» che non c'è: l'ultima riga attuale è «Un repository centrale di processi…».
4. **1.7.** Le fasce «Da 250 a 999» e «Oltre 1.000» lasciano scoperto il valore 1.000.
5. **Commenti aperti, non applicati**:
   - 10.2: «non si consideri spesa per personale interno dedicato» (Irene Di Deo);
   - 5.1: valutare se togliere la riga «Strategia, governance e organizzazione»;
   - 10.1: tabella «troppo pesante». Ora è su tre pagine, come le barriere del 2025.

## Appendice – Pagine e logiche (generata dal QSF)

**Survey flow:** blocco «Introduzione» → blocco «Questionario» (nessun branch o embedded data: il pulsante Indietro è disponibile su ogni pagina)

### Blocco «Introduzione»
**Pagina 1**
- **A** — testo

### Blocco «Questionario»
**Pagina 1**
- **Q1** — modulo testo (obbligatoria)
- **Q1.6** — scelta singola (obbligatoria)
  - *Skip logic:* se q) «Public Administration» → salta a **Esclusione**
- **Q1.7** — menu a tendina (obbligatoria)
  - *Skip logic:* se a) «Fino a 49 dipendenti» → salta a **Esclusione**

**Pagina 2**
- **Q2** — testo
- **Q2.1** — scelta singola (obbligatoria)
- **Q2.2** — scelta singola (obbligatoria)
- **Q2.3** — matrice una risposta per riga (obbligatoria)

**Pagina 3**
- **Q2.4** — scelta singola (obbligatoria)
  - *Mostrata se:* (Q2.3 riga 1 → «Sì, presente e mantenuto aggiornato» selezionata **o** Q2.3 riga 1 → «Sì, ma non aggiornato regolarmente» selezionata **o** Q2.3 riga 1 → «In corso di definizione» selezionata)

**Pagina 4**
- **Q3** — testo
- **Q3.1** — scelta singola (obbligatoria)
- **Q3.2** — matrice una risposta per riga (obbligatoria)

**Pagina 5**
- **Q3.3** — scelta singola (obbligatoria)
  - *Mostrata se:* 3.1 diversa da d)
- **Q3.4A** — scelta singola (obbligatoria)
  - *Mostrata se:* 3.1 diversa da d)
- **Q3.4B** — scelta singola (obbligatoria)
  - *Mostrata se:* 3.1 diversa da d)

**Pagina 6**
- **Q4** — testo
- **Q4.1** — scelta multipla (obbligatoria; ordine casuale)

**Pagina 7**
- **Q5** — testo
  - *Mostrata se:* «adopter» (3.1 diversa da d) **oppure** almeno uno strumento a)–g) alla 4.1)
- **Q5.1** — matrice risposta multipla (obbligatoria; ordine casuale)
  - *Mostrata se:* «adopter» (3.1 diversa da d) **oppure** almeno uno strumento a)–g) alla 4.1)

**Pagina 8**
- **Q5.2** — scelta multipla (facoltativa; max 2)
  - *Mostrata se:* «adopter» (3.1 diversa da d) **oppure** almeno uno strumento a)–g) alla 4.1) **E** alla 5.1 almeno una delle prime tre colonne in una delle righe 5, 6, 7 **E** alla 5.1 almeno una delle prime tre colonne in una delle righe 6, 7, 8 **E** alla 5.1 almeno una delle prime tre colonne in una delle righe 5, 7, 8 **E** alla 5.1 almeno una delle prime tre colonne in una delle righe 5, 6, 8
  - *Opzione a) «Amministrazione, finanza e controllo» visibile se:* alla 5.1 almeno una delle prime tre colonne nella riga 8
  - *Opzione b) «Acquisti e gestione dei fornitori» visibile se:* alla 5.1 almeno una delle prime tre colonne nella riga 5
  - *Opzione c) «Operations, produzione, logistica e fulfillme» visibile se:* alla 5.1 almeno una delle prime tre colonne nella riga 6
  - *Opzione d) «Customer service e gestione della relazione c» visibile se:* alla 5.1 almeno una delle prime tre colonne nella riga 7

**Pagina 9**
- **Q5.3a** — matrice una risposta per riga (facoltativa)
  - *Mostrata se:* «adopter» (3.1 diversa da d) **oppure** almeno uno strumento a)–g) alla 4.1) **E** alla 5.1 almeno una delle prime tre colonne nella riga 8 **E** (5.2 a) selezionata **oppure** nessun'altra famiglia selezionabile alla 5.1)

**Pagina 10**
- **Q5.3b** — matrice una risposta per riga (facoltativa)
  - *Mostrata se:* «adopter» (3.1 diversa da d) **oppure** almeno uno strumento a)–g) alla 4.1) **E** alla 5.1 almeno una delle prime tre colonne nella riga 5 **E** (5.2 b) selezionata **oppure** nessun'altra famiglia selezionabile alla 5.1)

**Pagina 11**
- **Q5.3c** — matrice una risposta per riga (facoltativa)
  - *Mostrata se:* «adopter» (3.1 diversa da d) **oppure** almeno uno strumento a)–g) alla 4.1) **E** alla 5.1 almeno una delle prime tre colonne nella riga 6 **E** (5.2 c) selezionata **oppure** nessun'altra famiglia selezionabile alla 5.1)

**Pagina 12**
- **Q5.3d** — matrice una risposta per riga (facoltativa)
  - *Mostrata se:* «adopter» (3.1 diversa da d) **oppure** almeno uno strumento a)–g) alla 4.1) **E** alla 5.1 almeno una delle prime tre colonne nella riga 7 **E** (5.2 d) selezionata **oppure** nessun'altra famiglia selezionabile alla 5.1)

**Pagina 13**
- **Q6** — testo
- **Q6.1** — scelta singola (obbligatoria)

**Pagina 14**
- **Q6.2** — scelta multipla (obbligatoria)
  - *Mostrata se:* (Q6.1 d) selezionata **o** Q6.1 e) selezionata **o** Q6.1 f) selezionata **o** Q6.1 g) selezionata)

**Pagina 15**
- **Q7** — testo
- **Q7.1** — scelta singola (obbligatoria)
- **Q7.2** — scelta singola (obbligatoria)
  - *Mostrata se:* «adopter» (3.1 diversa da d) **oppure** almeno uno strumento a)–g) alla 4.1)

**Pagina 16**
- **Q7.3** — scelta multipla (obbligatoria)
  - *Mostrata se:* «adopter» (3.1 diversa da d) **oppure** almeno uno strumento a)–g) alla 4.1) **E** (Q7.2 b) selezionata **o** Q7.2 c) selezionata **o** Q7.2 d) selezionata)

**Pagina 17**
- **Q7.4** — scelta singola (obbligatoria)
  - *Mostrata se:* «adopter» (3.1 diversa da d) **oppure** almeno uno strumento a)–g) alla 4.1) **E** Q7.3 a) NON selezionata
- **Q7.5** — scelta multipla (obbligatoria; max 2)
  - *Mostrata se:* «adopter» (3.1 diversa da d) **oppure** almeno uno strumento a)–g) alla 4.1) **E** (Q7.2 f) selezionata **o** Q7.2 g) selezionata **o** Q7.2 h) selezionata **o** Q7.2 i) selezionata)
- **Q7.6** — scelta singola (obbligatoria)
  - *Mostrata se:* «adopter» (3.1 diversa da d) **oppure** almeno uno strumento a)–g) alla 4.1)

**Pagina 18**
- **Q8** — testo
  - *Mostrata se:* «adopter» (3.1 diversa da d) **oppure** almeno uno strumento a)–g) alla 4.1)
- **Q8.1** — scelta multipla (obbligatoria)
  - *Mostrata se:* «adopter» (3.1 diversa da d) **oppure** almeno uno strumento a)–g) alla 4.1)

**Pagina 19**
- **Q8.2** — scelta multipla (obbligatoria; max 3)
  - *Mostrata se:* «adopter» (3.1 diversa da d) **oppure** almeno uno strumento a)–g) alla 4.1) **E** (Q8.1 a) selezionata **o** Q8.1 b) selezionata)

**Pagina 20**
- **Q9** — testo
  - *Mostrata se:* 3.1 diversa da d) **E** Q5.1: almeno una casella in colonna «Agenti AI autonomi» / «Automazione intelligente (AI)» (righe 1–11)
- **Q9.1** — matrice una risposta per riga (obbligatoria)
  - *Mostrata se:* 3.1 diversa da d) **E** Q5.1: almeno una casella in colonna «Agenti AI autonomi» / «Automazione intelligente (AI)» (righe 1–11)

**Pagina 21**
- **Q9.2** — scelta singola (obbligatoria)
  - *Mostrata se:* 3.1 diversa da d) **E** Q5.1: almeno una casella in colonna «Agenti AI autonomi» / «Automazione intelligente (AI)» (righe 1–11) **E** Q9.1: almeno una casella in colonna «Molto peggio del previsto» / «Peggio del previsto» (righe 1–7)

**Pagina 22**
- **Q10** — testo
- **Q10.1a** — scelta multipla (obbligatoria; max 3)

**Pagina 23**
- **Q10.1b** — scelta multipla (obbligatoria; max 3)

**Pagina 24**
- **Q10.1c** — scelta multipla (obbligatoria; max 3)

**Pagina 25**
- **Q10.2** — scelta singola (obbligatoria)

**Pagina 26**
- **Q10.3** — tabella side-by-side (facoltativa)
  - *Mostrata se:* (Q10.2 b) selezionata **o** Q10.2 c) selezionata **o** Q10.2 d) selezionata **o** Q10.2 e) selezionata **o** Q10.2 f) selezionata **o** Q10.2 g) selezionata **o** Q10.2 h) selezionata **o** Q10.2 i) selezionata)

**Pagina 27**
- **Q10.4_ns** — scelta multipla (facoltativa)
  - *Mostrata se:* (Q10.2 b) selezionata **o** Q10.2 c) selezionata **o** Q10.2 d) selezionata **o** Q10.2 e) selezionata **o** Q10.2 f) selezionata **o** Q10.2 g) selezionata **o** Q10.2 h) selezionata **o** Q10.2 i) selezionata)
- **Q10.4** — somma costante (obbligatoria; totale = 100)
  - *Mostrata (nella pagina) se:* (Q10.2 b) selezionata **o** Q10.2 c) selezionata **o** Q10.2 d) selezionata **o** Q10.2 e) selezionata **o** Q10.2 f) selezionata **o** Q10.2 g) selezionata **o** Q10.2 h) selezionata **o** Q10.2 i) selezionata) **E** Q10.4_ns a) NON selezionata

**Pagina 28**
- **Q10.5** — scelta singola (obbligatoria)

**Pagina 29**
- **Q10.6a** — scelta singola (obbligatoria)
  - *Mostrata se:* (Q10.5 a) selezionata **o** Q10.5 b) selezionata **o** Q10.5 c) selezionata)

**Pagina 30**
- **Q10.6b** — scelta singola (obbligatoria)
  - *Mostrata se:* (Q10.5 a) selezionata **o** Q10.5 b) selezionata **o** Q10.5 c) selezionata)
  - *Opzione h) «Non applicabile» visibile se:* Q10.6a l) NON selezionata

**Pagina 31**
- **Q10.7** — scelta multipla (obbligatoria; max 3)

**Pagina 32**
- **Esclusione** — testo
  - *Mostrata se:* (Q1.6 q) selezionata **o** Q1.7 a) selezionata)

