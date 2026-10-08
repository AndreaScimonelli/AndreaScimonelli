# Mercato e spesa in cybersecurity in UE e Regno Unito: conclusioni e metodologie di stima

Data: 8 ottobre 2026. Base: il database `fonti_mercato_cyber_UE_UK_2026-10-08.xlsx` (1.215 dati, 406 schede fonte, 158 ricerche senza esito), più una ricerca sulle metodologie dichiarate da 5 famiglie di produttori di stime, con verifica avversariale delle affermazioni chiave. I valori in euro di fonti in altra valuta sono convertiti con le medie annue dei cambi BCE del foglio `Cambi`.

## Sintesi

- **Nessun paese UE ha una misura ufficiale del mercato domestico della cybersecurity.** Quasi tutti i "mercati" pubblicati sono costruiti dal lato dei fornitori oppure non dichiarano il metodo.
- **Numeri con lo stesso nome misurano tre oggetti diversi:** mercato dei fornitori, ricavi dell'industria nazionale e spesa delle organizzazioni. Gran parte della dispersione tra fonti è una differenza di perimetro.
- **La metodologia più diffusa** è la somma dei ricavi dei vendor, poi ripartita per paese, settore e dimensione con survey o indicatori macro. Gli editori di ricerche di mercato dichiarano quasi tutti una "triangolazione top-down e bottom-up" senza parametri.
- **La metodologia più vicina all'oggetto del modello SBS** (spesa delle imprese utilizzatrici) è la meno diffusa: survey alle imprese riportata all'universo, oppure modello a rapporti fatturato × intensità IT × quota sicurezza.
- **Per il modello SBS** conviene calibrare sui pochi totali lato domanda riportati all'universo (INE Spagna, Banca d'Italia 2016, UK CSBS), produrre due numeri (con e senza personale interno), allineare il perimetro prima di ogni confronto e presentare il risultato come forbice.

---

## 1. Cosa dice il database

### 1.1 Trasparenza e lato della stima

| Indicatore | Valore |
|---|---|
| Fonti con valori di mercato, spesa o ricavi | 265 |
| di cui con approccio "Non dichiarato" | 140 |
| di cui "Ripreso da altra fonte" | 52 |
| di cui con trasparenza C (solo testo generico) o D (nessuna metodologia) | 211 |
| Righe di mercato domestico totale | 514 |
| di cui costruite dal lato domanda | 5 |
| Lato prevalente per fonte: Offerta / Domanda / Misto / Non determinabile | 85 / 33 / 16 / 131 |

Le fonti lato domanda misurano quasi sempre valori per singola organizzazione (mediane, medie, quote del budget IT). Pochissime riportano un totale all'universo delle imprese.

### 1.2 Tre famiglie di numeri non confrontabili

| Famiglia | Esempi | Cosa misura | Personale interno | Export |
|---|---|---|---|---|
| Mercato dei fornitori | IDC, Gartner, PAC per Bitkom, Anitec-Assinform, Statista, editori | Vendite di prodotti e servizi di sicurezza ai clienti del paese | Escluso | Escluso |
| Ricavi dell'industria nazionale | DSIT (UK), ACN (Francia), Agoria (Belgio), Cyber Ireland, INCIBE (Spagna), WifOR (Germania), Dialogic (Paesi Bassi) | Fatturato cyber dei fornitori con sede nel paese | Escluso | Incluso |
| Spesa delle organizzazioni | ENISA NIS Investments, UK Cyber Security Breaches Survey, INE, Banca d'Italia, Bitkom Wirtschaftsschutz | Spesa o quota di budget dichiarata dagli utenti | Incluso, tra 25% e 39% della spesa | Non pertinente |

Esempio della distanza tra famiglie. Per il Regno Unito DSIT stima 14,7 mld £ di ricavi del settore cyber nell'edizione 2026, con 8,6 mld £ di export nel 2024 ([DSIT 2026](https://www.gov.uk/government/publications/cyber-security-sectoral-analysis-2026/cyber-security-sectoral-analysis-2026)). Gli editori stimano il mercato domestico britannico tra 11,6 e 20,3 mld USD.

### 1.3 Dispersione per i paesi del modello (anno 2025)

| Paese | Fonte | Valore pubblicato | Mln € | Lato | Note di perimetro |
|---|---|---|---|---|---|
| Italia | [Anitec-Assinform 2026](https://www.matricedigitale.it/wp-content/uploads/2026/07/Rapporto-Anitec-Assinform_Il-Digitale-in-Italia-2026.pdf) | 2.245 Mln € | 2.245 | Offerta | Imprese e PA, al netto di IVA e personale interno |
| Italia | [Osservatorio Polimi 2026](https://www.osservatori.net/comunicato/cybersecurity-data-protection/cybersecurity-italia-mercato-crescita/) | 2,78 mld € | 2.780 | Misto | Imprese e PA; il framework include formazione e cyber insurance |
| Italia | [Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/italy-cybersecurity-market) | 4,1 mld USD | 3.646 | Non determinabile | Metodo dichiarato senza parametri |
| Italia | [MarketsandMarkets](https://www.marketsandmarkets.com/Market-Reports/geography/cyber-security-market/italy) | 5,72 mld USD | 5.063 | Non determinabile | Pagina paese con testo del report globale |
| Germania | [Statista, infografica](https://de.statista.com/infografik/36097/geschaetzter-weltweiter-umsatz-mit-cyber-security/) | 7 mld € | 7.000 | Offerta | B2C, B2B e B2G a prezzi dei vendor |
| Germania | [Bitkom con dati PAC](https://www.bitkom.org/sites/main/files/2025-10/bitkom-charts-cybercrime-und-der-markt-fuer-it-sicherheit-2025.pdf) | 11,1 mld € (stima) | 11.100 | Offerta | Software 4,8, servizi 5,6, hardware 0,8 mld €; clienti inclusi non dichiarati |
| Germania | [Grand View Research](https://www.grandviewresearch.com/horizon/outlook/cyber-security-market/germany) | 15,1 mld USD | 13.365 | Non determinabile | Hardware al 52,7%, contro circa 7% in Bitkom |
| Austria | [Mordor Intelligence](https://www.mordorintelligence.com/de/industry-reports/austria-cybersecurity-market) | 560 Mln USD | 496 | Non determinabile | Nessuna fonte nazionale pubblica un totale |

In Italia la distanza tra Anitec-Assinform e Polimi è stabile nel tempo (2023: 1.788 contro 2.150 Mln €; 2024: 2.001 contro 2.480 Mln €) ed è spiegabile con il perimetro. Le stime degli editori sono più alte e cambiano molto tra edizioni e tra pagine dello stesso sito.

### 1.4 Rotture di serie

- **Bitkom** passa da dati IDC a dati PAC. Il valore 2024 scende da 11,2 mld € ([ottobre 2024](https://www.bitkom.org/Presse/Presseinformation/Erstmals-mehr-als-10-Milliarden-Euro-fuer-Deutschlands-Cybersicherheit)) a 10,1 mld € ([ottobre 2025](https://www.bitkom.org/sites/main/files/2025-10/bitkom-charts-cybercrime-und-der-markt-fuer-it-sicherheit-2025.pdf)). Le due serie non vanno mescolate.
- **Polimi** ha rivisto il 2021 da 1,55 mld € a 1,576 mld € nelle edizioni successive.
- **Gartner** ha cambiato base nel 2018, passando dai ricavi dei vendor alla spesa end user ([comunicato 2018](https://www.gartner.com/en/newsroom/press-releases/2018-08-15-gartner-forecasts-worldwide-information-security-spending-to-exceed-124-billion-in-2019)).
- **Editori**: valori diversi a ogni edizione. Statista stessa avverte che i dati di edizioni diverse non sono confrontabili.

### 1.5 Rapporti dichiarati dagli utenti

| Rapporto | Valore | Popolazione | Fonte |
|---|---|---|---|
| Sicurezza su uscite di cassa IT | 4,9% | Banche italiane, 23 gruppi (2024) | [CIPA](https://www.cipa.it/rilevazioni/economiche/2024/Rilevazione_economica_2024.pdf) |
| Sicurezza su spesa IT, media | 5,1% (2022), 5,6% (2023) | Organizzazioni UE, dati Gartner | [ENISA NIS Investments 2024](https://www.enisa.europa.eu/sites/default/files/2024-11/CSPA%20-%20NIS%20Investments%20-%202024_0.pdf) |
| Sicurezza su spesa IT, mediana | 9% (2023) | Entità NIS, prevalentemente grandi | [ENISA NIS Investments 2024](https://www.enisa.europa.eu/sites/default/files/2024-11/CSPA%20-%20NIS%20Investments%20-%202024_0.pdf) |
| Sicurezza su spesa IT, PMI e grandi | 8,6% e 7% (edizione 2021) | Entità NIS | [ENISA NIS Investments 2021](https://www.enisa.europa.eu/sites/default/files/publications/ENISA%20Report%20-%20NIS%20Investments%202021.pdf) |
| Sicurezza su spesa IT, media | 11,9% (2024) | CISO, prevalentemente nordamericani | [IANS e Artico 2025](https://sf-cdn.iansresearch.com/sitefinity/docs/default-source/reports/2025-security-budget-benchmark-summary-report_08_05_2025.pdf?sfvrsn=43097214_2) |
| Sicurezza su budget IT, media | 18% (2025) | Imprese tedesche con 10+ addetti e almeno 1 Mln € di fatturato, quota stimata dal rispondente | [Bitkom Wirtschaftsschutz 2025](https://www.bitkom.org/sites/main/files/2025-12/bitkom-studienbericht-wirtschaftsschutz-2025.pdf) |
| Cyber su budget IT, classi | classi modali 3-5% e 6-10% (19% dei rispondenti ciascuna, 2023) | Imprese austriache | [KPMG con KSÖ 2023](https://www.ruv.at/wp-content/uploads/kpmg-studie-cybersecurity-in-oesterreich-2023_1x1.pdf) |

Le differenze dipendono dalla definizione di budget (budget del CISO o spesa totale), dalla statistica (mediana o media di rapporti) e dal campione (grandi entità o piccole imprese). La quota sul budget IT tende a essere più alta nelle PMI, mentre la spesa assoluta per impresa cresce molto con la dimensione.

---

## 2. Le metodologie di stima più diffuse

### 2.1 Quadro d'insieme

| Famiglia | Chi la usa | Lato | Cosa produce | Riproducibilità |
|---|---|---|---|---|
| A. Somma dei ricavi dei vendor con ripartizione | IDC, Gartner, Canalys/Omdia, PAC, e a valle Bitkom e Statista | Offerta | Mercato per paese e segmento | Bassa, note di dettaglio a pagamento |
| B. "Triangolazione" degli editori | Mordor, Grand View, MarketsandMarkets, IMARC, Fortune, Technavio, Ken Research, 6Wresearch | Per lo più offerta, dichiarazioni generiche | Mercato per paese e segmento | Bassa, nessun parametro pubblicato |
| C. Censimento dei fornitori | DSIT, ACN Francia, Agoria, Cyber Ireland, Dialogic, INCIBE; variante da contabilità nazionale WifOR | Offerta | Ricavi, valore aggiunto, addetti dell'industria nazionale | Media o alta |
| D. Survey agli utenti riportata all'universo | UK CSBS 2016-2019, Banca d'Italia Invind 2016, INE Spagna dal 2021, Statistics Canada | Domanda | Spesa totale delle imprese per settore e classe | Alta |
| E. Modello a rapporti | Gartner (spesa IT per settore), RTI per NIST 2013, struttura dichiarata da Mordor e IMARC | Domanda | Spesa per settore da fatturato × intensità | Media |
| F. Approcci misti | Osservatorio Polimi, Anitec-Assinform con NetConsulting cube, IDC Security Spending Guide | Misto | Mercato domestico | Bassa |

La famiglia A, con la variante B, è di gran lunga la più diffusa per il "mercato". Le famiglie D ed E misurano l'oggetto del modello SBS e sono le meno frequenti.

### 2.2 A. Somma dei ricavi dei vendor

- **IDC.** I tracker dei prodotti e dei servizi misurano i ricavi dei vendor ("Measurement for this tracker is revenue", [Security Products Tracker](https://my.idc.com/getdoc.jsp?containerId=IDC_P38710); [Services Tracker](https://my.idc.com/getdoc.jsp?containerId=IDC_P33285)). La Security Spending Guide alloca la spesa a paese, settore NACE Rev. 2 e classe dimensionale usando guidance dei vendor, analisti locali e survey agli utenti ([Spending Guide](https://my.idc.com/getdoc.jsp?containerId=IDC_P33461)). Le celle paese × settore × dimensione sono stime di modello; le classi pubblicate (1-9, 10-99, 100-499, 500-999, 1.000+) non coincidono con le classi SBS.
- **Gartner.** Stima i ricavi dei vendor da bilanci, richieste ai vendor, canale e survey e pubblica una "spesa end user" che include il consumer. Il passaggio da ricavi a spesa end user per la sicurezza non è documentato nelle pagine pubbliche.
- **Canalys/Omdia.** Stima trimestrale delle vendite di oltre 40 vendor in 52 paesi, ancorata ai vendor quotati, con ripartizione tra vendita diretta e canale ([Cybersecurity analysis](https://canalys.dev/site/analysis/cybersecurity+analysis)). Oltre il 90% della spesa passa dai partner, quindi il ricavo dei vendor sottostima la spesa degli utenti.
- **PAC.** Volumi per 30 paesi su software e servizi; conta solo ricavi non captive e, nei dati SITSI, esclude l'hardware di sicurezza ([segmentazione PAC](https://sitsi.pacanalyst.com/wp-content/uploads/2023/11/PAC_Segmentation.pdf)). È la fonte dei dati Bitkom dal 2025.
- **Statista Market Insights.** Ricavi dei vendor a prezzi del produttore senza IVA, B2C, B2B e B2G insieme, combinazione top-down e bottom-up con logica per segmento non pubblicata. Ogni paese è stimato con indicatori come PIL e penetrazione di internet; previsioni con modelli ETS o ARIMA ([pagina Germania](https://www.statista.com/outlook/tmo/cybersecurity/germany), [nota metodologica](https://www.statista.com/outlook/methodology/)).

### 2.3 B. La "triangolazione" degli editori

Nove editori su dieci dichiarano una triangolazione top-down e bottom-up con interviste di validazione. Il testo metodologico è identico tra report di settori lontanissimi per Fortune, Technavio, Grand View, IMARC, Ken Research e 6Wresearch. Nessuno pubblica parametri, pesi o formule. L'ancora numerica più frequente sono i ricavi dei fornitori.

Due eccezioni dichiarano un modello dal lato domanda, sempre senza parametri. Mordor, per l'Italia, parte dalla spesa IT nazionale, applica la quota sicurezza dei budget IT per tipo di acquirente e verifica la spesa per addetto ([Mordor Italia](https://www.mordorintelligence.com/industry-reports/italy-cybersecurity-market)). IMARC, per l'Europa, moltiplica la quota del budget di sicurezza sull'IT per la spesa IT delle imprese per paese e settore ([IMARC Europa](https://www.imarcgroup.com/europe-cybersecurity-market)). Grand View pubblica nei report cyber verticali una tabella a quattro strati lato domanda (organizzazioni indirizzabili, mercato servibile, utilizzatori attivi, monetizzazione).

Rischi tipici: incoerenze interne (MarketsandMarkets dà per l'Europa 2025 29,8 mld USD in una pagina e 54,8 mld USD in un'altra), circolarità (Fortune usa Statista come database, Research and Markets rivende report di altri editori), revisioni a ogni edizione.

### 2.4 C. Censimento dei fornitori

La catena è la stessa ovunque: elenco delle imprese da registri, siti web, cluster e strumenti automatici; collegamento a bilanci o microdati; attribuzione di una quota cyber alle imprese diversificate; imputazione delle lacune per addetto; calcolo del valore aggiunto.

- **DSIT.** Elenco costruito da tassonomia, cluster e dati web, arricchito con Companies House e FAME; 2.603 imprese nell'edizione 2026; distinzione tra imprese dedicate e diversificate ([DSIT 2026](https://www.gov.uk/government/publications/cyber-security-sectoral-analysis-2026/cyber-security-sectoral-analysis-2026)).
- **ACN Francia con DECISION.** Base di circa 680-765 imprese che coprono l'85% del fatturato della filiera; quota di attività stimata impresa per impresa ([Observatoire 2024](https://www.confiance-numerique.fr/wp-content/uploads/2024/06/2024-ACN-Observatory-of-digital-trust-bd.pdf)).
- **Cyber Ireland.** 632 imprese identificate anche con web crawling e LLM; per le imprese diversificate la quota cyber è stimata dalla quota di personale in ruoli cyber ([rapporto 2025](https://cyberireland.ie/wp-content/uploads/2025/06/PE-All-Island-Cyber-Security-Sector-Research-Report-FINAL.pdf)).
- **Dialogic per i Paesi Bassi.** Analisi testuale dei siti di tutte le imprese olandesi, collegamento ai microdati CBS, fattori di correzione da survey per classe di addetti (circa 50%, 40% e 25%) ([studio 2023](https://dialogic.nl/wp-content/uploads/2023/06/economische-kansen-van-de-cybersecuritysector-7.pdf)).
- **WifOR per la Germania (variante).** Coefficienti di sicurezza IT applicati alle classi WZ della contabilità nazionale; il mercato è produzione più importazioni meno export ([studio 2019](https://www.wifor.com/uploads/2019/08/it-sicherheitsmarkt-in-deutschland-studie-2019.pdf)). Il perimetro molto ampio porta a 26,8 mld € nel 2017.

Il passaggio più fragile è la quota cyber delle imprese diversificate, stimata da ciascuno in modo diverso. Questi studi misurano l'industria, non la domanda domestica.

### 2.5 D. Survey agli utenti riportata all'universo

| Fonte | Disegno | Perimetro | Risultato utile |
|---|---|---|---|
| [INE Spagna, ETICCE](https://www.ine.es/metodologia/t09/eticce1_24.pdf) | Statistica ufficiale annuale, stimatori di espansione, imputazione con la mediana dello strato | Imprese con 10+ addetti delle sezioni CNAE C-N; tabelle di spesa senza 56, 64-66 e 95.1; personale interno incluso | Spesa in sicurezza TIC 3.993 Mln € nel 2023 e 4.513 Mln € nel 2024 |
| [Banca d'Italia, Invind 2016](https://www.bancaditalia.it/pubblicazioni/qef/2017-0407/QEF_407.pdf) | Survey stratificata, imputazione con modello sulla spesa per addetto, winsorizzazione per classe | Imprese con 20+ addetti dell'industria e dei servizi non finanziari; PA esclusa; personale interno incluso | Totale 570-780 Mln €; spesa per addetto mediana 90,9 €, media 142,7 € |
| [UK CSBS 2016-2019](https://assets.publishing.service.gov.uk/media/5ff5c7278fa8f53b790e7363/Cyber_Security_Breaches_Survey_2019_-_Technical_Annex_V2.pdf) | Campione casuale dal registro, ponderazione per dimensione e settore | Imprese private, micro incluse; personale interno incluso | Medie e mediane per classe; media molto superiore alla mediana; domanda abbandonata nel 2020 |
| [Statistics Canada, CSCSC](https://www23.statcan.gc.ca/imdb/p2SV.pl?Function=getSurvey&Id=1580450) | Registro d'imprese, strati per settore e classe, pesi | Imprese con 10+ addetti; PA esclusa fino al 2023, unità federali incluse dal 2025 | Totali per dimensione e voce di spesa; è il disegno che un modello SBS imita |

Eurostat, Destatis, Statistik Austria e CBS rilevano l'adozione di misure di sicurezza, non la spesa ([Eurostat, ICT security in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=ICT_security_in_enterprises)).

### 2.6 E. Modello a rapporti

- **Gartner, spesa IT per settore.** Ricavi del settore × quota dei ricavi destinata all'IT, ripartita tra hardware, software, servizi e servizi interni (personale IT). Non è applicato alla sicurezza.
- **RTI per NIST (2013).** Valore per dollaro di ricavo × ricavi d'industria del Census × intensità IT relativa del settore, sommato sulle industrie ([rapporto NIST 13-1](https://www.nist.gov/system/files/documents/2017/05/09/report13-1.pdf)). Lo studio stima il valore di un miglioramento dell'infrastruttura di sicurezza, non la spesa, ma la catena di estrapolazione è la stessa. Gli autori avvertono che l'intensità IT riflette uso dell'IT e dimensione, non il rischio.
- **Forrester.** Dichiara che il dimensionamento del mercato tech USA parte dagli investimenti delle imprese nei conti nazionali e conta lo staff IT; non riguarda la sicurezza.
- **Mordor e IMARC**, come visto sopra, dichiarano questa struttura senza pubblicare i parametri.

È la logica del modello SBS. Nessuna fonte la applica in modo trasparente alla spesa cyber europea per settore e classe.

### 2.7 F. Approcci misti

- **Osservatorio Polimi.** "Triplice prospettiva": interviste a oltre 100 vendor (top-down), survey a grandi organizzazioni (145 nel 2025) e PMI (1.582 nel 2025) sulla spesa e sul budget cyber (bottom-up), confronto con studi esterni ([scenario 2025](https://www.osservatori.net/report/cybersecurity-data-protection/scenario-cybersecurity-2025/)). Non è pubblicato come si combinano le componenti. Le grandi imprese pesano oltre tre quarti della spesa ([comunicato 2023](https://www.osservatori.net/comunicato/cybersecurity-data-protection/cybersecurity-italia-mercato-crescita-2023/)).
- **Anitec-Assinform con NetConsulting cube.** Panel di almeno 400 fornitori e circa 5.000 interviste ad aziende utenti. Misura la spesa dell'utente finale al netto di IVA, personale interno e interscambio ([Il Digitale in Italia 2024](https://www.anitec-assinform.it/kdocs/2146137/il_digitale_in_italia_2024.pdf)). La nota metodologica è unica per tutto il mercato digitale.

### 2.8 Quadri metodologici europei

- **ENISA ECSMAF** indica come base della dimensione del mercato i ricavi della mappa dei fornitori e raccomanda triangolazione e indicatori proxy, senza un algoritmo di dimensionamento ([ECSMAF V3.0](https://www.enisa.europa.eu/sites/default/files/2026-03/ENISA%20Cybersecurity%20Market%20Analysis%20Framework%20(ECSMAF)%20%E2%80%93%20V3.0.pdf)).
- **Commissione, DG HOME**: combinazione di metodi, due estrapolazioni come limiti inferiore e superiore, punto medio ([studio sulle statistiche della sicurezza](https://home-affairs.ec.europa.eu/system/files/2020-09/security_statistics_-_final_report_en.pdf)).
- **OCSE**: le indagini ICT non forniscono indicatori economici sulla sicurezza come gli investimenti; checklist per indicatori tracciabili ([Measuring digital security risk management practices, 2019](https://www.oecd.org/content/dam/oecd/en/publications/reports/2019/06/measuring-digital-security-risk-management-practices-in-businesses_d66dd6a6/7b93c1f1-en.pdf); [New perspectives on measuring cybersecurity, 2024](https://www.oecd.org/content/dam/oecd/en/publications/reports/2024/06/new-perspectives-on-measuring-cybersecurity_6069c1b9/b1e31997-en.pdf)).
- La cybersecurity non ha un codice nelle classificazioni NACE e CPA: per questo il lato offerta richiede sempre di identificare le imprese una per una.

---

## 3. Implicazioni per il modello SBS (Italia, Germania, Austria)

### 3.1 Struttura

```
Spesa_cyber[n,s] = Fatturato_SBS[n,s] × (Spesa_IT / Fatturato)[n,s] × (Spesa_cyber / Spesa_IT)[n,s]
```

con n = settore NACE e s = classe dimensionale. In alternativa, o come controllo, Fatturato_SBS × (Spesa_cyber / Fatturato) diretto. Per le microimprese conviene un valore per impresa o per addetto, perché la quota sul fatturato è instabile. Va inclusa per ogni classe una quota di imprese con spesa nulla.

### 3.2 Parametri e calibrazione

| Parametro | Fonte | Uso consigliato | Cautela |
|---|---|---|---|
| Spesa cyber su fatturato per settore e classe | INE Spagna (4,0 mld € nel 2023, 4,5 nel 2024) diviso per il fatturato SBS spagnolo delle stesse celle | Prior per IT, DE e AT, da correggere | Il rapporto va calcolato: INE non lo pubblica. Stesso perimetro: 10+ addetti, senza CNAE 56, 64-66 e 95.1 |
| Spesa per addetto e totale Italia | Banca d'Italia Invind 2016 | Punto storico per l'Italia, imprese 20+ | Da indicizzare; limite inferiore dichiarato dagli autori |
| Spesa delle micro e quota a spesa zero | UK CSBS 2016-2019 | Ordine di grandezza per le classi 0-9 e 10-49 | Fuori UE, varianza molto alta |
| Quota cyber su IT, grandi imprese NIS | ENISA NIS Investments (mediana 9% nel 2023) | Solo per le celle 250+ dei settori NIS2 | Campione non proporzionale e non ponderato |
| Quota cyber su IT, imprese tedesche | Bitkom Wirtschaftsschutz (18% nel 2025) | Scenario alto per la Germania | Media di quote stimate dal rispondente, dominata dalle piccole imprese |
| Quota cyber su IT, banche italiane | CIPA (4,9% delle uscite di cassa IT, 365,7 Mln € per 23 gruppi nel 2024) | Solo se il modello copre la finanza | Solo banche |
| Propensione alla sicurezza per settore e classe | Eurostat, modulo ICT security; Statistik Austria, IKT-Sicherheit | Indice relativo per modulare i rapporti tra settori e classi | Non contiene spesa |
| Quota del personale interno | Tra 25% (CIPA, banche) e 39% (IANS 2025) | Passaggio da spesa totale a spesa esterna | Varia per dimensione e settore |

### 3.3 Perimetro da dichiarare

- **Due output.** Spesa totale con personale interno, confrontabile con ENISA, INE, Banca d'Italia e CSBS. Spesa esterna in hardware, software e servizi, circa il 60-75% del totale, confrontabile con Anitec-Assinform, Polimi, Bitkom e analisti.
- **Settori fuori SBS.** La finanza (K) e la PA (O) restano di norma fuori dal perimetro SBS. In Italia banche (433,7 Mln €) e PA (341,9 Mln €) valgono da sole circa il 39% della spesa Anitec-Assinform 2024, a cui si aggiungono assicurazioni e finanziarie ([Il Digitale in Italia 2025](https://lentepubblica.it/wp-content/uploads/2025/07/ANITEC-ASSINFORM_il_digitale_in_italia_2025_v5-compresso.pdf)). Va tolta questa parte prima di ogni confronto.
- **Voci da decidere esplicitamente.** Formazione (inclusa da Anitec negli "Altri servizi" e da Polimi), polizze cyber (nel framework Polimi, 2,5% del mercato nel 2017), hardware di rete (escluso da PAC SITSI), consumer.

### 3.4 Controlli incrociati per paese

- **Italia.** Il totale del modello, dopo aver aggiunto finanza e PA da fonti dedicate, dovrebbe cadere nella forbice tra Anitec-Assinform (valore basso, spesa esterna) e Polimi (valore alto): 2.001 e 2.480 Mln € nel 2024; 2.245 e 2.780 Mln € nel 2025.
- **Germania.** Usare solo la serie Bitkom con dati PAC di ottobre 2025 (2025: 11,1 mld €; software 4,8, servizi 5,6, hardware 0,8). Va trattata come mercato totale con clienti non dichiarati, quindi con PA e forse consumer.
- **Austria.** Nessuna fonte nazionale pubblica un totale. Si possono trasferire i rapporti di Germania e Italia, corretti con l'indagine IKT-Sicherheit di Statistik Austria, dichiarando che si tratta di trasferimenti.
- **Spagna come banco di prova.** Applicato alla Spagna, il modello deve riprodurre il totale INE con lo stesso perimetro. Una differenza ampia indica prima un problema di perimetro (soglie, finanza, personale) che di livello.

### 3.5 Incertezza

Presentare il risultato come forbice tra uno scenario basso e uno alto, come fanno lo studio DG HOME (due metodi e punto medio) e RAND (set di parametri alternativi). Documentare parametri, fonti e passaggi per ogni cella: è proprio ciò che manca agli editori.

### 3.6 Da evitare

- Usare i valori degli editori come obiettivo di calibrazione: non sono riproducibili e cambiano a ogni edizione.
- Usare le quote paese degli editori per ripartire un totale europeo.
- Moltiplicare mediane ENISA per il numero di imprese, o sommare mediane.
- Applicare medie di rapporti per impresa (Bitkom, IANS) al fatturato aggregato senza ponderazione.
- Confrontare la spesa con personale interno con i mercati dei fornitori.
- Usare i ricavi dell'industria nazionale come spesa domestica senza togliere l'export e aggiungere le importazioni.
- Mescolare vintage diversi della stessa serie (Bitkom IDC e Bitkom PAC; Gartner prima e dopo il 2018).

---

## 4. Limiti di questa analisi

- **Accesso alle fonti.** L'ambiente di esecuzione bloccava l'apertura diretta delle pagine. Valori e citazioni sono stati letti negli estratti testuali delle pagine indicate, restituiti da un motore di ricerca. Valori letti da grafici vanno ricontrollati sul documento.
- **Verifica.** Nel database sono state riaperte le fonti di 565 righe (545 confermate, 8 corrette, 10 non ritrovate, 2 rimosse). Per le metodologie, 75 affermazioni chiave sono state ricontrollate da verificatori indipendenti: 63 confermate, 8 contraddette e 4 non supportate. Le correzioni sono incluse in questo documento.
- **Note a pagamento.** Le note metodologiche di dettaglio di IDC, Gartner, Forrester e PAC sono a pagamento. Qui sono descritte solo le parti pubbliche.
- **Deduzioni.** Dove una caratteristica non è dichiarata dalla fonte, il database la marca come "Dedotta" con motivazione.

## Fonti principali citate

**Database e dati**
- `fonti_mercato_cyber_UE_UK_2026-10-08.xlsx`, fogli Dati, Fonti_Metodologie, Copertura_Paesi, Ricerche_senza_esito, Cambi.

**Analisti e editori**
- IDC: [Security Products Tracker](https://my.idc.com/getdoc.jsp?containerId=IDC_P38710), [Services Tracker](https://my.idc.com/getdoc.jsp?containerId=IDC_P33285), [Security Spending Guide](https://my.idc.com/getdoc.jsp?containerId=IDC_P33461)
- Gartner: [forecast sicurezza 2018](https://www.gartner.com/en/newsroom/press-releases/2018-08-15-gartner-forecasts-worldwide-information-security-spending-to-exceed-124-billion-in-2019)
- Canalys: [Cybersecurity analysis](https://canalys.dev/site/analysis/cybersecurity+analysis)
- PAC: [segmentazione SITSI](https://sitsi.pacanalyst.com/wp-content/uploads/2023/11/PAC_Segmentation.pdf)
- Statista: [Cybersecurity Germania](https://www.statista.com/outlook/tmo/cybersecurity/germany), [metodologia Market Insights](https://www.statista.com/outlook/methodology/)
- Mordor: [Italia](https://www.mordorintelligence.com/industry-reports/italy-cybersecurity-market), [Austria](https://www.mordorintelligence.com/de/industry-reports/austria-cybersecurity-market)
- IMARC: [Europa](https://www.imarcgroup.com/europe-cybersecurity-market)
- MarketsandMarkets: [Italia](https://www.marketsandmarkets.com/Market-Reports/geography/cyber-security-market/italy)
- Grand View Research: [Germania](https://www.grandviewresearch.com/horizon/outlook/cyber-security-market/germany), [metodologia](https://www.grandviewresearch.com/info/research-methodology)

**Fonti nazionali e di settore**
- Osservatorio Polimi: [comunicato 2026](https://www.osservatori.net/comunicato/cybersecurity-data-protection/cybersecurity-italia-mercato-crescita/), [scenario 2025](https://www.osservatori.net/report/cybersecurity-data-protection/scenario-cybersecurity-2025/)
- Anitec-Assinform: [Il Digitale in Italia 2024](https://www.anitec-assinform.it/kdocs/2146137/il_digitale_in_italia_2024.pdf), [2025](https://lentepubblica.it/wp-content/uploads/2025/07/ANITEC-ASSINFORM_il_digitale_in_italia_2025_v5-compresso.pdf), [2026](https://www.matricedigitale.it/wp-content/uploads/2026/07/Rapporto-Anitec-Assinform_Il-Digitale-in-Italia-2026.pdf)
- Bitkom: [mercato 2024](https://www.bitkom.org/Presse/Presseinformation/Erstmals-mehr-als-10-Milliarden-Euro-fuer-Deutschlands-Cybersicherheit), [mercato 2025](https://www.bitkom.org/sites/main/files/2025-10/bitkom-charts-cybercrime-und-der-markt-fuer-it-sicherheit-2025.pdf), [Wirtschaftsschutz 2025](https://www.bitkom.org/sites/main/files/2025-12/bitkom-studienbericht-wirtschaftsschutz-2025.pdf)
- KPMG con KSÖ: [Cybersecurity in Österreich 2023](https://www.ruv.at/wp-content/uploads/kpmg-studie-cybersecurity-in-oesterreich-2023_1x1.pdf)
- CIPA: [rilevazione economica 2024](https://www.cipa.it/rilevazioni/economiche/2024/Rilevazione_economica_2024.pdf)
- DSIT: [Cyber security sectoral analysis 2026](https://www.gov.uk/government/publications/cyber-security-sectoral-analysis-2026/cyber-security-sectoral-analysis-2026)
- ACN Francia: [Observatoire 2024](https://www.confiance-numerique.fr/wp-content/uploads/2024/06/2024-ACN-Observatory-of-digital-trust-bd.pdf)
- Cyber Ireland: [All-Island report 2025](https://cyberireland.ie/wp-content/uploads/2025/06/PE-All-Island-Cyber-Security-Sector-Research-Report-FINAL.pdf)
- Dialogic: [settore cyber olandese 2023](https://dialogic.nl/wp-content/uploads/2023/06/economische-kansen-van-de-cybersecuritysector-7.pdf)
- WifOR: [IT-Sicherheitsmarkt 2019](https://www.wifor.com/uploads/2019/08/it-sicherheitsmarkt-in-deutschland-studie-2019.pdf)

**Survey lato domanda e statistiche ufficiali**
- ENISA NIS Investments: [2021](https://www.enisa.europa.eu/sites/default/files/publications/ENISA%20Report%20-%20NIS%20Investments%202021.pdf), [2024](https://www.enisa.europa.eu/sites/default/files/2024-11/CSPA%20-%20NIS%20Investments%20-%202024_0.pdf), [2025](https://www.enisa.europa.eu/sites/default/files/2025-12/NIS%20Investments%202025%20-%20Main%20report_0.pdf)
- INE: [questionario ETICCE 2024](https://www.ine.es/metodologia/t09/eticce1_24.pdf), [metodologia](https://www.ine.es/daco/daco42/comele/meto_eticce.pdf)
- Banca d'Italia: [QEF 407, Invind 2016](https://www.bancaditalia.it/pubblicazioni/qef/2017-0407/QEF_407.pdf)
- UK CSBS: [allegato tecnico 2019](https://assets.publishing.service.gov.uk/media/5ff5c7278fa8f53b790e7363/Cyber_Security_Breaches_Survey_2019_-_Technical_Annex_V2.pdf)
- Statistics Canada: [CSCSC](https://www23.statcan.gc.ca/imdb/p2SV.pl?Function=getSurvey&Id=1580450)
- Eurostat: [ICT security in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=ICT_security_in_enterprises)
- IANS e Artico: [Security Budget Benchmark 2025](https://sf-cdn.iansresearch.com/sitefinity/docs/default-source/reports/2025-security-budget-benchmark-summary-report_08_05_2025.pdf?sfvrsn=43097214_2)

**Quadri metodologici e letteratura**
- ENISA: [ECSMAF V3.0](https://www.enisa.europa.eu/sites/default/files/2026-03/ENISA%20Cybersecurity%20Market%20Analysis%20Framework%20(ECSMAF)%20%E2%80%93%20V3.0.pdf)
- Commissione europea, DG HOME: [statistiche sull'industria della sicurezza](https://home-affairs.ec.europa.eu/system/files/2020-09/security_statistics_-_final_report_en.pdf)
- OCSE: [New perspectives on measuring cybersecurity, 2024](https://www.oecd.org/content/dam/oecd/en/publications/reports/2024/06/new-perspectives-on-measuring-cybersecurity_6069c1b9/b1e31997-en.pdf)
- RTI per NIST: [Planning Report 13-1](https://www.nist.gov/system/files/documents/2017/05/09/report13-1.pdf)
- RAND: [Estimating the Global Cost of Cyber Risk](https://www.rand.org/content/dam/rand/pubs/research_reports/RR2200/RR2299/RAND_RR2299.pdf)
