#!/usr/bin/env python3
"""
Genera il file QSF (Qualtrics Survey Format) della
"Survey di Ricerca 2026/2027 – Questionario End User – Grandi e grandissime imprese"
dell'Osservatorio Intelligent Business Process Automation (Politecnico di Milano).

Contenuti: Survey_IBPA_2026-2027_EndUser_Grandi_FINALE_v4.docx
Stile e impostazioni: Survey_IBPA_2025.qsf (edizione precedente)

Uso:  python3 build_qsf.py [percorso_output.qsf]

Scelte strutturali (come nel 2025):
  - survey flow con soli due blocchi consecutivi ("Introduzione" e "Questionario"), senza branch,
    embedded data o altri elementi tra i blocchi: in Qualtrics qualunque elemento del flow tra due
    blocchi disattiva il pulsante Indietro sulla pagina successiva;
  - tutti i filtri del documento sono display logic sulle domande / sulle opzioni;
  - gli screen-out sono skip logic verso la pagina finale "Esclusione".
"""
import html
import json
import random
import re
import sys
from collections import OrderedDict

OUT = sys.argv[1] if len(sys.argv) > 1 else "Survey_IBPA_2026-2027_EndUser_Grandi.qsf"

_rng = random.Random(20262027)
_ALNUM = "abcdefghijklmnopqrstuvwxyz" "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def rid(prefix, n=15):
    return prefix + "".join(_rng.choice(_ALNUM) for _ in range(n))


SURVEY_ID = rid("SV_")
RS_ID = rid("RS_")
NOW = "2026-11-05 12:00:00"
SURVEY_NAME = "Survey IBPA 2026 - End User Grandi imprese"
# Libreria dell'account che possiede la survey 2025 (messaggio di fine survey riutilizzato)
LIB_2025 = "UR_cSGyJAp59NL7cF0"
EOS_MSG_2025 = "MS_1YBpMl6kYzH5CZg"

# --------------------------------------------------------------------------
# Stile testi (come nel QSF 2025)
# --------------------------------------------------------------------------
BR = "<br />\n"


def plain(s):
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<sup>.*?</sup>", "", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def short(s, n=95):
    p = plain(s)
    return p if len(p) <= n else p[:n].rstrip() + "..."


def HDR(title, intro=None):
    """Intestazione di sezione: titolo 29px in grassetto + eventuale testo introduttivo corsivo 16px."""
    s = '<span style="font-size:29px;"><strong>%s</strong></span>' % title
    if intro:
        s += BR + BR + '<em><span style="font-size:16px;">%s</span></em>' % intro
    return s


def Q(stem=None, instr=None, note=None, sub=None):
    """Domanda: testo semplice + istruzione corsiva 16px + nota corsiva 16px + sottotitolo in grassetto."""
    s = stem or ""
    if instr:
        s += (BR if s else "") + '<em><span style="font-size:16px;">%s</span></em>' % instr
    if note:
        s += (BR + BR if s else "") + '<span style="font-size:16px;"><em>%s</em></span>' % note
    if sub:
        s += (BR + BR if s else "") + "<strong>%s</strong>" % sub
    return s


def B(label, rest=""):
    """Opzione con etichetta in grassetto (stile 2025)."""
    return "<strong>%s</strong>%s" % (label, rest)


# --------------------------------------------------------------------------
# Registro domande
# --------------------------------------------------------------------------
QUESTIONS = OrderedDict()
_qcount = [0]
LET = "abcdefghijklmnopqrstuvwxyz"


def _new_qid():
    _qcount[0] += 1
    return "QID%d" % _qcount[0]


def _base(tag, qid, text, qtype, selector, subselector=None):
    p = OrderedDict()
    p["QuestionText"] = text
    p["DefaultChoices"] = False
    p["DataExportTag"] = tag
    p["QuestionType"] = qtype
    p["Selector"] = selector
    if subselector is not None:
        p["SubSelector"] = subselector
    p["DataVisibility"] = {"Private": False, "Hidden": False}
    p["Configuration"] = OrderedDict([("QuestionDescriptionOption", "UseText")])
    p["QuestionDescription"] = short(text)
    return p


def _val(force, vtype="None", **extra):
    s = OrderedDict([("ForceResponse", "ON" if force else "OFF"), ("ForceResponseType", "ON"),
                     ("Type", vtype)])
    s.update(extra)
    return {"Settings": s}


def _reg(tag, qid, p, kind, **meta):
    assert tag not in QUESTIONS, tag
    p["GradingData"] = []
    p["Language"] = []
    p["QuestionID"] = qid
    QUESTIONS[tag] = dict(qid=qid, payload=p, kind=kind, text=p["QuestionText"], **meta)
    return QUESTIONS[tag]


def mc(tag, text, specs, multi=False, force=True, rand=None, maxc=None, dropdown=False):
    """Scelta multipla. specs: stringhe o dict {t, te, excl, id, key}."""
    qid = _new_qid()
    choices, order, keymap, labels = OrderedDict(), [], {}, {}
    for i, s in enumerate(specs):
        if isinstance(s, str):
            s = {"t": s}
        cid = str(s.get("id", i + 1))
        c = OrderedDict([("Display", s["t"])])
        if s.get("te"):
            c["TextEntry"] = "true"
            c["TextEntrySize"] = "Medium"
        if s.get("excl"):
            c["ExclusiveAnswer"] = True
        choices[cid] = c
        order.append(cid)
        keymap[s.get("key", LET[i])] = cid
        labels[cid] = plain(s["t"])
    if dropdown:
        p = _base(tag, qid, text, "MC", "DL")
    else:
        p = _base(tag, qid, text, "MC", "MAVR" if multi else "SAVR", "TX")
    p["Choices"] = choices
    p["ChoiceOrder"] = order
    if rand:
        p["Randomization"] = rand(order)
    if maxc:
        p["Validation"] = _val(force, "ChoiceRange", MinChoices="1", MaxChoices=str(maxc))
    else:
        p["Validation"] = _val(force)
    p["NextChoiceId"] = max(int(c) for c in order) + 1
    p["NextAnswerId"] = 1
    return _reg(tag, qid, p, "MC", multi=multi, ck=keymap, clabels=labels, force=force)


def matrix(tag, text, rows, cols, multi=False, force=True, excl_cols=(), rand_rows=False):
    qid = _new_qid()
    choices = OrderedDict((str(i + 1), OrderedDict([("Display", r)])) for i, r in enumerate(rows))
    answers = OrderedDict()
    for j, a in enumerate(cols):
        d = OrderedDict([("Display", a)])
        if (j + 1) in excl_cols:
            d["ExclusiveAnswer"] = True
        answers[str(j + 1)] = d
    p = _base(tag, qid, text, "Matrix", "Likert", "MultipleAnswer" if multi else "SingleAnswer")
    p["Configuration"].update(OrderedDict([("TextPosition", "inline"), ("ChoiceColumnWidth", 25),
                                           ("RepeatHeaders", "none"), ("WhiteSpace", "OFF"),
                                           ("MobileFirst", True)]))
    p["Choices"] = choices
    p["ChoiceOrder"] = list(choices.keys())
    if rand_rows:
        p["Randomization"] = OrderedDict([("Advanced", None), ("TotalRandSubset", ""), ("Type", "All")])
    p["Validation"] = _val(force)
    p["NextChoiceId"] = len(rows) + 1
    p["NextAnswerId"] = len(cols) + 1
    p["Answers"] = answers
    p["AnswerOrder"] = list(answers.keys())
    p["ChoiceDataExportTags"] = False
    return _reg(tag, qid, p, "Matrix", multi=multi, force=force,
                rlabels={str(i + 1): plain(r) for i, r in enumerate(rows)},
                alabels={str(j + 1): plain(a) for j, a in enumerate(cols)})


def form(tag, text, fields):
    """Text entry a più campi (come l'anagrafica 2025). fields: (etichetta, validazione|None)."""
    qid = _new_qid()
    p = _base(tag, qid, text, "TE", "FORM")
    ch = OrderedDict()
    for i, (lab, valid) in enumerate(fields):
        c = OrderedDict([("Display", lab)])
        if valid:
            c["TextEntry"] = "on"
            c["TextEntryValidation"] = valid
        ch[str(i + 1)] = c
    p["Choices"] = ch
    p["ChoiceOrder"] = list(ch.keys())
    p["Validation"] = _val(True)
    p["NextChoiceId"] = len(fields) + 1
    p["NextAnswerId"] = 1
    p["SearchSource"] = {"AllowFreeResponse": "false"}
    return _reg(tag, qid, p, "FORM")


def db(tag, text):
    qid = _new_qid()
    p = _base(tag, qid, text, "DB", "TB")
    p["ChoiceOrder"] = []
    p["Validation"] = {"Settings": {"Type": "None"}}
    p["NextChoiceId"] = 4
    p["NextAnswerId"] = 1
    return _reg(tag, qid, p, "DB")


def cs(tag, text, items, total=100):
    """Somma costante con vincolo 'Must total'."""
    qid = _new_qid()
    ch = OrderedDict((str(i + 1), OrderedDict([("Display", t)])) for i, t in enumerate(items))
    p = _base(tag, qid, text, "CS", "VRTL")
    p["Choices"] = ch
    p["ChoiceOrder"] = list(ch.keys())
    p["Validation"] = _val(True, "ChoicesTotal", ChoiceTotal=str(total), EnforceRange=None)
    p["NextChoiceId"] = len(items) + 1
    p["NextAnswerId"] = 1
    return _reg(tag, qid, p, "CS", clabels={str(i + 1): plain(t) for i, t in enumerate(items)})


def sbs_spesa(tag, text, rows, options):
    """Side-by-side 'Non so' + 'Variazione' (menu a tendina): stessa struttura della Q8.4 del 2025."""
    qid = _new_qid()
    p = _base(tag, qid, text, "SBS", "SBSMatrix")
    p["Configuration"]["RepeatHeaders"] = "none"
    rch = OrderedDict((str(i + 1), {"Display": r}) for i, r in enumerate(rows))
    p["Choices"] = rch
    p["ChoiceOrder"] = list(rch.keys())
    p["Validation"] = _val(False)
    p["NextChoiceId"] = len(rows) + 1
    p["NextAnswerId"] = 3
    p["NumberOfQuestions"] = 2
    col1 = OrderedDict([
        ("Answers", {"1": {"Display": "Se si seleziona questa opzione non selezionare alcuna risposta per la colonna \"Variazione\""}}),
        ("QuestionText", "<strong>Non so</strong>"), ("RecodeValues", []), ("VariableNaming", []),
        ("AnalyzeChoices", []), ("QuestionType", "Matrix"), ("Selector", "Likert"), ("SubSelector", "SingleAnswer"),
        ("ChoiceColumnWidthPixels", None),
        ("Configuration", {"ChoiceColumnWidthPixels": 159, "QuestionDescriptionOption": "UseText"}),
        ("DataExportTag", tag + "#1"), ("QuestionID", qid + "#1"), ("Choices", rch),
        ("ChoiceDataExportTags", False), ("QuestionDescription", "Non so")])
    col2 = OrderedDict([
        ("Answers", OrderedDict((str(i + 1), {"Display": o}) for i, o in enumerate(options))),
        ("QuestionText", "<strong>Variazione</strong>"), ("RecodeValues", []), ("VariableNaming", []),
        ("AnalyzeChoices", {"1": "on"}), ("QuestionType", "Matrix"), ("Selector", "Likert"), ("SubSelector", "DL"),
        ("ChoiceColumnWidthPixels", None),
        ("Configuration", {"ChoiceColumnWidthPixels": 265, "QuestionDescriptionOption": "UseText"}),
        ("DataExportTag", tag + "#2"), ("QuestionID", qid + "#2"), ("Choices", rch),
        ("ChoiceDataExportTags", False), ("QuestionDescription", "Variazione")])
    p["AdditionalQuestions"] = OrderedDict([("1", col1), ("2", col2)])
    p["ChoiceDataExportTags"] = False
    return _reg(tag, qid, p, "SBS")


# --------------------------------------------------------------------------
# Condizioni logiche (descrizioni in italiano come nell'account Qualtrics 2025)
# --------------------------------------------------------------------------
OPDESC = {"Selected": "è selezionato", "NotSelected": "non è selezionato"}
CONJDESC = {"If": "Se", "Or": "O", "And": "E"}


def c_sel(tag, key, op="Selected"):
    q = QUESTIONS[tag]
    cid = q["ck"][key]
    loc = "q://%s/SelectableChoice/%s" % (q["qid"], cid)
    return dict(_q=short(q["text"]), _c=q["clabels"][cid], LogicType="Question", QuestionID=q["qid"],
                QuestionIsInLoop="no", ChoiceLocator=loc, Operator=op,
                QuestionIDFromLocator=q["qid"], LeftOperand=loc, Type="Expression")


def c_cell(tag, row, col, op="Selected"):
    q = QUESTIONS[tag]
    r, a = str(row), str(col)
    assert r in q["rlabels"] and a in q["alabels"], (tag, row, col)
    loc = "q://%s/SelectableChoice/%s/%s" % (q["qid"], r, a)
    return dict(_q=short(q["text"]), _c="%s - %s" % (short(q["rlabels"][r], 55), q["alabels"][a]),
                LogicType="Question", QuestionID=q["qid"], QuestionIsInLoop="no", ChoiceLocator=loc,
                Operator=op, QuestionIDFromLocator=q["qid"], LeftOperand=loc, Type="Expression")


def L(*groups, inpage=False):
    """Logica a insiemi: ogni gruppo = (connettivo interno 'Or'|'And', [condizioni]);
    i gruppi sono uniti in AND (primo gruppo 'If', successivi 'AndIf')."""
    out = OrderedDict()
    for gi, (conj, conds) in enumerate(groups):
        assert conj in ("Or", "And") and conds
        g = OrderedDict()
        for i, c0 in enumerate(conds):
            c = OrderedDict((k, v) for k, v in c0.items() if not k.startswith("_"))
            word = CONJDESC["If"] if i == 0 else CONJDESC[conj]
            c["Description"] = ('<span class="ConjDesc">%s</span> <span class="QuestionDesc">%s</span> '
                                '<span class="LeftOpDesc">%s</span> <span class="OpDesc">%s</span> '
                                % (word, c0["_q"], c0["_c"], OPDESC[c0["Operator"]]))
            if i > 0:
                c["Conjuction"] = conj          # sic: grafia usata da Qualtrics
            g[str(i)] = c
        g["Type"] = "If" if gi == 0 else "AndIf"
        out[str(gi)] = g
    out["Type"] = "BooleanExpression"
    out["inPage"] = inpage
    return out


def set_dl(tag, logic):
    QUESTIONS[tag]["payload"]["DisplayLogic"] = logic


def adv_rand_fixed_last(order, n_fixed_last=1):
    rnd, fixed = order[:-n_fixed_last], order[-n_fixed_last:]
    return OrderedDict([
        ("Type", "Advanced"),
        ("Advanced", OrderedDict([("FixedOrder", ["{~SubSet~}"] * len(rnd) + fixed), ("RandomizeAll", []),
                                  ("RandomSubSet", rnd), ("ScaleReversal", []), ("Undisplayed", []),
                                  ("TotalRandSubset", len(rnd))])),
        ("ConsistentScaleReversal", False), ("EvenPresentation", False), ("TotalRandSubset", "")])


# ==========================================================================
# CONTENUTI
# ==========================================================================
ALTRO = {"t": "Altro (specificare):", "te": True}

# ---------------- Introduzione (testo 2025 aggiornato) ----------------
db("A",
   '<h1 style="text-align: center;"><span style="font-size:29px;"><span style="font-family:Arial,Helvetica,sans-serif;">'
   '<span style="color:#002d56;"><strong>Survey di Ricerca dell\'Osservatorio Intelligent Business Process Automation '
   'del Politecnico di Milano 2026/2027</strong></span></span></span></h1>\n<br>\n'
   '<span style="font-size:16px;">Attraverso la seguente rilevazione l’<a href="https://www.osservatori.net/intelligent-business-process-automation/">'
   'Osservatorio Intelligent Business Process Automation</a> intende approfondire il grado di maturità delle organizzazioni '
   'italiane in merito al tema della Process Automation.<br>\n<br>\n'
   '<em>Ricordiamo fin da subito che tutti i dati forniti rimarranno all’interno del gruppo di Ricerca e non verranno '
   'divulgati se non in forma aggregata o di elaborazioni statistiche, quindi non sarà possibile in alcun modo risalire '
   'ad un’azienda rispondente.</em><br>\n<br>\n'
   '<strong><i><u>Guida alla compilazione del questionario.</u></i></strong><br>\n'
   '<b>La compilazione richiede mediamente dai 20 ai 25 minuti</b>. Se desidera interrompere momentaneamente la '
   'compilazione, al termine di ogni pagina le risposte saranno salvate in automatico. Le risposte saranno conservate e '
   'si potrà ritornare alla compilazione del questionario attraverso il link unico iniziale. Eventuali informazioni o '
   'chiarimenti in merito alla compilazione possono essere richiesti ad Andrea Scimonelli '
   '(<a href="mailto:andrea.scimonelli@polimi.it">andrea.scimonelli@polimi.it</a>).</span><br>\n&nbsp;\n'
   '<p><span style="font-size:16px;"><span style="font-family:Arial,Helvetica,sans-serif;"><b>Perché partecipare?</b></span></span></p>\n\n'
   '<p><span style="font-size:16px;"><span style="font-family:Arial,Helvetica,sans-serif;">• I rispondenti riceveranno '
   'un&nbsp;<b>report approfondito</b>&nbsp;con i risultati della ricerca, che include un’analisi dettagliata dello stato '
   'di adozione della Process Automation in Italia.</span></span></p>\n\n'
   '<p><span style="font-size:16px;"><span style="font-family:Arial,Helvetica,sans-serif;">• I risultati della ricerca '
   'saranno esposti durante il&nbsp;<b>Convegno Finale dell’Osservatorio IBPA</b>, un evento esclusivo per discutere dei '
   'principali trend e delle opportunità nell’ambito della Process Automation.</span></span><br>\n&nbsp;</p>\n'
   '<span style="font-size:16px;">Cliccando su "<em>Pagina successiva</em>" si esprime il consenso al trattamento dei suoi '
   'dati da parte degli Osservatori Digital Innovation e si dichiara di aver preso visione dell’informativa privacy '
   '(<a href="https://www.osservatori.net/it/assistenza/privacy-policy">link</a>).<br>\n<br>\n'
   'Il presente questionario non può essere utilizzato o riprodotto, anche parzialmente, senza preventiva autorizzazione '
   'da parte degli Osservatori Digital Innovation del Politecnico di Milano.</span>')

# ---------------- 1. Anagrafica ----------------
form("Q1", '<span style="font-size:29px;"><strong>Anagrafica</strong></span>', [
    ("Nome", None), ("Cognome", None), ("E-mail aziendale", "ValidEmail"),
    ("Ragione sociale dell’azienda", None), ("Job Title", None)])
mc("Q1.6", Q("Settore di attività:", "Selezionare quello prevalente"), [
    "Aerospace & Defence", "Automotive", "Banking and Finance", "Chemical", "Construction",
    "Education", "Energy, Resources & Utility", "Food & Beverage", "Healthcare & Assistance",
    "Hospitality", "ICT & Electronics", "Insurance", "Logistics, Transportation",
    "Manufacturing", "Media and Entertainment", "Pharma", "Public Administration",
    "GDO & Retail", "Services", "Telco", "Tourism", ALTRO])
mc("Q1.7", Q("Dimensione aziendale (numero di dipendenti):"), [
    "Fino a 49 dipendenti", "Da 50 a 249 dipendenti", "Da 250 a 999 dipendenti",
    "Oltre 1.000 dipendenti"], dropdown=True)

# ---------------- 2. Maturità digitale e gestione per processi ----------------
db("Q2", HDR("Maturità digitale e gestione per processi"))
mc("Q2.1", Q("Quale affermazione rispecchia meglio l’orientamento al digitale della sua azienda?", "Risposta singola"), [
    "Investiamo in modo significativo nel digitale, con progetti trasversali su tutte le aree aziendali.",
    "Investiamo in modo significativo nel digitale, ma solo in alcune aree aziendali specifiche.",
    "Investiamo poco nel digitale perché i benefici attesi non sono ancora pienamente chiari alla nostra organizzazione.",
    "Investiamo poco nel digitale perché nel nostro settore il digitale è considerato poco rilevante.",
    "Investiamo poco o nulla nel digitale principalmente per via dei costi (tempi, competenze, risorse) giudicati troppo elevati rispetto ai benefici.",
    ALTRO])
mc("Q2.2", Q("Come descriverebbe il livello di digitalizzazione documentale e di interconnessione dei processi nella sua azienda?",
             "Risposta singola"), [
    "I principali processi aziendali utilizzano ancora documenti cartacei o non digitalizzati.",
    "L’azienda ha iniziato a digitalizzare i documenti, ma molte aree rimangono isolate (i sistemi non dialogano tra loro).",
    "La maggior parte dei processi è digitalizzata, ma i sistemi non sono completamente integrati (esistono ancora barriere o silos informativi).",
    "I processi principali sono completamente digitalizzati e integrati su piattaforme che consentono lo scambio di dati tra sistemi diversi.",
    "I sistemi sono integrati, automatizzati e monitorati in tempo reale tramite infrastruttura cloud, con strumenti che aiutano a prevenire disallineamenti tra i dati dei diversi processi."])
matrix("Q2.3", Q("Quali dei seguenti elementi di gestione per processi sono presenti nella sua azienda?",
                 "Una risposta per riga",
                 note="<sup>1</sup> BPMN (Business Process Model and Notation): standard internazionale per rappresentare "
                      "graficamente i processi con una simbologia condivisa, che rende la mappa leggibile allo stesso modo da "
                      "funzioni e fornitori diversi. Swimlane: diagramma a corsie, in cui ogni corsia raccoglie le attività di "
                      "un ruolo o di una funzione, così da rendere visibili i passaggi di responsabilità lungo il processo. "
                      "SIPOC (Supplier, Input, Process, Output, Customer): schema sintetico che descrive un processo "
                      "elencandone fornitori, input, fasi principali, output e destinatari, usato per delimitarne il "
                      "perimetro prima di analizzarlo."), [
    "Un inventario o mappa dei processi aziendali (process landscape)",
    "Process owner formalmente identificati, con responsabilità definite",
    "Process owner con autorità formale sul ridisegno del processo e sulle sue priorità",
    "KPI di processo con target definiti e monitorati nel tempo",
    "Modellazione dei processi con notazioni standard (es. BPMN, swimlane, SIPOC)<sup>1</sup>",
    "Un repository centrale di processi, procedure e linee guida operative"],
    ["Sì, presente e mantenuto aggiornato", "Sì, ma non aggiornato regolarmente", "In corso di definizione", "No"])
mc("Q2.4", Q("Che quota dei processi aziendali stima sia oggi formalmente mappata?", "Risposta singola"), [
    "Meno del 25%", "Tra il 25% e il 50%", "Tra il 51% e il 75%", "Oltre il 75%", "Non so"])

# ---------------- 3. Approccio alla Process Automation ----------------
db("Q3", HDR("Approccio alla Process Automation",
             "Per Process Automation si intende l’insieme di tecnologie, strumenti e metodologie che consentono di "
             "automatizzare attività e processi aziendali per aumentare efficienza, precisione e velocità, riducendo "
             "l’intervento manuale. Rientrano in questa definizione sia l’automazione tradizionale di attività ripetitive "
             "e regolari (workflow automatici, API, Robotic Process Automation), sia l’automazione intelligente, che "
             "integra machine learning e analisi dei dati e permette di automatizzare attività non rigidamente "
             "strutturate, sia le soluzioni agentiche, in cui sistemi basati su AI pianificano ed eseguono autonomamente "
             "sequenze di azioni per raggiungere un obiettivo." + BR + BR +
             "Salvo diversa indicazione, non si faccia riferimento ai processi fisici (produzione, manutenzione, movimentazione)."))
mc("Q3.1", Q("Quale affermazione rispecchia meglio l’attuale approccio alla Process Automation nella sua azienda?",
             "Risposta singola"), [
    "L’automazione è applicata a specifici dipartimenti o processi, senza una strategia aziendale centralizzata (es. automazione limitata a HR o gestione ordini).",
    "L’automazione è adottata in diversi dipartimenti o processi, ma non è ancora trasversale o parte di una strategia aziendale complessiva (es. automazione in finanza e HR, ma non in supply chain o customer service).",
    "L’automazione è integrata trasversalmente nella strategia aziendale, coinvolgendo più dipartimenti e processi.",
    "Non applichiamo la Process Automation.",
    {"t": "Altro (specificare il tipo di approccio adottato):", "te": True}])
matrix("Q3.2", Q("Come descriverebbe l’atteggiamento prevalente verso l’automazione ai diversi livelli organizzativi?",
                 "Una risposta per riga"),
       ["Top management", "Middle management", "Ruoli operativi"],
       ["Preoccupazione per la sostituzione o la perdita di controllo",
        "Scarsa consapevolezza dei benefici, senza resistenza esplicita",
        "Consapevolezza crescente e interesse a sperimentare",
        "Automazione e AI viste come leva per il valore del lavoro"])
mc("Q3.3", Q("In quale fase del percorso di automazione collocherebbe attualmente la sua azienda?",
             "Risposta singola. Si consideri come unità di conteggio il singolo flusso automatizzato, "
             "indipendentemente dalla sua ampiezza"), [
    B("Sperimentazione iniziale", " (progetti pilota, indicativamente meno di 10 processi automatizzati)."),
    B("Implementazione", " (indicativamente tra 10 e 50 processi automatizzati, estesi a processi trasversali)."),
    B("Scalabilità aziendale", " (indicativamente oltre 50 processi automatizzati, integrati in più dipartimenti)."),
    "Automazione sospesa o progetti “abbandonati”"])
mc("Q3.4A", Q("Con riferimento alla modalità <u>prevalente</u> con cui viene introdotta la Process Automation, indichi "
              "la situazione più vicina alla sua azienda per ciascuno dei due aspetti seguenti.",
              "Una risposta per ciascun aspetto", sub="A — Ampiezza dell’unità automatizzata"), [
    "Prevalentemente singoli task all’interno di una funzione.",
    "Processi completi, ma contenuti all’interno di una singola funzione.",
    "Processi end-to-end che attraversano più funzioni (es. order-to-cash, purchase-to-pay, hire-to-retire).",
    "Non siamo in grado di rispondere."])
mc("Q3.4B", Q(sub="B — Ruolo dell’analisi di processo"), [
    "I processi sono già mappati e ottimizzati in azienda, solo quando si vuole introdurre un’automazione, si analizza il processo ed eventualmente lo si ridisegna;",
    "Processo e automazione vengono progettati insieme, in un unico percorso, senza una fase di ridisegno preliminare.",
    "L’analisi approfondita del processo viene svolta soltanto in una minoranza di occasioni, per i progetti più complessi.",
    "L’automazione viene introdotta senza una preventiva analisi o revisione del processo."])

# ---------------- 4. Tecnologie di automazione ----------------
db("Q4", HDR("Tecnologie di automazione"))
mc("Q4.1", Q("Quali di questi strumenti sono presenti nella sua realtà?",
             "Risposta multipla – selezionare tutte le opzioni applicabili"), [
    B("Soluzioni di Robotic Process Automation", " – esempi: UiPath, Blue Prism, Automation Anywhere"),
    B("Soluzioni di API automation e integrazione tra sistemi", " – esempi: Boomi, MuleSoft, Workato"),
    B("Strumenti di Business Process Management", " – esempi: Camunda, Appian, Pega"),
    B("Strumenti di Workflow Automation o piattaforme low-code", " – esempi: n8n, Nintex, Power Automate, Zapier"),
    B("Strumenti di Process Mining o Process Intelligence", " – esempi: Celonis, Apromore"),
    B("Strumenti di Intelligent Document Processing", " – esempi: ABBYY, Rossum, moduli IDP delle piattaforme di automazione"),
    B("Piattaforme di sviluppo o orchestrazione di agenti AI", " – esempi: Microsoft Copilot Studio, Google Vertex AI Agent Builder, LangGraph, CrewAI, moduli agentici delle piattaforme RPA"),
    {"t": "Nessuno di questi", "excl": True}], multi=True, rand=adv_rand_fixed_last)

# ---------------- 5. Mappatura dei processi automatizzati ----------------
db("Q5", HDR("Mappatura dei processi automatizzati",
             "In questa sezione le chiediamo di indicare dove l’automazione è effettivamente applicata, utilizzando una "
             "classificazione per famiglie di processo anziché per aree organizzative. Le famiglie elencate sono "
             "indipendenti dalla struttura organizzativa della sua azienda: le consideri come raggruppamenti di attività, "
             "a prescindere da quale funzione le presidia." + BR + BR +
             "<strong>Automazione tradizionale</strong>: tecnologie che automatizzano attività ripetitive e basate su "
             "regole predeterminate (workflow, RPA, integrazioni via API)." + BR +
             "<strong>Automazione intelligente</strong>: soluzioni che integrano AI, machine learning e analisi dei dati, "
             "estendendo l’automazione ad attività non rigidamente strutturate." + BR +
             "<strong>Agenti AI autonomi</strong>: sistemi che pianificano ed eseguono autonomamente sequenze di azioni "
             "per raggiungere un obiettivo definito, attivando altri sistemi aziendali."))
matrix("Q5.1", Q("Per ciascuna famiglia di processo, indichi quali tipologie di automazione sono oggi in uso nella sua azienda.",
                 "Risposta multipla per riga sulle prime tre colonne; le ultime due colonne sono esclusive"), [
    B("Strategia, governance e organizzazione", " (pianificazione strategica, performance management, policy e deleghe, struttura organizzativa)"),
    B("Risorse umane e sviluppo delle persone", " (selezione e onboarding, formazione, valutazione della performance, welfare, workforce planning)"),
    B("Ricerca, sviluppo e innovazione dell’offerta", " (scouting tecnologico, ideazione, sviluppo prodotto, prototipazione, test, lancio, proprietà intellettuale)"),
    B("Marketing, vendite e canali commerciali", " (analisi di mercato, brand, campagne, advertising, contenuti, gestione lead, offerte e preventivi, digital commerce)"),
    B("Acquisti e gestione dei fornitori", " (strategie di sourcing, scouting e qualifica, contrattualizzazione, procurement operativo, vendor rating)"),
    B("Operations, produzione, logistica e fulfillment", " (pianificazione della domanda e degli approvvigionamenti, esecuzione, magazzino, evasione ordini, trasporti, qualità, resi)"),
    B("Customer service e gestione della relazione con il cliente", " (assistenza, dati cliente, reclami, post-vendita, esperienza e fidelizzazione, misurazione della soddisfazione)"),
    B("Amministrazione, finanza e controllo", " (contabilità e fatturazione, chiusure e bilancio, budgeting e controllo di gestione, tesoreria e pagamenti)"),
    B("Legal, contrattualistica e gestione degli asset", " (consulenza legale, ciclo di vita dei contratti, asset e facility management)"),
    B("IT, dati e cybersecurity", " (strategia e architetture IT, sviluppo e integrazione software, esercizio dei sistemi, gestione dei dati, sicurezza, identità digitali)"),
    B("Risk management, compliance e sostenibilità", " (gestione dei rischi, conformità normativa, audit interno, continuità operativa, ESG, relazioni istituzionali)")],
    ["Automazione tradizionale", "Automazione intelligente (AI)", "Agenti AI autonomi", "Nessuna automazione",
     "Non applicabile"], multi=True, excl_cols=(4, 5), rand_rows=True)

# famiglie approfondibili: (lettera 5.2, riga 5.1, etichetta, righe matrice 5.3)
FAM = [
    ("a", 8, "Amministrazione, finanza e controllo", [
        "Registrazione contabile e gestione del ciclo di fatturazione attiva e passiva, inclusa la fatturazione elettronica",
        "Controlli di coerenza tra fattura, ordine e contratto e gestione degli scostamenti",
        "Chiusure contabili periodiche e predisposizione del bilancio",
        "Budgeting, forecast e analisi degli scostamenti rispetto al consuntivo",
        "Gestione degli incassi, solleciti e riconciliazioni bancarie",
        "Adempimenti fiscali e conservazione digitale a norma"]),
    ("b", 5, "Acquisti e gestione dei fornitori", [
        "Analisi della spesa per categoria e supply market intelligence",
        "Scouting, qualifica e onboarding dei fornitori (RFI, RFQ, RFP)",
        "Negoziazione e gestione del ciclo di vita dei contratti di fornitura",
        "Procurement operativo: richieste d’acquisto, emissione ordini, ricezione e ciclo procure-to-pay",
        "Vendor rating e monitoraggio delle performance dei fornitori",
        "Qualifica ESG dei fornitori e monitoraggio della compliance di filiera"]),
    ("c", 6, "Operations, produzione, logistica e fulfillment", [
        "Previsione della domanda e Sales & Operations Planning",
        "Pianificazione degli approvvigionamenti e ottimizzazione delle scorte",
        "Schedulazione e controllo dell’esecuzione produttiva o dell’erogazione del servizio",
        "Gestione del magazzino e delle movimentazioni (inventari, picking, packing)",
        "Gestione degli ordini cliente ed evasione (order fulfillment)",
        "Pianificazione dei trasporti, tracciamento e notifiche di consegna",
        "Controllo qualità e gestione dei resi (reverse logistics)"]),
    ("d", 7, "Customer service e gestione della relazione con il cliente", [
        "Gestione delle anagrafiche cliente, single customer view e qualità del dato CRM",
        "Ricezione e smistamento delle richieste (ticketing, classificazione, routing)",
        "Risoluzione delle richieste e gestione delle escalation",
        "Gestione dei reclami e analisi delle cause",
        "Servizi post-vendita e pianificazione degli interventi tecnici",
        "Raccolta dei feedback e misurazione della soddisfazione (NPS, CSAT, CES)",
        "Programmi di loyalty, retention e personalizzazione"]),
]
mc("Q5.2", Q("Tra le famiglie seguenti, selezioni al massimo due su cui desidera fornire un maggiore livello di dettaglio.",
             "Risposta multipla, massimo 2 – Facoltativo"),
   [lab for _, _, lab, _ in FAM], multi=True, force=False, maxc=2)
COLS_53 = ["Automatizzato – automazione tradizionale", "Automatizzato – automazione intelligente o agentic",
           "Non automatizzato, prioritario nei prossimi 12 mesi", "Non automatizzato / non rilevante"]
for key, _, lab, rows in FAM:
    matrix("Q5.3" + key, Q("Per le famiglie selezionate, indichi lo stato di automazione dei singoli processi.",
                            "Una risposta per riga – Facoltativo", sub=lab), rows, COLS_53, force=False)

# ---------------- 6. Agentic Automation ----------------
db("Q6", HDR("Agentic Automation"))
mc("Q6.1", Q("In relazione all’Agentic AI, dove posizionerebbe la sua realtà aziendale?",
             "Risposta singola – indichi la situazione più vicina alla vostra realtà"), [
    "Non ho mai sentito il termine.",
    "Conosco personalmente il tema, ma non è mai stato discusso in azienda.",
    "Abbiamo discusso del tema in azienda, ma non abbiamo ancora avviato valutazioni o sperimentazioni.",
    "Stiamo analizzando le potenzialità o conducendo studi interni sul tema.",
    "Abbiamo avviato sperimentazioni su ambiti o processi selezionati.",
    "Stiamo estendendo l’utilizzo di agenti autonomi in alcuni processi aziendali.",
    "L’Agentic AI è parte integrante della strategia di automazione o dei sistemi operativi interni."])
mc("Q6.2", Q("Quali capacità hanno le soluzioni di Agentic AI presenti in azienda o in fase di valutazione?",
             "Risposta multipla – selezionare tutte le opzioni applicabili"), [
    B("Autonomia operativa", " – la soluzione esegue attività o processi senza intervento umano costante."),
    B("Collaborazione e adattamento multi-agente", " – più agenti cooperano e si coordinano per obiettivi comuni."),
    B("Uso di strumenti", " – l’agente attiva autonomamente altri sistemi o applicazioni aziendali (CRM, ERP, ticketing)."),
    B("Accesso a memoria e apprendimento continuo", " – la soluzione conserva informazioni e migliora le proprie azioni nel tempo."),
    B("Orientamento agli obiettivi", " – l’agente pianifica e sceglie autonomamente le azioni necessarie."),
    B("Interazione conversazionale", " – l’agente risponde a domande degli utenti o fornisce informazioni."),
    B("Esecuzione di flussi di lavoro predefiniti", " – la soluzione segue script o regole fisse senza adattarsi al contesto."),
    B("Generazione di contenuti", " – l’agente produce testi, immagini o report su richiesta."),
    B("Supporto all’utente tramite suggerimenti o raccomandazioni", ", senza agire autonomamente."),
    ALTRO,
    "Non ho abbastanza informazioni per rispondere."], multi=True)

# ---------------- 7. Organizzazione e competenze ----------------
db("Q7", HDR("Organizzazione e competenze"))
mc("Q7.1", Q("Esiste in azienda una funzione o un ruolo che presidia la gestione dei processi (BPM, Process Excellence, Organizzazione)?",
             "Risposta singola"), [
    "Sì, una funzione dedicata, con risorse proprie e un mandato formalizzato",
    "Sì, un presidio part-time collocato all’interno di un’altra funzione (es. Organizzazione, IT, Operations)",
    "No, ma i process owner operano in autonomia nelle rispettive aree",
    "No, non esiste un presidio strutturato sulla gestione dei processi"])
mc("Q7.2", Q("Come sono organizzati i presidi sull’automazione dei processi e sull’intelligenza artificiale?",
             "Risposta singola"), [
    "Un unico team presidia sia l’automazione dei processi sia l’AI.",
    "Esistono due presidi distinti, che lavorano su iniziative congiunte con una governance condivisa.",
    "Esistono due presidi distinti, che si coordinano caso per caso, senza meccanismi strutturati.",
    "Esistono due presidi distinti, che operano in modo sostanzialmente indipendente.",
    "Esiste un presidio sull’automazione dei processi, ma non sull’AI.",
    "Esiste un presidio sull’AI, ma non sull’automazione dei processi.",
    "Non abbiamo un team dedicato: le competenze sono distribuite nelle funzioni di business",
    "Non abbiamo competenze interne dedicate: ci affidiamo a fornitori o consulenti esterni",
    "Non esiste alcun presidio strutturato sull’automazione e AI"])
mc("Q7.3", Q("Quali elementi sono condivisi tra il presidio sull’automazione e quello sull’AI?",
             "Risposta multipla – selezionare tutte le opzioni applicabili"), [
    "Un budget unico per i due presidi",
    "Una pipeline o un backlog unico dei casi d’uso",
    "Criteri di prioritizzazione comuni",
    "Piattaforme tecnologiche comuni",
    "Metriche e KPI comuni",
    "Un unico sponsor o referente a livello di direzione",
    "Processi comuni di risk management e compliance",
    {"t": "Nessuno di questi elementi è condiviso", "excl": True}], multi=True)
mc("Q7.4", Q("Chi detiene il budget per le iniziative di automazione?", "Risposta singola"), [
    "Il presidio dell’automazione, con un budget dedicato e autonomo",
    "Il presidio dell’automazione, ma all’interno di un budget più ampio (IT, trasformazione, innovazione)",
    "Comitato esecutivo o Consiglio di amministrazione",
    "Amministratore delegato o Direzione generale",
    "Direzione Sistemi Informativi (CIO/CTO)",
    "Direzione Operations",
    "Direzione Amministrazione, Finanza e Controllo",
    "Le singole funzioni di business, con budget autonomi",
    "Non esiste un budget dedicato all’automazione: le iniziative sono finanziate di volta in volta",
    ALTRO])
mc("Q7.5", Q("Quali sono le principali motivazioni per cui la sua azienda non dispone di figure dedicate all’automazione?",
             "Risposta multipla – selezionare i due fattori principali"), [
    "Competenze interne limitate sui temi di automazione",
    "Difficoltà a reperire sul mercato le figure necessarie",
    "Priorità aziendali concentrate su altri ambiti strategici",
    "Costi considerati troppo elevati per creare o mantenere un team interno",
    "Scarsa consapevolezza o visione strategica sul valore dell’automazione",
    "Cultura aziendale ancora poco orientata all’innovazione o alla sperimentazione",
    "Preferenza per il supporto di consulenti o fornitori esterni",
    ALTRO], multi=True, maxc=2)
mc("Q7.6", Q("Nei prossimi 12 mesi è previsto un impatto sull’organico delle aree interessate dall’automazione?",
             "Risposta singola"), [
    "Riduzione significativa dell’organico",
    "Riduzione contenuta, gestita prevalentemente attraverso il turnover naturale",
    "Organico invariato, con ricollocazione delle persone su attività diverse",
    "Organico invariato, senza modifiche sostanziali alle mansioni",
    "Crescita dell’organico, per l’ingresso di nuove competenze",
    "Non siamo in grado di formulare una previsione"])

# ---------------- 8. Esternalizzazione ----------------
db("Q8", HDR("Esternalizzazione"))
mc("Q8.1", Q("In che modo l’automazione e l’intelligenza artificiale stanno modificando il ricorso a servizi o attività esternalizzate nella sua azienda?",
             "Risposta multipla – selezionare tutte le opzioni applicabili",
             note="Tra le attività potenzialmente esternalizzate rientrano, ad esempio: contabilità e gestione finanziaria, "
                  "payroll, customer service, data entry, gestione documentale, reportistica e analisi dati, supporto IT "
                  "di primo livello, gestione ordini o approvazioni cicliche, amministrazione del personale, risposte a "
                  "richieste standard di clienti o fornitori."), [
    "Abbiamo riportato completamente all’interno alcune attività prima gestite interamente da fornitori esterni, grazie alla possibilità di automatizzarle.",
    "Abbiamo parzialmente ridotto il ricorso a fornitori esterni, automatizzando internamente alcune attività prima affidate all’esterno.",
    "Vorremmo automatizzare processi oggi gestiti da fornitori esterni entro 12 mesi.",
    "Stiamo valutando di automatizzare processi oggi gestiti da fornitori esterni, senza obiettivi temporali definiti.",
    "Abbiamo aumentato il ricorso a fornitori esterni",
    {"t": "Al momento non sono avvenuti cambiamenti significativi nel livello di esternalizzazione.", "excl": True},
    ALTRO], multi=True)
mc("Q8.2", Q("Quali di questi servizi precedentemente esternalizzati sono stati maggiormente impattati?",
             "Risposta multipla – massimo 3 opzioni"), [
    "Contabilità e gestione finanziaria",
    "Payroll ed elaborazione stipendi",
    "Customer service (gestione ticket, risposte automatiche)",
    "Data entry e inserimento dati",
    "Gestione documentale",
    "Reportistica e analisi dati",
    "Supporto IT di primo livello (help desk)",
    "Gestione ordini o approvazioni cicliche",
    "Amministrazione del personale (es. organizzazione turni)",
    "Risposte a richieste standard di clienti o fornitori",
    ALTRO], multi=True, maxc=3)

# ---------------- 9. Aspettative e risultati ----------------
db("Q9", HDR("Aspettative e risultati",
             "Le domande seguenti non chiedono quanto bene abbiano funzionato le iniziative, ma quanto si siano "
             "discostate da ciò che l’azienda si attendeva prima di avviarle. Risponda sulla base delle iniziative "
             "effettivamente avviate, non di quelle soltanto valutate."))
matrix("Q9.1", Q("Rispetto alle aspettative iniziali, come si sono rivelate le seguenti dimensioni nelle iniziative di "
                 "automazione intelligente o agentica avviate negli ultimi 24 mesi?", "Una risposta per riga"), [
    "Qualità e completezza dei dati disponibili",
    "Affidabilità e prevedibilità degli output prodotti dall’AI",
    "Sforzo di progettazione e messa a punto delle soluzioni (prompt, flussi, guardrail)",
    "Facilità di integrazione con i sistemi aziendali esistenti",
    "Tempo necessario per portare la soluzione a regime",
    "Adozione da parte degli utenti",
    "Beneficio economico effettivamente ottenuto"],
    ["Meglio del previsto", "In linea con le aspettative", "Peggio del previsto", "Molto peggio del previsto",
     "Non applicabile"])
mc("Q9.2", Q("Quale affermazione descrive meglio la vostra esperienza rispetto agli scostamenti rilevati?",
             "Risposta singola"), [
    "I problemi emersi erano criticità preesistenti che l’automazione ha reso visibili (qualità dei dati, processi non standardizzati, responsabilità non definite)",
    "I problemi erano specifici della tecnologia e non prevedibili in fase di valutazione",
    "Le aspettative iniziali erano state fissate senza un’analisi sufficiente",
    "Le aspettative erano corrette, ma i tempi di realizzazione si sono allungati",
    "Non sapremmo attribuire lo scostamento"])

# ---------------- 10. Barriere, investimenti e prossimi passi ----------------
db("Q10", HDR("Barriere, investimenti e prossimi passi"))
BARRIERE = [
    "Limitate competenze interne o difficoltà nel reperire risorse specializzate",
    "Costi di implementazione e di esercizio troppo elevati",
    "Difficoltà a costruire il business case o a dimostrare il ritorno economico",
    "Sistemi legacy o difficoltà di integrazione con i sistemi aziendali esistenti",
    "Qualità, disponibilità o accessibilità dei dati",
    "Mancanza di una chiara strategia o di sponsorship del top management",
    "Resistenza al cambiamento: disaccordo sul merito o timori sugli impatti occupazionali",
    "Fatica da cambiamento: sovraccarico dovuto al numero di iniziative in corso",
    "Complessità tecnica o tempi di implementazione troppo lunghi",
    "Preoccupazioni di sicurezza informatica e protezione dei dati",
    "Incertezza o onere della conformità normativa (AI Act, GDPR, normative di settore)",
    "Assenza di presidi di governance sull’uso dell’AI nei processi (policy, risk management, audit)",
    "Processi poco standardizzati o troppo variabili per essere automatizzati",
    "Preferenza per il mantenimento di processi manuali più flessibili",
    "Affidabilità e prevedibilità degli output prodotti dall’AI",                          # 15: non per tradizionale
    "Assenza di responsabilità chiare sugli output e sulle azioni dei sistemi automatici",  # 16: idem
    "Nessuna barriera rilevante",                                                           # 17: esclusiva
]


def barriere(skip=()):
    return [{"t": t, "id": i, "key": str(i), "excl": i == 17}
            for i, t in enumerate(BARRIERE, start=1) if i not in skip]


S101 = "Quali sono le principali barriere che la sua azienda percepisce oggi nell’introduzione di %s?"
mc("Q10.1a", Q(S101 % "soluzioni di <u>automazione tradizionale</u>", "Selezionare al massimo 3 barriere"),
   barriere(skip=(15, 16)), multi=True, maxc=3)
mc("Q10.1b", Q(S101 % "soluzioni di <u>automazione intelligente</u>", "Selezionare al massimo 3 barriere"),
   barriere(), multi=True, maxc=3)
mc("Q10.1c", Q(S101 % "<u>soluzioni agentiche</u>", "Selezionare al massimo 3 barriere"),
   barriere(), multi=True, maxc=3)
mc("Q10.2", Q("In quale fascia di spesa rientra, per il 2026, la spesa della sua azienda in software e servizi legati all’automazione dei processi?",
              "Risposta singola. Si considerino, ad esempio: licenze software per workflow automation, RPA, process "
              "mining, piattaforme AI e agentiche; progetti avviati con partner tecnologici o consulenti esterni sul tema"), [
    "Nessuna spesa", "Inferiore a 10.000 euro", "Tra 10.000 e 25.000 euro", "Tra 25.001 e 50.000 euro",
    "Tra 50.001 e 100.000 euro", "Tra 100.001 e 250.000 euro", "Tra 250.001 e 500.000 euro",
    "Tra 500.001 e 1 milione di euro", "Oltre 1 milione di euro", "Non so / dato non disponibile"])
sbs_spesa("Q10.3", Q("Qual è la dinamica della spesa rispetto al 2025 e la previsione per il 2027?", "Una risposta per riga"),
          ["Variazione rispetto al 2025", "Previsione sul 2027"],
          ["Più che raddoppio", "Raddoppio", "In crescita tra il 50% e il 100%", "In crescita tra il 20% e il 50%",
           "In crescita tra il 10% e il 20%", "In crescita di meno del 10%", "Stabile", "In diminuzione"])
mc("Q10.4_ns", Q("Come si ripartisce approssimativamente la spesa 2026 tra le diverse tipologie di automazione?"),
   ["Non siamo in grado di stimare la ripartizione"], multi=True, force=False)
cs("Q10.4", Q(instr="Indicare una percentuale approssimativa; il totale deve essere pari a 100%"), [
    "Automazione tradizionale (RPA, workflow, integrazioni via API)",
    "Automazione intelligente non agentica (AI applicata ai processi, IDP, modelli predittivi, elaborazione del linguaggio)",
    "Soluzioni agentiche (agenti autonomi, orchestrazione multi-agente)"])
mc("Q10.5", Q("La sua azienda è in grado di quantificare il beneficio economico delle iniziative di automazione?",
              "Risposta singola"), [
    "Sì, con una metodologia strutturata, applicata sistematicamente e validata dal controllo di gestione",
    "Sì, con una metodologia strutturata applicata dal team di automazione, non validata dal controllo di gestione",
    "Solo per alcuni progetti, con stime ad hoc",
    "No, ma stiamo introducendo una misurazione strutturata",
    "No, e al momento non è una priorità"])
S106 = "Qual è l’ordine di grandezza del beneficio economico annuo attribuito all’automazione dei processi per il 2026?"
I106 = "Compili almeno una delle due righe, nell’unità di misura che utilizzate internamente"
mc("Q10.6a", Q(S106, I106, sub="Beneficio economico annuo, espresso in euro"), [
    "Nessun beneficio netto", "Inferiore a 10.000 euro", "Tra 10.000 e 25.000", "Tra 25.001 e 50.000",
    "Tra 50.001 e 100.000", "Tra 100.001 e 250.000", "Tra 250.001 e 500.000", "Tra 500.001 e 1 milione",
    "Tra 1 e 2,5 milioni", "Tra 2,5 e 5 milioni", "Oltre 5 milioni", {"t": "Non applicabile", "key": "na"}])
mc("Q10.6b", Q(S106, I106, sub="Beneficio annuo, espresso in FTE equivalenti liberati"), [
    "Meno di 1", "Tra 1 e 3", "Tra 4 e 10", "Tra 11 e 25", "Tra 26 e 50", "Tra 51 e 100", "Oltre 100",
    {"t": "Non applicabile", "key": "na"}])
mc("Q10.7", Q("Quali sono i prossimi passi che la sua azienda intende compiere in ambito automazione nei prossimi 12 mesi?",
              "Risposta multipla – selezionare al massimo tre priorità già identificate come rilevanti o su cui si sta già lavorando"), [
    "Estendere o potenziare i processi automatizzati in nuove aree aziendali",
    "Introdurre tecnologie di Agentic AI",
    "Introdurre tecnologie di automazione tradizionale (es. piattaforma RPA)",
    "Introdurre tecnologie di automazione intelligente (es. Intelligent Document Processing)",
    "Migliorare l’integrazione tra soluzioni di automazione e sistemi aziendali esistenti (ERP, CRM, legacy)",
    "Definire o aggiornare la strategia aziendale sull’automazione",
    "Mappare e ridisegnare i processi come precondizione all’automazione",
    "Rafforzare le competenze interne attraverso formazione o nuove assunzioni",
    "Misurare in modo più strutturato l’impatto dei progetti tramite nuovi KPI o sistemi di monitoraggio",
    "Avviare progetti pilota di automazione intelligente",
    "Coinvolgere nuove funzioni di business nelle progettualità di automazione",
    "Consolidare e ottimizzare i processi già automatizzati per migliorarne efficienza, affidabilità e manutenibilità",
    "Rafforzare le partnership con fornitori o startup tecnologiche",
    "Avviare iniziative di change management e promozione di una cultura dell’innovazione legata all’automazione",
    "Definire policy e presidi di governance sull’uso dell’AI nei processi",
    ALTRO], multi=True, maxc=3)

# ---------------- Esclusione (testo 2025) ----------------
db("Esclusione",
   "Questo sondaggio ha l’obiettivo di mappare le medie e grandi imprese del settore privato che utilizzano tecnologie "
   "di Process Automation. Poiché, in base alle informazioni da lei fornite, la sua azienda non rientra nel target, il "
   "questionario è stato concluso automaticamente. La ringraziamo sinceramente per la disponibilità e per il tempo che "
   "ci ha dedicato.")

# ==========================================================================
# DISPLAY LOGIC (tutti i filtri del documento, senza elementi nel survey flow)
# ==========================================================================


def A3():      # 3.1 diversa da d) «Non applichiamo la Process Automation»
    return [c_sel("Q3.1", k) for k in "abce"]


def ADOPT():   # prosegue chi NON ha (3.1 = d) e (4.1 = h)  <=>  3.1 in a,b,c,e  oppure  almeno uno strumento in 4.1
    return A3() + [c_sel("Q4.1", k) for k in "abcdefg"]


def E(key):    # famiglia selezionabile alla 5.2: alla 5.1 almeno una delle prime tre colonne
    row = next(r for k, r, _, _ in FAM if k == key)
    return [c_cell("Q5.1", row, c) for c in (1, 2, 3)]


def AI51():    # alla 5.1 almeno una casella «Automazione intelligente» o «Agenti AI autonomi»
    return [c_cell("Q5.1", r, c) for r in range(1, 12) for c in (2, 3)]


def SPESA():   # 10.2 = fascia da b) a i)
    return [c_sel("Q10.2", k) for k in "bcdefghi"]


set_dl("Q2.4", L(("Or", [c_cell("Q2.3", 1, c) for c in (1, 2, 3)])))      # riga 1 della 2.3 diversa da «No»
for t in ("Q3.3", "Q3.4A", "Q3.4B"):
    set_dl(t, L(("Or", A3())))
for t in ("Q5", "Q5.1"):
    set_dl(t, L(("Or", ADOPT())))
# 5.2: solo se le famiglie selezionabili sono almeno due (ogni terna di famiglie ne contiene almeno una)
fk = [k for k, _, _, _ in FAM]
terne = [[x for x in fk if x != escl] for escl in fk]
set_dl("Q5.2", L(("Or", ADOPT()), *[("Or", sum((E(x) for x in t3), [])) for t3 in terne]))
for k in fk:
    QUESTIONS["Q5.2"]["payload"]["Choices"][QUESTIONS["Q5.2"]["ck"][k]]["DisplayLogic"] = L(("Or", E(k)))
# 5.3x: famiglia scelta alla 5.2, oppure unica famiglia selezionabile (5.2 saltata)
for k in fk:
    others = [(x, r) for x, r, _, _ in FAM if x != k]
    clauses = [("Or", [c_sel("Q5.2", k), c_cell("Q5.1", r, c, "NotSelected")]) for _, r in others for c in (1, 2, 3)]
    set_dl("Q5.3" + k, L(("Or", ADOPT()), ("Or", E(k)), *clauses))
set_dl("Q6.2", L(("Or", [c_sel("Q6.1", k) for k in "defg"])))
for t in ("Q7.2", "Q7.6", "Q8", "Q8.1"):
    set_dl(t, L(("Or", ADOPT())))
set_dl("Q7.3", L(("Or", ADOPT()), ("Or", [c_sel("Q7.2", k) for k in "bcd"])))
set_dl("Q7.4", L(("Or", ADOPT()), ("Or", [c_sel("Q7.3", "a", "NotSelected")])))
set_dl("Q7.5", L(("Or", ADOPT()), ("Or", [c_sel("Q7.2", k) for k in "fghi"])))
set_dl("Q8.2", L(("Or", ADOPT()), ("Or", [c_sel("Q8.1", "a"), c_sel("Q8.1", "b")])))
for t in ("Q9", "Q9.1"):
    set_dl(t, L(("Or", A3()), ("Or", AI51())))
set_dl("Q9.2", L(("Or", A3()), ("Or", AI51()),
                 ("Or", [c_cell("Q9.1", r, c) for r in range(1, 8) for c in (3, 4)])))
for t in ("Q10.3", "Q10.4_ns"):
    set_dl(t, L(("Or", SPESA())))
# campo percentuali: in-page, scompare se si spunta «Non siamo in grado di stimare la ripartizione»
QUESTIONS["Q10.4"]["payload"]["InPageDisplayLogic"] = L(("Or", SPESA()),
                                                         ("Or", [c_sel("Q10.4_ns", "a", "NotSelected")]), inpage=True)
for t in ("Q10.6a", "Q10.6b"):
    set_dl(t, L(("Or", [c_sel("Q10.5", k) for k in "abc"])))
# «compili almeno una delle due righe»: se in euro è «Non applicabile», in FTE l'opzione non compare
QUESTIONS["Q10.6b"]["payload"]["Choices"][QUESTIONS["Q10.6b"]["ck"]["na"]]["DisplayLogic"] = \
    L(("Or", [c_sel("Q10.6a", "na", "NotSelected")]))
set_dl("Esclusione", L(("Or", [c_sel("Q1.6", "q"), c_sel("Q1.7", "a")])))

# ==========================================================================
# BLOCCHI (come nel 2025: Introduzione + Questionario con interruzioni di pagina)
# ==========================================================================
PB = "PB"
PAGES = [
    ["Q1", "Q1.6", "Q1.7"],
    ["Q2", "Q2.1", "Q2.2", "Q2.3"], ["Q2.4"],
    ["Q3", "Q3.1", "Q3.2"], ["Q3.3", "Q3.4A", "Q3.4B"],
    ["Q4", "Q4.1"],
    ["Q5", "Q5.1"], ["Q5.2"], ["Q5.3a"], ["Q5.3b"], ["Q5.3c"], ["Q5.3d"],
    ["Q6", "Q6.1"], ["Q6.2"],
    ["Q7", "Q7.1", "Q7.2"], ["Q7.3"], ["Q7.4", "Q7.5", "Q7.6"],
    ["Q8", "Q8.1"], ["Q8.2"],
    ["Q9", "Q9.1"], ["Q9.2"],
    ["Q10", "Q10.1a"], ["Q10.1b"], ["Q10.1c"], ["Q10.2"], ["Q10.3"], ["Q10.4_ns", "Q10.4"],
    ["Q10.5"], ["Q10.6a"], ["Q10.6b"], ["Q10.7"],
    ["Esclusione"],
]
ESCL_QID = QUESTIONS["Esclusione"]["qid"]


def skip_to_escl(tag, key, n):
    q = QUESTIONS[tag]
    cid = q["ck"][key]
    loc = "q://%s/SelectableChoice/%s" % (q["qid"], cid)
    lab = q["clabels"][cid]
    return [OrderedDict([
        ("SkipLogicID", n), ("ChoiceLocator", loc), ("Condition", "Selected"), ("SkipToDestination", ESCL_QID),
        ("Locator", loc),
        ("SkipToDescription", "%s <strong>%s</strong>  <strong>è selezionato</strong>" % (short(q["text"], 27), lab)),
        ("Description", "Condizione: <strong title=\"%s\">%s</strong> <strong>è selezionato</strong>. Salta a: "
                        "<strong>Questo sondaggio ha l’obiettivo di ma...</strong>." % (lab, lab)),
        ("QuestionID", q["qid"])])]


SKIPS = {"Q1.6": skip_to_escl("Q1.6", "q", 1), "Q1.7": skip_to_escl("Q1.7", "a", 2)}

els = []
for i, page in enumerate(PAGES):
    if i:
        els.append({"Type": "Page Break"})
    for t in page:
        e = OrderedDict([("Type", "Question"), ("QuestionID", QUESTIONS[t]["qid"])])
        if t in SKIPS:
            e["SkipLogic"] = SKIPS[t]
        els.append(e)

BLOCK_OPTS = OrderedDict([("BlockLocking", "false"), ("RandomizeQuestions", "false"), ("BlockVisibility", "Expanded")])
BL_INTRO, BL_TRASH, BL_MAIN = rid("BL_"), rid("BL_"), rid("BL_")
BLOCKS = [
    OrderedDict([("Type", "Default"), ("Description", "Introduzione"), ("ID", BL_INTRO),
                 ("BlockElements", [{"Type": "Question", "QuestionID": QUESTIONS["A"]["qid"]}]),
                 ("Options", BLOCK_OPTS)]),
    OrderedDict([("Type", "Trash"), ("Description", "Domande eliminate nel cestino / inutilizzate"),
                 ("ID", BL_TRASH), ("BlockElements", [])]),
    OrderedDict([("Type", "Standard"), ("SubType", ""), ("Description", "Questionario"), ("ID", BL_MAIN),
                 ("BlockElements", els), ("Options", BLOCK_OPTS)]),
]
_used = sorted(e["QuestionID"] for b in BLOCKS for e in b["BlockElements"] if e["Type"] == "Question")
assert _used == sorted(q["qid"] for q in QUESTIONS.values()), "domande non assegnate o duplicate"

# Survey flow: SOLO i due blocchi, uno dopo l'altro (pulsante Indietro sempre disponibile)
FLOW_ROOT = OrderedDict([
    ("Flow", [OrderedDict([("ID", BL_INTRO), ("Type", "Block"), ("FlowID", "FL_2")]),
              OrderedDict([("ID", BL_MAIN), ("Type", "Standard"), ("FlowID", "FL_3")])]),
    ("Properties", {"Count": 3}), ("FlowID", "FL_1"), ("Type", "Root")])

# ==========================================================================
# OPZIONI SONDAGGIO (identiche al 2025: tema polimi, pulsante Indietro, messaggio finale di libreria)
# ==========================================================================
SURVEY_OPTIONS = OrderedDict([
    ("BackButton", "true"), ("SaveAndContinue", "true"), ("SurveyProtection", "PublicSurvey"),
    ("BallotBoxStuffingPrevention", "false"), ("NoIndex", "Yes"), ("SecureResponseFiles", "true"),
    ("SurveyExpiration", "None"), ("SurveyTermination", "DisplayMessage"), ("Header", ""), ("Footer", ""),
    ("ProgressBarDisplay", "NoText"), ("PartialData", "+1 week"), ("ValidationMessage", None),
    ("PreviousButton", ""), ("NextButton", " → "), ("SurveyTitle", "Sondaggio IBPA"),
    ("SkinLibrary", "polimi"), ("SkinType", "templated"),
    ("Skin", OrderedDict([("brandingId", None), ("templateId", "*base"), ("overrides", None)])),
    ("NewScoring", 1),
    ("SurveyMetaDescription", "La modalità più semplice, affidabile ed efficace per raccogliere i dati delle "
                              "esperienze. Scopri Experience Management e prova subito un account gratuito."),
    ("EOSMessage", EOS_MSG_2025), ("ShowExportTags", "false"), ("CollectGeoLocation", "false"),
    ("PasswordProtection", "No"), ("AnonymizeResponse", "No"), ("RefererCheck", "No"),
    ("BallotBoxStuffingPreventionBehavior", None), ("BallotBoxStuffingPreventionMessage", None),
    ("BallotBoxStuffingPreventionMessageLibrary", None), ("BallotBoxStuffingPreventionURL", None),
    ("RecaptchaV3", "false"), ("ConfirmStart", False), ("AutoConfirmStart", False), ("RelevantID", "false"),
    ("RelevantIDLockoutPeriod", "+30 days"), ("UseCustomSurveyLinkCompletedMessage", None),
    ("SurveyLinkCompletedMessage", None), ("SurveyLinkCompletedMessageLibrary", None), ("ResponseSummary", "No"),
    ("EOSMessageLibrary", LIB_2025), ("EOSRedirectURL", "http://"), ("EmailThankYou", "false"),
    ("ThankYouEmailMessageLibrary", None), ("ThankYouEmailMessage", None), ("ValidateMessage", "false"),
    ("ValidationMessageLibrary", None), ("InactiveSurvey", "DefaultMessage"), ("PartialDeletion", None),
    ("PartialDataCloseAfter", "LastActivity"), ("InactiveMessageLibrary", None), ("InactiveMessage", None),
    ("AvailableLanguages", {"IT": []}), ("ProtectSelectionIds", True),
])


def element(el, primary, secondary, tertiary, payload):
    return OrderedDict([("SurveyID", SURVEY_ID), ("Element", el), ("PrimaryAttribute", primary),
                        ("SecondaryAttribute", secondary), ("TertiaryAttribute", tertiary), ("Payload", payload)])


elements = [
    element("BL", "Survey Blocks", None, None, BLOCKS),
    element("FL", "Survey Flow", None, None, FLOW_ROOT),
    element("PROJ", "CORE", None, "1.1.0", {"ProjectCategory": "CORE", "SchemaVersion": "1.1.0"}),
    element("QC", "Survey Question Count", str(len(QUESTIONS)), None, None),
    element("RS", RS_ID, "Default Response Set", None, None),
    element("SCO", "Scoring", None, None, OrderedDict([
        ("ScoringCategories", []), ("ScoringCategoryGroups", []), ("ScoringSummaryCategory", None),
        ("ScoringSummaryAfterQuestions", 0), ("ScoringSummaryAfterSurvey", 0), ("DefaultScoringCategory", None),
        ("AutoScoringCategory", None)])),
    element("SO", "Survey Options", None, None, SURVEY_OPTIONS),
]
for tag, q in QUESTIONS.items():
    elements.append(element("SQ", q["qid"], short(q["text"]), None, q["payload"]))
elements.append(element("STAT", "Survey Statistics", None, None, {"MobileCompatible": True, "ID": "Survey Statistics"}))

QSF = OrderedDict([
    ("SurveyEntry", OrderedDict([
        ("SurveyID", SURVEY_ID), ("SurveyName", SURVEY_NAME), ("SurveyDescription", None),
        ("SurveyOwnerID", LIB_2025), ("SurveyBrandID", "polimi"), ("DivisionID", None), ("SurveyLanguage", "IT"),
        ("SurveyActiveResponseSet", RS_ID), ("SurveyStatus", "Inactive"),
        ("SurveyStartDate", "0000-00-00 00:00:00"), ("SurveyExpirationDate", "0000-00-00 00:00:00"),
        ("SurveyCreationDate", NOW), ("CreatorID", LIB_2025), ("LastModified", NOW),
        ("LastAccessed", "0000-00-00 00:00:00"), ("LastActivated", "0000-00-00 00:00:00"), ("Deleted", None)])),
    ("SurveyElements", elements),
])

with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(QSF, fh, ensure_ascii=False, separators=(",", ":"))

print("Scritto %s: %d domande + %d testi descrittivi, %d pagine nel blocco Questionario"
      % (OUT, sum(1 for q in QUESTIONS.values() if q["kind"] != "DB"),
         sum(1 for q in QUESTIONS.values() if q["kind"] == "DB"), len(PAGES)))
