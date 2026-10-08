# Mercato e spesa in cybersecurity in UE e Regno Unito: conclusioni e metodologie di stima

Data: 8 ottobre 2026.

**Basi del documento**
- **Database.** `fonti_mercato_cyber_UE_UK_2026-10-08.xlsx`: 1.215 dati, 406 schede fonte, 158 ricerche senza esito.
- **Ricerca sulle metodologie.** Cinque gruppi di produttori di stime: società di analisi IT, editori di ricerche di mercato, osservatori e studi nazionali, survey lato domanda e statistiche ufficiali, letteratura e quadri europei. Le affermazioni chiave sono state ricontrollate da verificatori indipendenti.

Alcuni valori usati qui vengono solo dalla ricerca sulle metodologie e non sono ancora nel foglio Dati:
- i totali INE Spagna e Banca d'Italia (Invind 2016);
- i dati di Statistics Canada;
- alcuni rapporti delle tabelle 1.5 e 3.2.

Per ognuno è indicato il link. I valori in euro di fonti in altra valuta usano le medie annue dei cambi BCE del foglio `Cambi`.

## Sintesi

- **Nessun paese UE ha una misura ufficiale del mercato domestico della cybersecurity**, cioè delle vendite dei fornitori ai clienti del paese. Solo la Spagna (INE, dal 2021) pubblica ogni anno una statistica ufficiale della spesa in sicurezza delle imprese con almeno 10 addetti.
- **Numeri con lo stesso nome misurano tre oggetti diversi:** mercato dei fornitori, ricavi dell'industria nazionale, spesa delle organizzazioni. Gran parte della dispersione tra fonti è una differenza di perimetro.
- **La metodologia più diffusa per il "mercato" è la somma dei ricavi dei vendor**, ripartita poi per paese, settore e dimensione con survey o indicatori macro. Però la maggior parte delle fonti non dichiara alcun metodo: su 406 schede, 252 non lo dichiarano e 58 riprendono un'altra fonte.
- **Le metodologie più vicine all'oggetto del modello SBS (spesa delle imprese utilizzatrici) sono le meno diffuse.** Sono due: la survey alle imprese riportata all'universo e il modello a rapporti fatturato × intensità IT × quota sicurezza. La seconda è applicata per settore nella valutazione d'impatto NIS2 della Commissione.
- **Metodo consigliato:**
  1. catena a rapporti per settore NACE e classe dimensionale;
  2. parametri dalle survey riportate all'universo (INE, Invind) e, con cautela, dalle survey per organizzazione;
  3. controllo con i mercati lato offerta (Anitec-Assinform, Polimi, Bitkom con PAC), dopo aver tolto personale interno, settori fuori SBS e voci non comprese;
  4. risultato presentato come forbice.

---

## 1. Cosa dice il database

### 1.1 Trasparenza e lato della stima

Criterio: fonti con almeno una riga il cui oggetto è Mercato domestico, Spesa o budget delle organizzazioni oppure Ricavi dell'industria nazionale. Il lato prevalente è il lato più frequente tra le righe della fonte.

| Indicatore | Valore |
|---|---|
| Fonti con valori di mercato, spesa o ricavi | 274 |
| di cui con approccio "Non dichiarato" | 143 |
| di cui "Ripreso da altra fonte" | 53 |
| di cui con trasparenza C (solo testo generico) o D (nessuna metodologia) | 216 |
| Lato prevalente: Offerta / Domanda / Misto / Non determinabile / pari merito | 85 / 37 / 16 / 134 / 2 |
| Righe di mercato domestico con tipo Totale aggregato (con scomposizioni; 385 senza) | 514 |
| di cui classificate lato domanda | 5, tutte IMARC Europa (due sono previsioni) |

**Nessun totale nazionale di mercato domestico è costruito dal lato domanda con un metodo verificabile.** Le fonti lato domanda misurano quasi sempre valori per singola organizzazione: mediane, medie, quote del budget IT.

Sulle 406 schede del foglio Fonti_Metodologie l'approccio è:

| Approccio | Schede |
|---|---|
| Non dichiarato | 252 |
| Ripreso da altra fonte | 58 |
| Bottom-up, in gran parte lato offerta | 47 |
| Modello previsionale | 26 |
| Top-down | 13 |
| Survey riportata all'universo | 8 |

### 1.2 Tre oggetti di misura non confrontabili

| Oggetto | Esempi | Cosa misura | Personale interno | Export |
|---|---|---|---|---|
| Mercato dei fornitori | IDC, Gartner, PAC per Bitkom, Anitec-Assinform, Statista, editori; Polimi con un perimetro più ampio | Vendite di prodotti e servizi di sicurezza ai clienti del paese | Escluso: dichiarato da Anitec per il mercato ICT e da PAC (ricavi non captive); dedotto per IDC, Gartner, Statista ed editori; non dichiarato da Polimi | Escluso (dedotto dall'allocazione al paese di spesa) |
| Ricavi dell'industria nazionale | DSIT (UK), ACN (Francia), Agoria (Belgio), Cyber Ireland, INCIBE (Spagna), Dialogic (Paesi Bassi) | Fatturato cyber dei fornitori con sede nel paese | Escluso, salvo Cyber Ireland che conta le funzioni cyber interne dei gruppi | Incluso: dichiarato per Agoria e ACN, dedotto per DSIT, non dichiarato per INCIBE e Dialogic |
| Spesa delle organizzazioni | ENISA NIS Investments, UK Cyber Security Breaches Survey, INE, Banca d'Italia, Bitkom Wirtschaftsschutz | Spesa o quota di budget dichiarata dagli utenti | Incluso per ENISA, CSBS, INE e Banca d'Italia; non dichiarato per Bitkom | Non pertinente |

Il peso del personale interno sulla spesa di sicurezza varia:
- 25% nelle banche italiane ([CIPA](https://www.cipa.it/rilevazioni/economiche/2024/Rilevazione_economica_2024.pdf));
- circa 37% nelle entità NIS (ENISA 2020-2021);
- 39% tra i CISO del benchmark [IANS 2025](https://sf-cdn.iansresearch.com/sitefinity/docs/default-source/reports/2025-security-budget-benchmark-summary-report_08_05_2025.pdf?sfvrsn=43097214_2).

WifOR (Germania) è un caso a parte: il suo "mercato" è produzione più importazioni meno export.

**Esempio della distanza tra oggetti: il Regno Unito.**
- DSIT stima ricavi del settore cyber per 14,7 mld £ nel 2025, cioè 17.198 Mln €, con un export di 8,6 mld £ nel 2024 ([DSIT 2026](https://www.gov.uk/government/publications/cyber-security-sectoral-analysis-2026/cyber-security-sectoral-analysis-2026)).
- Gli editori stimano il mercato domestico 2025 tra 13.071 e 15.398 Mln € (Mordor, Grand View, IMARC).
- Ricavi meno export valgono circa 6 mld £, quindi circa la metà delle stime degli editori (calcolo con anni non identici).

Il gap è coperto dalle importazioni e dai margini del canale: i due oggetti non si confrontano senza correzioni.

### 1.3 Dispersione per i paesi del modello

| Paese | Fonte | Anno | Valore pubblicato | Mln € | Lato | Note di perimetro |
|---|---|---|---|---|---|---|
| Italia | [Anitec-Assinform 2026](https://www.matricedigitale.it/wp-content/uploads/2026/07/Rapporto-Anitec-Assinform_Il-Digitale-in-Italia-2026.pdf) | 2025 | 2.245 Mln € | 2.245 | Offerta | Imprese e PA; il comunicato arrotonda a 2,24 mld € |
| Italia | [Osservatorio Polimi 2026](https://www.osservatori.net/comunicato/cybersecurity-data-protection/cybersecurity-italia-mercato-crescita/) | 2025 | 2,78 mld € | 2.780 | Misto | Imprese e PA; include formazione e polizze cyber |
| Italia | [Ken Research](https://www.kenresearch.com/italy-cybersecurity-and-mssp-market) | 2025 | 3.141 Mln USD | 2.780 | Non determinabile | Coincide con Polimi |
| Italia | [Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/italy-cybersecurity-market) | 2025 | 4,12 mld USD | 3.646 | Non determinabile | Catena dichiarata nella metodologia generale, senza parametri |
| Italia | [MarketsandMarkets](https://www.marketsandmarkets.com/Market-Reports/geography/cyber-security-market/italy) | 2025 (stima) | 5,72 mld USD | 5.063 | Non determinabile | Pagina paese con testo del report globale |
| Germania | [CBI su dati Statista](https://www.cbi.eu/market-information/outsourcing-itobpo/cybersecurity/market-potential) | 2025 | 6,87 mld € | 6.870 | Offerta | B2C, B2B e B2G a prezzi dei vendor |
| Germania | [Bitkom con dati PAC](https://www.bitkom.org/sites/main/files/2025-10/bitkom-charts-cybercrime-und-der-markt-fuer-it-sicherheit-2025.pdf) | 2024 | 10,1 mld € | 10.100 | Offerta | Ultimo consuntivo; clienti inclusi non dichiarati |
| Germania | stessa fonte | 2025 (stima) | 11,1 mld € | 11.100 | Offerta | Software 4,8, servizi 5,6, hardware 0,8 mld € (le componenti sommano 11,2 per arrotondamento) |
| Germania | [Grand View Research](https://www.grandviewresearch.com/horizon/outlook/cyber-security-market/germany) | 2025 | 15,1 mld USD | 13.365 | Non determinabile | Hardware al 52,7%, contro circa 7% in Bitkom |
| Austria | [Mordor Intelligence](https://www.mordorintelligence.com/de/industry-reports/austria-cybersecurity-market) | 2025 | 560 Mln USD | 496 | Non determinabile | Nessuna fonte nazionale pubblica un totale |
| Austria | [Verified Market Research](https://www.verifiedmarketresearch.com/product/austria-cybersecurity-market/) | 2024 | 1,2 mld USD | 1.109 | Non determinabile | Per il 2024 Metastat dà 508 Mln € |

**Italia.** Polimi è sempre sopra Anitec-Assinform e la distanza si è allargata:

| Anno | Distanza | Polimi rispetto ad Anitec |
|---|---|---|
| 2020 | 132 Mln € | +11% |
| 2023 | 362 Mln € | +20% |
| 2024 | 479 Mln € | +24% |
| 2025 | 535 Mln € | +24% |

Una parte dipende dal perimetro. Nel 2024 le polizze cyber valgono l'8% della spesa Polimi, circa 200 Mln € ([scheda MAECI su dati Polimi](https://www.esteri.it/wp-content/uploads/2025/05/cyber_sp.pdf), valore letto da grafico). Spiegano quindi circa il 40% dello scarto. Il resto riflette metodi non documentati.

Le stime degli editori per l'Italia 2025 vanno da 2.780 Mln € (Ken Research) a 5.063 Mln € (MarketsandMarkets). La quota del 14,2% dell'Europa attribuita da IMARC implica circa 10,3 mld € (calcolo).

**Germania.** Nel 2025 la forbice va da 6.870 a 13.365 Mln €. 6Wresearch dà 95 Mln €, un valore anomalo che il foglio Copertura_Paesi include nel minimo.

### 1.4 Rotture di serie

- **Bitkom.** Passa da dati IDC a dati PAC. Il valore 2024 scende da 11,2 mld € ([ottobre 2024](https://www.bitkom.org/Presse/Presseinformation/Erstmals-mehr-als-10-Milliarden-Euro-fuer-Deutschlands-Cybersicherheit)) a 10,1 mld € ([ottobre 2025](https://www.bitkom.org/sites/main/files/2025-10/bitkom-charts-cybercrime-und-der-markt-fuer-it-sicherheit-2025.pdf)). Un rapporto Bitkom diverso (ITK-Markt 2025) dà 5,1 mld € per il software di sicurezza 2025, contro 4,8 della serie PAC.
- **Polimi.** Ha rivisto il 2021 da 1,55 a 1,576 mld €.
- **Gartner.** Da luglio 2018 ha aggiunto segmenti al forecast ed è passato alla spesa end user ([comunicato 2018](https://www.gartner.com/en/newsroom/press-releases/2018-08-15-gartner-forecasts-worldwide-information-security-spending-to-exceed-124-billion-in-2019)). Prima il forecast era basato sui ricavi dei vendor, secondo la [presentazione F-Secure Q2 2018](https://www.withsecure.com/content/dam/with-secure/en/investor/materials/interim-reports/2018/F-Secure%20Q2%202018%20Presentation%20FINAL.pdf).
- **Editori.** I valori cambiano a ogni edizione; Statista stessa avverte che edizioni diverse non sono confrontabili.

### 1.5 Rapporti dichiarati dagli utenti

| Rapporto | Valore | Popolazione | Fonte |
|---|---|---|---|
| Sicurezza su uscite di cassa IT | 4,9% (4,4% sul costo totale IT) | Banche italiane, 23 gruppi (2024) | [CIPA](https://www.cipa.it/rilevazioni/economiche/2024/Rilevazione_economica_2024.pdf) |
| Sicurezza su spesa IT, media | 5,1% (2022), 5,6% (2023) | Organizzazioni UE, dati Gartner | [ENISA 2024](https://www.enisa.europa.eu/sites/default/files/2024-11/CSPA%20-%20NIS%20Investments%20-%202024_0.pdf) |
| Sicurezza su spesa IT, entità NIS1 | mediana 6,7-7,7%, media 7,2-8,8% (2020-2022) | Operatori NIS1 | [ENISA 2021](https://www.enisa.europa.eu/sites/default/files/publications/ENISA%20Report%20-%20NIS%20Investments%202021.pdf), [2022](https://www.enisa.europa.eu/sites/default/files/publications/NIS%20Investments%202022.pdf), [2023](https://www.enisa.europa.eu/sites/default/files/publications/CSPA%20-%20NIS%20Investments%20-%202023.pdf) |
| Sicurezza su spesa IT, entità NIS2 | mediana 9% (2023 e 2024), media 9,6% (2023) e 9,3% (2024) | Settori NIS2 ad alta criticità, 83% grandi | [ENISA 2024](https://www.enisa.europa.eu/sites/default/files/2024-11/CSPA%20-%20NIS%20Investments%20-%202024_0.pdf), [ENISA 2025](https://www.enisa.europa.eu/sites/default/files/2025-12/NIS%20Investments%202025%20-%20Main%20report.pdf) |
| Sicurezza su spesa IT, PMI e grandi | 8,6% e 7% (edizione 2021) | Entità NIS1 | [ENISA 2021](https://www.enisa.europa.eu/sites/default/files/publications/ENISA%20Report%20-%20NIS%20Investments%202021.pdf) |
| Sicurezza su spesa IT, media | circa 8% (2025) | Europa, lato offerta | [PAC](https://sitsi.pacanalyst.com/le-marche-europeen-de-la-cybersecurite-une-croissance-sans-limite/) |
| Sicurezza su budget IT, media | 9,6% (2022) | 186 decisori europei | [VOICE con Metrics](https://www.voice-ev.org/wp-content/uploads/2022/02/VOICE-Metrics-Trendstudie-IT-Agenda-2022-DE-v1-1.pdf) |
| Cyber su budget IT, media | 11% (2025) | 1.500 PMI italiane | [Confindustria e Generali, Cyber Index PMI](https://www.confindustria.an.it/documenti/2026/03_Marzo/CyberIndexPMI2025_ExecutiveSummary.pdf) |
| Sicurezza su spesa IT, media | 10,9% (2025); 11,9% (2024, rivisto dal 13,2% pubblicato in precedenza); 26,1% sotto 50 Mln $ di ricavi contro 11,6% tra 600 Mln $ e 1 mld $ | CISO, prevalentemente nordamericani | [IANS e Artico 2025](https://sf-cdn.iansresearch.com/sitefinity/docs/default-source/reports/2025-security-budget-benchmark-summary-report_08_05_2025.pdf?sfvrsn=43097214_2) |
| Sicurezza su budget IT, media | 9% (2022), 14% (2023), 17% (2024), 18% (2025) | Imprese tedesche con 10+ addetti e almeno 1 Mln € di fatturato, quota stimata dal rispondente | [Bitkom Wirtschaftsschutz 2025](https://www.bitkom.org/sites/main/files/2025-12/bitkom-studienbericht-wirtschaftsschutz-2025.pdf) |
| Cyber su budget IT, distribuzione | le classi 3-5% e 6-10% raccolgono ciascuna il 19% dei rispondenti (2023) | Imprese austriache | [KPMG con KSÖ 2023](https://www.ruv.at/wp-content/uploads/kpmg-studie-cybersecurity-in-oesterreich-2023_1x1.pdf) |

Le differenze dipendono da tre fattori:
- **definizione del budget:** budget del CISO o spesa totale, uscite di cassa o costo totale;
- **statistica:** mediana o media di rapporti;
- **campione:** grandi entità o piccole imprese.

La quota sul budget IT tende a essere più alta nelle imprese piccole. La spesa assoluta per impresa cresce invece molto con la dimensione.

---

## 2. Le metodologie di stima più diffuse

### 2.1 Quadro d'insieme

| Famiglia di metodo | Chi la usa | Lato | Cosa produce | Riproducibilità |
|---|---|---|---|---|
| A. Somma dei ricavi dei vendor con ripartizione | IDC, Gartner, Canalys/Omdia, PAC; a valle Bitkom e Statista; Anitec-Assinform con un panel di fornitori | Offerta | Mercato per paese e segmento | Bassa |
| B. "Triangolazione" degli editori | Mordor, Grand View, MarketsandMarkets, IMARC, Fortune, Technavio, Ken Research, 6Wresearch | Per lo più non determinabile | Mercato per paese e segmento | Bassa |
| C. Censimento dei fornitori | DSIT, ACN Francia, Cyber Ireland, Dialogic, Agoria, INCIBE; variante da contabilità nazionale WifOR | Offerta | Ricavi, valore aggiunto e addetti dell'industria nazionale | Media per DSIT, ACN, Cyber Ireland, Dialogic, WifOR; bassa per Agoria e INCIBE |
| D. Survey agli utenti riportata all'universo | INE Spagna, Statistics Canada, Banca d'Italia Invind 2016, UK CSBS 2016-2019 | Domanda | Totali per settore e classe (INE, Statistics Canada); totale nazionale (Invind); medie e mediane per classe (CSBS) | Alta |
| E. Modello a rapporti | Valutazione d'impatto NIS2, Gartner per la spesa IT di settore, RTI per NIST (benefici, non spesa); struttura affine in Mordor e IMARC | Domanda | Spesa per settore da fatturato × intensità IT × quota sicurezza | Media |
| F. Approccio misto | Osservatorio Polimi; IDC Security Spending Guide (livello di offerta, allocazione con survey) | Misto | Mercato domestico | Bassa |

Riproducibilità indica se il calcolo si può rifare con dati e parametri pubblici. Non coincide con la Trasparenza A-D del database: quella valuta la pagina da cui è letto il singolo valore.

Tra le fonti che dichiarano un metodo, la famiglia A, con la variante B, è di gran lunga la più diffusa per il "mercato". Le famiglie D ed E misurano l'oggetto del modello SBS e sono le meno frequenti.

### 2.2 A. Somma dei ricavi dei vendor

- **IDC.** I tracker dei prodotti e dei servizi misurano i ricavi dei vendor ([Security Products Tracker](https://my.idc.com/getdoc.jsp?containerId=IDC_P38710), [Services Tracker](https://my.idc.com/getdoc.jsp?containerId=IDC_P33285)). La [Security Spending Guide](https://my.idc.com/getdoc.jsp?containerId=IDC_P33461) incrocia tecnologia, settore, dimensione e paese, con classi 1-9, 10-99, 100-499, 500-999 e 1.000+ che non coincidono con le classi SBS.
  - Per la ICT Spending Guide IDC dichiara di allocare i ricavi dei vendor al paese d'uso. Usa guidance dei vendor, analisti locali e survey agli utenti, con settori NACE Rev. 2 per l'Europa ([tassonomia 2022](https://pdfcoffee.com/idcx27s-worldwide-ict-spending-guide-enterprise-and-smb-by-industry-taxonomy-2022-release-v2-2022-2022-sep-pdf-free.html)).
  - Che lo stesso valga per la Security Spending Guide è una deduzione.
- **Gartner.** Secondo la metodologia generale, Gartner analizza le vendite di oltre mille vendor ([comunicato 2024](https://www.gartner.com/en/newsroom/press-releases/2024-11-07-gartner-forecasts--it-sending-in-europe-to-grow-9-percent-in-2025)). Nel metodo dichiarato per i servizi IT riconcilia i valori con dati di domanda.
  - Per il forecast sicurezza la nota metodologica non è pubblica: l'applicazione di questo metodo è dedotta.
  - Il valore pubblicato è una "spesa end user" che include il consumer.
- **Canalys/Omdia.** Stima trimestrale del valore venduto dai principali vendor in oltre 50 paesi, con ripartizione tra vendita diretta e canale ([Cybersecurity analysis](https://canalys.dev/site/analysis/cybersecurity+analysis)).
  - I valori sono presentati come spesa (end-user value) e riguardano solo le tecnologie, senza servizi.
  - Oltre il 90% della spesa avviene tramite o con partner. In generale il ricavo dei vendor, senza margini di canale, è inferiore alla spesa degli utenti (deduzione).
- **PAC.** Conta solo ricavi non captive e, nei dati SITSI, esclude l'hardware di sicurezza ([segmentazione PAC](https://sitsi.pacanalyst.com/wp-content/uploads/2023/11/PAC_Segmentation.pdf)).
  - Il metodo di stima dei volumi per paese non è pubblico; il lato offerta è dedotto dalla definizione.
  - Nei dati per Bitkom compare un hardware di sicurezza di 0,8 mld € di origine non dichiarata.
- **Statista Market Insights.** Ricavi dei vendor a prezzi del produttore senza IVA, con B2C, B2B e B2G insieme ([pagina Germania](https://www.statista.com/outlook/tmo/cybersecurity/germany), [nota metodologica](https://www.statista.com/outlook/methodology/)).
  - Combinazione top-down e bottom-up con una logica per segmento non pubblicata.
  - Ogni paese è stimato con indicatori come PIL e penetrazione di internet.
  - Previsioni con modelli ETS o ARIMA.
- **Anitec-Assinform con NetConsulting cube.** Panel di almeno 400 fornitori, più circa 5.000 interviste ad aziende utenti, che secondo il database servono a verificare le strategie ([Il Digitale in Italia 2024](https://www.anitec-assinform.it/kdocs/2146137/il_digitale_in_italia_2024.pdf)).
  - La definizione "spesa dell'utente finale al netto di IVA, personale interno e interscambio" vale per tutto il mercato digitale.
  - Per la cyber non c'è una nota specifica.

### 2.3 B. La "triangolazione" degli editori

Sono stati esaminati dieci editori: Statista, Mordor, Grand View, MarketsandMarkets, IMARC, Fortune, Technavio, Research and Markets, Ken Research e 6Wresearch.
- Sette o otto dichiarano nelle pagine metodologiche generali una triangolazione top-down e bottom-up, quasi sempre con interviste.
- Technavio e 6Wresearch la citano solo in forma generica.
- Research and Markets rimanda all'editore originale.

Nessuno pubblica parametri o pesi numerici. Alcuni pubblicano formule generiche senza valori:
- Fortune: attività × penetrazione × uso × prezzo;
- IMARC: un modello di spesa per le previsioni;
- Mordor: una catena lato domanda.

Il testo metodologico è identico tra report di settori lontanissimi per Fortune, Technavio, Ken Research e 6Wresearch. Grand View usa la stessa frase generica, ma nei report cyber verticali pubblica una tabella specifica.

Alcuni editori dichiarano una struttura lato domanda, sempre senza parametri:
- **Mordor, per l'Italia.** La spesa IT e digitale nazionale viene tradotta in un "demand pool" di sicurezza e poi riconciliata con controlli lato offerta ([Mordor Italia](https://www.mordorintelligence.com/industry-reports/italy-cybersecurity-market)).
- **IMARC, per l'Europa.** Le previsioni usano il budget di sicurezza IT per paese e settore × la spesa IT per paese; il metodo del livello dell'anno base non è dichiarato ([IMARC Europa](https://www.imarcgroup.com/europe-cybersecurity-market)).
- **Grand View, nei report cyber verticali.** Una tabella a quattro strati: organizzazioni indirizzabili, mercato servibile, utilizzatori attivi, monetizzazione.
- **Ken Research, per il Regno Unito.** Parte dai budget IT nazionali.

L'ancora dichiarata sono i ricavi dei fornitori solo per Statista e MarketsandMarkets.

Le pagine paese registrate nel database di norma non riportano il metodo, per questo hanno trasparenza D. Il testo metodologico sta nelle pagine generali o nei report a pagamento.

Rischi tipici:
- **incoerenze interne:** MarketsandMarkets dà per l'Europa 2025 29,8 mld USD in una pagina e 54,8 in un'altra;
- **circolarità:** Fortune usa Statista come database, Research and Markets rivende report di altri editori;
- **revisioni** a ogni edizione.

### 2.4 C. Censimento dei fornitori

La catena tipica è documentata per DSIT e Cyber Ireland, e in parte per ACN e Dialogic:
1. elenco delle imprese da registri, siti web, cluster e strumenti automatici;
2. collegamento a bilanci o microdati;
3. attribuzione di una quota cyber alle imprese diversificate;
4. calcolo di ricavi, valore aggiunto e addetti.

Le fonti si distinguono così:
- **DSIT:** 2.603 imprese nell'edizione 2026 ([DSIT 2026](https://www.gov.uk/government/publications/cyber-security-sectoral-analysis-2026/cyber-security-sectoral-analysis-2026)).
- **Cyber Ireland:** 632 imprese; la quota cyber delle imprese diversificate viene dal personale in ruoli cyber ([rapporto 2025](https://cyberireland.ie/wp-content/uploads/2025/06/PE-All-Island-Cyber-Security-Sector-Research-Report-FINAL.pdf)).
- **ACN Francia con DECISION:** 691 imprese che rappresentano l'85% del fatturato, con quota di attività stimata impresa per impresa ([Observatoire 2023](http://www.decision.eu/wp-content/uploads/2023/06/Observatoire-ACN-2023-de-la-confiance-nume%CC%81rique.pdf)). Misura la filiera della confiance numérique, di cui la cyber è circa la metà.
- **Dialogic:** fattori fissi per classe di addetti, circa 50%, 40% e 25% ([studio 2023](https://dialogic.nl/wp-content/uploads/2023/06/economische-kansen-van-de-cybersecuritysector-7.pdf)).
- **Agoria e INCIBE:** estrapolano da survey ai fornitori con un metodo non descritto.
- **WifOR:** applica coefficienti di sicurezza IT a intere classi WZ (la NACE tedesca) della contabilità nazionale. Mercato = produzione + importazioni − export: 26,8 mld € nel 2017, con un perimetro molto ampio ([studio 2019](https://www.wifor.com/uploads/2019/08/it-sicherheitsmarkt-in-deutschland-studie-2019.pdf)).

Il passaggio più fragile è la quota cyber delle imprese diversificate, stimata da ciascuno in modo diverso. Questi studi misurano l'industria, non la domanda domestica.

### 2.5 D. Survey agli utenti riportata all'universo

| Fonte | Disegno | Perimetro | Risultato utile |
|---|---|---|---|
| [INE Spagna, ETICCE](https://www.ine.es/metodologia/t09/eticce1_24.pdf) | Statistica ufficiale annuale; stimatori di espansione corretti per la mancata risposta; imputazione con la mediana dello strato ([metodologia](https://www.ine.es/daco/daco42/comele/meto_eticce.pdf)) | Imprese con 10+ addetti delle sezioni CNAE (la NACE spagnola) C-J e L-N più il gruppo 95.1; tabelle di spesa senza 56, 64-66 e 95.1; personale interno incluso | 3.993 Mln € nel 2023 ([tabella](https://ine.es/jaxi/files/tpx/en/xlsx/73522.xlsx)): 957 Mln € nella classe 10-49, 883 nella 50-249, 2.153 (54%) nella 250+. 4.513 Mln € nel 2024 ([tabella](https://www.ine.es/jaxi/files/tpx/csv_bd/76408.csv)) |
| [Banca d'Italia, Invind 2016](https://www.bancaditalia.it/pubblicazioni/qef/2017-0407/QEF_407.pdf) | Survey stratificata; imputazione con modello sulla spesa per addetto; winsorizzazione per classe | Imprese con 20+ addetti dell'industria e dei servizi non finanziari; PA esclusa; personale interno incluso | Totale 570-780 Mln €. Spesa per addetto: mediana 90,9 €, media 142,7 €. Mediana per impresa: 4.530 € (3.120 € nelle piccole, 44.590 € nelle grandi). Nel biennio 2021-2022 il 22,8% delle imprese non ha speso nulla ([Invind 2022](https://www.bancaditalia.it/pubblicazioni/indagine-imprese/2022-indagini-imprese/statistiche_IIS_30062023.pdf)) |
| [UK CSBS 2016-2019](https://assets.publishing.service.gov.uk/media/5ff5c7278fa8f53b790e7363/Cyber_Security_Breaches_Survey_2019_-_Technical_Annex_V2.pdf) | Campione casuale dal registro delle imprese, ponderazione per dimensione e settore | Imprese private con più di una persona a libro paga; personale interno incluso | Medie e mediane per classe, con micro e piccole insieme (1-49); circa un terzo delle imprese a spesa zero; nessun totale nazionale; domanda abbandonata nel 2020 |
| [Statistics Canada, CSCSC](https://www23.statcan.gc.ca/imdb/p2SV.pl?Function=getSurvey&Id=1580450) | Registro d'imprese, strati per settore e classe (10-49, 50-249, 250+), pesi | Imprese con 10+ addetti; PA esclusa fino al 2023, unità federali incluse dal 2025 | Totali per dimensione e voce di spesa. È il disegno che un modello SBS imita |

Eurostat, Destatis, Statistik Austria e CBS rilevano l'adozione di misure di sicurezza, non la spesa ([Eurostat, ICT security in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=ICT_security_in_enterprises)). Per l'INE va considerata una rottura di serie: dal 2022-2023 l'unità di rilevazione è l'impresa statistica.

### 2.6 E. Modello a rapporti

**Valutazione d'impatto NIS2 della Commissione (SWD(2020) 345).** È il precedente applicato più vicino al modello SBS ([allegato](https://www.eerstekamer.nl/bijlage/20210114/swd_2020_345_impact_assessment_7/document3/f=/vlfghch5jfhz.pdf)).
- Catena: spesa ICT pari al 5,69% del fatturato × sicurezza pari al 9,14% della spesa ICT = 0,52% del fatturato per settore nel 2020.
- Dopo la NIS2 la stima sale a circa l'11% della spesa ICT e allo 0,63% del fatturato.
- I parametri sono ipotesi derivate da previsioni Gartner, non misure UE, e non distinguono le classi dimensionali.

**Altri precedenti.**
- **Gartner, spesa IT per settore:** ricavi del settore × quota destinata all'IT, comprese le spese per personale IT interno. Non è applicato alla sicurezza.
- **RTI per NIST (2013):** valore per dollaro di ricavo × ricavi d'industria del Census × intensità IT relativa del settore ([rapporto 13-1](https://www.nist.gov/system/files/documents/2017/05/09/report13-1.pdf)).
  - Stima i benefici di un miglioramento della sicurezza, non la spesa, ma la catena di estrapolazione è la stessa.
  - Gli autori avvertono che l'intensità IT riflette uso dell'IT e dimensione, non il rischio.
- **Forrester:** in un [blog del 2012](https://www.forrester.com/blogs/12-09-30-is_the_us_bureau_of_economic_analysis_undermeasuring_the_tech_economy/) un analista dichiara di dimensionare il mercato tech USA partendo dagli investimenti delle imprese nei conti nazionali. Il software interno è contato tramite i costi dello staff IT.
- **Mordor e IMARC:** usano una struttura affine (spesa IT × quota sicurezza) senza parametri.

Nessuna fonte applica questa catena in modo trasparente per settore e classe dimensionale.

### 2.7 F. Approccio misto: l'Osservatorio Polimi

"Triplice prospettiva" ([scenario 2025](https://www.osservatori.net/report/cybersecurity-data-protection/scenario-cybersecurity-2025/)):
- interviste a oltre 100 vendor (top-down);
- survey a grandi organizzazioni (145 nel 2025) e a PMI (1.582 nel 2025) sulla spesa e sul budget cyber (bottom-up);
- confronto con studi esterni.

Non è pubblicato come si combinano le componenti.

Composizione 2024: soluzioni 37%, servizi 41%, formazione 14%, polizze 8% (valori letti da grafico). Le grandi imprese pesano oltre tre quarti della spesa ([comunicato 2023](https://www.osservatori.net/comunicato/cybersecurity-data-protection/cybersecurity-italia-mercato-crescita-2023/)). Questa quota comprende grandi organizzazioni pubbliche e finanziarie. In Spagna le imprese con 250+ addetti valgono il 54% della spesa delle imprese 10+.

### 2.8 Quadri metodologici e letteratura

- **ENISA ECSMAF.**
  - La versione 1 pone come base della dimensione del mercato i ricavi della mappa dei fornitori ([ECSMAF V1](https://www.enisa.europa.eu/sites/default/files/publications/WP%202021%20O.7.1%20-%20Market%20Analysis%20Framework.pdf)).
  - La versione 3.0 descrive sette passi e indicatori proxy, con un questionario che chiede quota di fatturato cyber ai fornitori e budget cyber in percentuale del fatturato alle organizzazioni ([ECSMAF V3.0](https://www.enisa.europa.eu/sites/default/files/2026-03/ENISA%20Cybersecurity%20Market%20Analysis%20Framework%20(ECSMAF)%20%E2%80%93%20V3.0.pdf)).
  - Nessuna delle due dà un algoritmo di dimensionamento.
- **Commissione, DG HOME.** Combinazione di metodi, due estrapolazioni come limite inferiore e superiore, punto medio ([studio sulle statistiche della sicurezza](https://home-affairs.ec.europa.eu/system/files/2020-09/security_statistics_-_final_report_en.pdf)).
- **OCSE.**
  - Le indagini ICT non forniscono indicatori economici come gli investimenti in sicurezza ([2012](https://www.oecd.org/content/dam/oecd/en/publications/reports/2012/12/improving-the-evidence-base-for-information-security-and-privacy-policies_g17a2217/5k4dq3rkb19n-en.pdf)).
  - Checklist per indicatori con metodologia tracciabile ([2024](https://www.oecd.org/content/dam/oecd/en/publications/reports/2024/06/new-perspectives-on-measuring-cybersecurity_6069c1b9/b1e31997-en.pdf)).
- **RAND.** [Estimating the Global Cost of Cyber Risk](https://www.rand.org/content/dam/rand/pubs/research_reports/RR2200/RR2299/RAND_RR2299.pdf) (2018) è un modello input-output del costo del rischio cyber, non della spesa. Con tre set di parametri ottiene costi diretti tra 275 miliardi e 6,6 trilioni di dollari.
- **Classificazioni.** La cybersecurity non ha un codice nelle classificazioni NACE e PRODCOM. Per questo il lato offerta richiede di identificare le imprese una per una, oppure di stimare coefficienti di rilevanza su classi intere, come fa WifOR.

---

## 3. Implicazioni per il modello SBS (Italia, Germania, Austria)

### 3.1 Struttura

```
Spesa_cyber[n,s] = Fatturato_SBS[n,s] × (Spesa_IT / Fatturato)[n,s] × (Spesa_cyber / Spesa_IT)[n,s]
```

Con n = settore NACE e s = classe dimensionale.

- **Spesa_IT** è la spesa IT totale con il personale IT interno, come in ENISA e Gartner. Ogni rapporto cyber/IT va annotato con il suo denominatore. Quelli su base diversa (per esempio CIPA, sulle uscite di cassa) vanno usati solo come intervallo.
- **Alternativa o controllo:** Fatturato_SBS × (Spesa_cyber / Fatturato) diretto.
- **Microimprese:** conviene un valore per impresa o per addetto, perché la quota sul fatturato è instabile.
- **Imprese a spesa zero.**
  - Correzione necessaria quando il parametro viene da campioni di organizzazioni che hanno un budget di sicurezza (ENISA, IANS, survey ai CISO). In quel caso va applicato solo alla quota di imprese che spendono: circa due terzi secondo la CSBS, circa il 77% delle imprese 20+ secondo Invind 2022.
  - Nessuna correzione per i rapporti aggregati (INE) e per le medie CSBS, che includono già gli zeri.

### 3.2 Parametri e calibrazione

| Parametro | Fonte | Uso consigliato | Cautela |
|---|---|---|---|
| Spesa IT su fatturato per settore e classe | INE ETICCE 2021 (voci K.1-K.4: spesa TIC totale e in sicurezza per classe); valutazione d'impatto NIS2 (5,69% del fatturato, ipotesi Gartner); ENISA 2025, IT su ricavi per Stato | Termine centrale della catena | Va verificato se nell'ETICCE la voce di sicurezza è compresa nelle voci TIC o si aggiunge. ENISA vale solo per entità NIS. L'intensità IT non misura il rischio |
| Spesa cyber su fatturato per settore e classe | INE Spagna 2023-2024 diviso per il fatturato SBS spagnolo delle stesse celle | Punto di partenza per IT, DE e AT, da correggere | Il rapporto va calcolato: INE non lo pubblica. Stesso perimetro: 10+ addetti, senza CNAE 56, 64-66 e 95.1 |
| Spesa per addetto e totale Italia | Banca d'Italia Invind 2016 | Punto storico per l'Italia, imprese 20+ | Limite inferiore dichiarato dagli autori. Da indicizzare dichiarandolo, per esempio con la crescita delle serie italiane: Anitec circa ×2,2 dal 2017 al 2024, Polimi circa ×2,3 |
| Quota cyber su IT, grandi imprese NIS | ENISA NIS Investments: media 9,3% e mediana 9% (dati 2024) | Solo per le celle 250+ dei settori NIS2; media come valore centrale, mediana come limite basso | Campione non proporzionale e non ponderato; rottura tra campione NIS1 e NIS2 |
| Quota cyber su IT, PMI italiane | Confindustria e Generali, Cyber Index PMI (11% nel 2025) | Celle italiane 10-249 | Media di quote dichiarate |
| Quota cyber su IT, imprese tedesche | Bitkom Wirtschaftsschutz (18% nel 2025) | Limite superiore per le celle tedesche 10-249, non sull'aggregato | Media di quote stimate dal rispondente, probabilmente dominata dalle piccole imprese (ponderazione non dichiarata dopo il 2022). Salita da 9% a 18% in tre anni, con possibile ancoraggio al 20% raccomandato da BSI e Bitkom |
| Scenario centrale della quota cyber su IT | PAC Europa circa 8%, ENISA 9-9,6%, VOICE 9,6%, Confindustria PMI 11% | Intervallo 8-12% | Sono medie di quote con denominatori diversi |
| Spesa per impresa, Mittelstand tedesco | Deloitte 2020: media 80.050 €, 40% delle imprese sotto 10.000 € ([studio](https://it-sicherheit.de/wp-content/uploads/2024/09/Deloitte_Studie_Cybersecurity_im_Mittelstand.pdf)) | Controllo per impresa per la Germania | Campione di medie imprese; un solo anno |
| Spesa delle micro e quota a spesa zero | UK CSBS 2016-2019; Invind 2022 per l'Italia | Ordine di grandezza per la classe 1-49 nel suo insieme; quota a spesa zero | La CSBS non separa 0-9 e 10-49 ed esclude le imprese senza dipendenti; è fuori UE e ha varianza altissima |
| Quota cyber su IT, banche italiane | CIPA: 4,9% delle uscite di cassa IT, 365,7 Mln € per 23 gruppi nel 2024 | Solo se il modello copre la finanza | Solo banche; denominatore diverso |
| Propensione alla sicurezza per settore e classe | Eurostat, modulo ICT security; Statistik Austria, IKT-Sicherheit | Indice relativo per modulare i rapporti tra settori e classi | Non contiene spesa |
| Quota del personale interno | 25% (CIPA), circa 37% (ENISA 2020-2021), 39% (IANS 2025) | Passaggio da spesa totale a spesa esterna | Varia per dimensione e settore |

### 3.3 Perimetro da dichiarare

- **Due output.**
  - Spesa totale con personale interno, confrontabile con ENISA, INE, Banca d'Italia e CSBS.
  - Spesa esterna in hardware, software e servizi, circa il 60-75% del totale. È confrontabile con Anitec-Assinform e con i mercati degli analisti. Con Polimi e Bitkom il confronto va fatto con cautela: il personale interno non è dichiarato e Polimi include le polizze.
- **Settori fuori SBS.** Nel 2024, in Italia, valgono circa il 48% della spesa Anitec-Assinform: 961 su 2.001 Mln € (calcolo; [Il Digitale in Italia 2025](https://lentepubblica.it/wp-content/uploads/2025/07/ANITEC-ASSINFORM_il_digitale_in_italia_2025_v5-compresso.pdf)).
  - banche: 433,7 Mln €;
  - assicurazioni e finanziarie: 113,6 Mln €;
  - PA: 341,9 Mln €;
  - sanità: 72,1 Mln €.

  La parte confrontabile con un modello sulle imprese SBS è quindi circa 1,04 mld €. Va verificata nei metadati della versione SBS usata la copertura delle sezioni K, O, P e Q.
- **Voci da decidere esplicitamente.**
  - formazione: 14% della spesa Polimi 2024; inclusa da Anitec negli "Altri servizi";
  - polizze cyber: 8% della spesa Polimi 2024, 2,5% nel 2017;
  - hardware di sicurezza: escluso dai dati SITSI di PAC, presente per 0,8 mld € nella serie Bitkom;
  - consumer.

### 3.4 Controlli incrociati per paese

- **Italia.** Confrontare l'output "spesa esterna" del modello con Anitec-Assinform e Polimi, al netto di finanza, PA e sanità. Per Polimi togliere anche le polizze: senza polizze il valore 2024 scende a circa 2.280 Mln € (calcolo). Polimi non pubblica la ripartizione per settore, quindi si applicano le quote Anitec, dichiarandolo.
- **Germania.**
  - Confrontare l'output "spesa esterna" con la serie Bitkom-PAC: riferimento principale il consuntivo 2024 (10,1 mld €), il 2025 (11,1 mld €) solo come stima.
  - Prima togliere dal valore Bitkom le componenti fuori SBS (PA, istruzione e sanità pubbliche, finanza, eventuale consumer), con quote dichiarate come ipotesi. Il modello deve risultare inferiore.
  - Non mescolare edizioni con dati IDC e PAC.
- **Austria.** Nessun totale nazionale. Usare come vincoli:
  - la distribuzione KPMG del rapporto cyber/IT (le classi 3-5% e 6-10% raccolgono ciascuna il 19% dei rispondenti nel 2023);
  - la distribuzione EY 2026 per importo: 6% senza budget, 41% sotto 25.000 €, 32% non sa ([EY](https://www.ey.com/de_at/insights/cybersecurity/ey-cybersecurity-studie)).

  Trasferire da Germania e Italia solo rapporti per classe, corretti con l'indagine IKT-Sicherheit di Statistik Austria.
- **Spagna come banco di prova, evitando la circolarità.** Due strade:
  - calibrare su INE 2023 e validare su INE 2024 o sulla ripartizione per classe;
  - stimare la catena con parametri non INE (ENISA, valutazione d'impatto NIS2, Confindustria) e confrontarla con INE.

  Se il modello usa il rapporto INE/fatturato, applicato alla Spagna riproduce INE per costruzione.

### 3.5 Incertezza

Presentare il risultato come forbice tra uno scenario basso e uno alto, come lo studio DG HOME (due metodi e punto medio). Documentare parametri, fonti e passaggi per ogni cella: è proprio ciò che manca agli editori.

### 3.6 Da evitare

- Usare i valori degli editori come obiettivo di calibrazione: non sono riproducibili e cambiano a ogni edizione.
- Usare le quote paese degli editori per ripartire un totale europeo.
- Moltiplicare mediane ENISA per il numero di imprese, o sommare mediane.
- Applicare medie di rapporti per impresa (Bitkom, IANS) al fatturato aggregato senza ponderazione.
- Confrontare la spesa con personale interno con i mercati dei fornitori.
- Usare i ricavi dell'industria nazionale come spesa domestica senza togliere l'export e aggiungere le importazioni.
- Mescolare edizioni diverse della stessa serie: Bitkom con dati IDC e con dati PAC; Gartner prima e dopo il 2018.

---

## 4. Limiti di questa analisi

- **Accesso alle fonti.** L'ambiente di esecuzione bloccava l'apertura diretta delle pagine. Valori e citazioni sono stati letti negli estratti testuali delle pagine indicate, restituiti da un motore di ricerca. Valori letti da grafici vanno ricontrollati sul documento.
- **Verifica.**
  - Nel database sono state riaperte le fonti di 565 righe: 545 confermate, 8 corrette, 10 non ritrovate, 2 rimosse.
  - Per le metodologie, 75 affermazioni chiave sono state ricontrollate: 63 confermate, 8 contraddette, 4 non supportate.
  - Questo documento è stato poi rivisto da tre revisori indipendenti (numeri, metodologie, chiarezza). Le correzioni sostanziali sono incluse.
- **Classificazioni del database da riallineare.** Alcune schede registrano la trasparenza della pagina paese, non quella della metodologia generale dell'editore: Mordor Italia ha trasparenza D, anche se la pagina metodologica descrive una catena. Le due schede IMARC Europa (IMARC-CYBEREU-2026 e IMARC-CYBEREUR-2026) hanno classificazioni diverse.
- **Note a pagamento.** Le note metodologiche di dettaglio di IDC, Gartner, Forrester e PAC sono a pagamento. Qui sono descritte solo le parti pubbliche.
- **Deduzioni.** Dove una caratteristica non è dichiarata dalla fonte, il testo lo indica come deduzione.

## Fonti principali citate

**Database**
- `fonti_mercato_cyber_UE_UK_2026-10-08.xlsx`, fogli Dati, Fonti_Metodologie, Copertura_Paesi, Ricerche_senza_esito, Cambi.

**Analisti e editori**
- IDC: [Security Products Tracker](https://my.idc.com/getdoc.jsp?containerId=IDC_P38710), [Services Tracker](https://my.idc.com/getdoc.jsp?containerId=IDC_P33285), [Security Spending Guide](https://my.idc.com/getdoc.jsp?containerId=IDC_P33461), [tassonomia ICT Spending Guide 2022](https://pdfcoffee.com/idcx27s-worldwide-ict-spending-guide-enterprise-and-smb-by-industry-taxonomy-2022-release-v2-2022-2022-sep-pdf-free.html)
- Gartner: [forecast sicurezza 2018](https://www.gartner.com/en/newsroom/press-releases/2018-08-15-gartner-forecasts-worldwide-information-security-spending-to-exceed-124-billion-in-2019), [IT spending Europa 2024](https://www.gartner.com/en/newsroom/press-releases/2024-11-07-gartner-forecasts--it-sending-in-europe-to-grow-9-percent-in-2025)
- Canalys: [Cybersecurity analysis](https://canalys.dev/site/analysis/cybersecurity+analysis)
- PAC: [segmentazione SITSI](https://sitsi.pacanalyst.com/wp-content/uploads/2023/11/PAC_Segmentation.pdf), [mercato europeo](https://sitsi.pacanalyst.com/le-marche-europeen-de-la-cybersecurite-une-croissance-sans-limite/)
- Forrester: [blog 2012 sul dimensionamento del mercato tech USA](https://www.forrester.com/blogs/12-09-30-is_the_us_bureau_of_economic_analysis_undermeasuring_the_tech_economy/)
- Statista: [Cybersecurity Germania](https://www.statista.com/outlook/tmo/cybersecurity/germany), [metodologia Market Insights](https://www.statista.com/outlook/methodology/)
- Mordor: [Italia](https://www.mordorintelligence.com/industry-reports/italy-cybersecurity-market), [Austria](https://www.mordorintelligence.com/de/industry-reports/austria-cybersecurity-market)
- IMARC: [Europa](https://www.imarcgroup.com/europe-cybersecurity-market)
- MarketsandMarkets: [Italia](https://www.marketsandmarkets.com/Market-Reports/geography/cyber-security-market/italy)
- Grand View Research: [Germania](https://www.grandviewresearch.com/horizon/outlook/cyber-security-market/germany), [metodologia](https://www.grandviewresearch.com/info/research-methodology)
- Ken Research: [Italia](https://www.kenresearch.com/italy-cybersecurity-and-mssp-market)

**Fonti nazionali e di settore**
- Osservatorio Polimi: [comunicato 2026](https://www.osservatori.net/comunicato/cybersecurity-data-protection/cybersecurity-italia-mercato-crescita/), [scenario 2025](https://www.osservatori.net/report/cybersecurity-data-protection/scenario-cybersecurity-2025/), [scheda MAECI](https://www.esteri.it/wp-content/uploads/2025/05/cyber_sp.pdf)
- Anitec-Assinform: [Il Digitale in Italia 2024](https://www.anitec-assinform.it/kdocs/2146137/il_digitale_in_italia_2024.pdf), [2025](https://lentepubblica.it/wp-content/uploads/2025/07/ANITEC-ASSINFORM_il_digitale_in_italia_2025_v5-compresso.pdf), [2026](https://www.matricedigitale.it/wp-content/uploads/2026/07/Rapporto-Anitec-Assinform_Il-Digitale-in-Italia-2026.pdf)
- Confindustria e Generali: [Cyber Index PMI 2025](https://www.confindustria.an.it/documenti/2026/03_Marzo/CyberIndexPMI2025_ExecutiveSummary.pdf)
- Bitkom: [mercato 2024](https://www.bitkom.org/Presse/Presseinformation/Erstmals-mehr-als-10-Milliarden-Euro-fuer-Deutschlands-Cybersicherheit), [mercato 2025](https://www.bitkom.org/sites/main/files/2025-10/bitkom-charts-cybercrime-und-der-markt-fuer-it-sicherheit-2025.pdf), [Wirtschaftsschutz 2025](https://www.bitkom.org/sites/main/files/2025-12/bitkom-studienbericht-wirtschaftsschutz-2025.pdf)
- Deloitte: [Cyber Security im Mittelstand](https://it-sicherheit.de/wp-content/uploads/2024/09/Deloitte_Studie_Cybersecurity_im_Mittelstand.pdf)
- VOICE con Metrics: [IT-Agenda 2022](https://www.voice-ev.org/wp-content/uploads/2022/02/VOICE-Metrics-Trendstudie-IT-Agenda-2022-DE-v1-1.pdf)
- KPMG con KSÖ: [Cybersecurity in Österreich 2023](https://www.ruv.at/wp-content/uploads/kpmg-studie-cybersecurity-in-oesterreich-2023_1x1.pdf); EY: [Cybersecurity-Studie Österreich](https://www.ey.com/de_at/insights/cybersecurity/ey-cybersecurity-studie)
- CIPA: [rilevazione economica 2024](https://www.cipa.it/rilevazioni/economiche/2024/Rilevazione_economica_2024.pdf)
- DSIT: [Cyber security sectoral analysis 2026](https://www.gov.uk/government/publications/cyber-security-sectoral-analysis-2026/cyber-security-sectoral-analysis-2026)
- ACN Francia: [Observatoire 2023](http://www.decision.eu/wp-content/uploads/2023/06/Observatoire-ACN-2023-de-la-confiance-nume%CC%81rique.pdf)
- Cyber Ireland: [All-Island report 2025](https://cyberireland.ie/wp-content/uploads/2025/06/PE-All-Island-Cyber-Security-Sector-Research-Report-FINAL.pdf)
- Dialogic: [settore cyber olandese 2023](https://dialogic.nl/wp-content/uploads/2023/06/economische-kansen-van-de-cybersecuritysector-7.pdf)
- WifOR: [IT-Sicherheitsmarkt 2019](https://www.wifor.com/uploads/2019/08/it-sicherheitsmarkt-in-deutschland-studie-2019.pdf)

**Survey lato domanda e statistiche ufficiali**
- ENISA NIS Investments: [2021](https://www.enisa.europa.eu/sites/default/files/publications/ENISA%20Report%20-%20NIS%20Investments%202021.pdf), [2022](https://www.enisa.europa.eu/sites/default/files/publications/NIS%20Investments%202022.pdf), [2023](https://www.enisa.europa.eu/sites/default/files/publications/CSPA%20-%20NIS%20Investments%20-%202023.pdf), [2024](https://www.enisa.europa.eu/sites/default/files/2024-11/CSPA%20-%20NIS%20Investments%20-%202024_0.pdf), [2025](https://www.enisa.europa.eu/sites/default/files/2025-12/NIS%20Investments%202025%20-%20Main%20report.pdf)
- INE: [questionario ETICCE 2024](https://www.ine.es/metodologia/t09/eticce1_24.pdf), [metodologia](https://www.ine.es/daco/daco42/comele/meto_eticce.pdf), [tabella 2023](https://ine.es/jaxi/files/tpx/en/xlsx/73522.xlsx), [tabella 2024](https://www.ine.es/jaxi/files/tpx/csv_bd/76408.csv)
- Banca d'Italia: [QEF 407, Invind 2016](https://www.bancaditalia.it/pubblicazioni/qef/2017-0407/QEF_407.pdf), [Invind 2022](https://www.bancaditalia.it/pubblicazioni/indagine-imprese/2022-indagini-imprese/statistiche_IIS_30062023.pdf)
- UK CSBS: [allegato tecnico 2019](https://assets.publishing.service.gov.uk/media/5ff5c7278fa8f53b790e7363/Cyber_Security_Breaches_Survey_2019_-_Technical_Annex_V2.pdf)
- Statistics Canada: [CSCSC](https://www23.statcan.gc.ca/imdb/p2SV.pl?Function=getSurvey&Id=1580450)
- Eurostat: [ICT security in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=ICT_security_in_enterprises)
- IANS e Artico: [Security Budget Benchmark 2025](https://sf-cdn.iansresearch.com/sitefinity/docs/default-source/reports/2025-security-budget-benchmark-summary-report_08_05_2025.pdf?sfvrsn=43097214_2)

**Quadri metodologici e letteratura**
- Commissione europea: [valutazione d'impatto NIS2, SWD(2020) 345](https://www.eerstekamer.nl/bijlage/20210114/swd_2020_345_impact_assessment_7/document3/f=/vlfghch5jfhz.pdf)
- ENISA: [ECSMAF V1](https://www.enisa.europa.eu/sites/default/files/publications/WP%202021%20O.7.1%20-%20Market%20Analysis%20Framework.pdf), [ECSMAF V3.0](https://www.enisa.europa.eu/sites/default/files/2026-03/ENISA%20Cybersecurity%20Market%20Analysis%20Framework%20(ECSMAF)%20%E2%80%93%20V3.0.pdf)
- Commissione europea, DG HOME: [statistiche sull'industria della sicurezza](https://home-affairs.ec.europa.eu/system/files/2020-09/security_statistics_-_final_report_en.pdf)
- OCSE: [2012](https://www.oecd.org/content/dam/oecd/en/publications/reports/2012/12/improving-the-evidence-base-for-information-security-and-privacy-policies_g17a2217/5k4dq3rkb19n-en.pdf), [2024](https://www.oecd.org/content/dam/oecd/en/publications/reports/2024/06/new-perspectives-on-measuring-cybersecurity_6069c1b9/b1e31997-en.pdf)
- RTI per NIST: [Planning Report 13-1](https://www.nist.gov/system/files/documents/2017/05/09/report13-1.pdf)
- RAND: [Estimating the Global Cost of Cyber Risk](https://www.rand.org/content/dam/rand/pubs/research_reports/RR2200/RR2299/RAND_RR2299.pdf)
