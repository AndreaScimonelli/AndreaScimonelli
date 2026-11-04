#!/usr/bin/env python3
"""
Genera il file QSF (Qualtrics Survey Format) della
"Survey di Ricerca 2026/2027 – Questionario End User – Grandi e grandissime imprese"
dell'Osservatorio Intelligent Business Process Automation (Politecnico di Milano).

Fonte: Survey_IBPA_2026-2027_EndUser_Grandi_FINALE_v4.docx

Uso:  python3 build_qsf.py [percorso_output.qsf]

Il QSF replica la struttura dei file esportati da Qualtrics (SurveyEntry +
SurveyElements: BL, FL, PROJ, QC, RS, SCO, SO, SQ..., STAT).
I filtri del documento sono implementati come:
  - branch nel Survey Flow per i filtri di sezione e gli screen-out;
  - display logic sulle singole domande / opzioni per i filtri di domanda;
  - embedded data per la logica 5.1 -> 5.2 -> 5.3.
"""
import html
import json
import random
import re
import sys
from collections import OrderedDict

OUT = sys.argv[1] if len(sys.argv) > 1 else "Survey_IBPA_2026-2027_EndUser_Grandi.qsf"

_rng = random.Random(20262027)
_ALNUM = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def rid(prefix, n=15):
    return prefix + "".join(_rng.choice(_ALNUM) for _ in range(n))


SURVEY_ID = rid("SV_")
OWNER_ID = rid("UR_")
RS_ID = rid("RS_")
NOW = "2026-11-04 17:00:00"
SURVEY_NAME = "Survey IBPA 2026-2027 – End User Grandi e grandissime imprese"


# --------------------------------------------------------------------------
# Utility testo
# --------------------------------------------------------------------------
def plain(s):
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<sup>.*?</sup>", "", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def short(s, n=100):
    p = plain(s)
    return p if len(p) <= n else p[:n].rstrip() + "..."


def H(title):
    """Intestazione di sezione mostrata al rispondente."""
    return ('<div style="font-size:1.15em;font-weight:bold;color:#1F3864;'
            'margin-bottom:14px;">%s</div>' % title)


def BOX(text):
    """Riquadro grigio per i testi introduttivi/definizioni (visibili)."""
    return ('<div style="background-color:#F2F2F2;padding:10px 12px;'
            'font-size:0.9em;line-height:1.45;">%s</div>' % text)


def Q(stem=None, instr=None, note=None, head=None, sub=None):
    """Testo domanda: [intestazione sezione] domanda (grassetto) + istruzione + nota + sottotitolo."""
    s = ""
    if head:
        s += H(head)
    if stem:
        s += "<b>%s</b>" % stem
    if instr:
        s += (("<br>" if stem else "") +
              '<span style="font-size:0.85em;color:#595959;"><i>%s</i></span>' % instr)
    if note:
        s += "<br><br>" + note
    if sub:
        s += ("<br><br>" if (stem or instr or note) else "") + (
            '<span style="color:#1F3864;"><b>%s</b></span>' % sub)
    return s


def ROW(name, detail):
    """Riga di matrice con testo fra parentesi in carattere ridotto."""
    return '%s <span style="font-size:0.85em;color:#595959;">(%s)</span>' % (name, detail)


# --------------------------------------------------------------------------
# Registro domande
# --------------------------------------------------------------------------
QUESTIONS = OrderedDict()   # tag -> info
_qcount = [0]
LET = "abcdefghijklmnopqrstuvwxyz"


def _new_qid():
    _qcount[0] += 1
    return "QID%d" % _qcount[0]


def _base_payload(tag, qid, text, qtype, selector, subselector=None):
    p = OrderedDict()
    p["QuestionText"] = text
    p["DefaultChoices"] = False
    p["DataExportTag"] = tag
    p["QuestionType"] = qtype
    p["Selector"] = selector
    if subselector is not None:
        p["SubSelector"] = subselector
    p["Configuration"] = OrderedDict([("QuestionDescriptionOption", "UseText")])
    p["QuestionDescription"] = short(text)
    return p


def _validation(force, vtype="None", **extra):
    s = OrderedDict([("ForceResponse", "ON" if force else "OFF"),
                     ("ForceResponseType", "ON"),
                     ("Type", vtype)])
    s.update(extra)
    return {"Settings": s}


def _register(tag, qid, payload, kind, **meta):
    assert tag not in QUESTIONS, tag
    payload["QuestionID"] = qid
    payload["DataVisibility"] = {"Private": False, "Hidden": False}
    QUESTIONS[tag] = dict(qid=qid, payload=payload, kind=kind, text=payload["QuestionText"], **meta)
    return QUESTIONS[tag]


def mc(tag, text, specs, multi=False, force=True, rand=None, maxc=None, minc=None,
       dl=None):
    """Domanda a scelta multipla. specs: stringhe o dict {t, te, excl, id, key, dl}."""
    qid = _new_qid()
    choices, order, keymap, labels = OrderedDict(), [], {}, {}
    for i, s in enumerate(specs):
        if isinstance(s, str):
            s = {"t": s}
        cid = str(s.get("id", i + 1))
        c = OrderedDict([("Display", s["t"])])
        if s.get("te"):
            c["TextEntry"] = "true"
            c["TextEntrySize"] = "Small"
        if s.get("excl"):
            c["ExclusiveAnswer"] = True
        if s.get("dl"):
            c["DisplayLogic"] = s["dl"]
        choices[cid] = c
        order.append(cid)
        key = s.get("key", LET[i])
        keymap[key] = cid
        labels[cid] = plain(s["t"])
    p = _base_payload(tag, qid, text, "MC", "MAVR" if multi else "SAVR", "TX")
    p["Choices"] = choices
    p["ChoiceOrder"] = order
    if rand:
        p["Randomization"] = rand(order)
    if maxc:
        mn = minc if minc is not None else (1 if force else 0)
        p["Validation"] = _validation(force, "ChoiceRange",
                                      MinChoices=str(mn), MaxChoices=str(maxc))
    else:
        p["Validation"] = _validation(force)
    p["Language"] = []
    p["NextChoiceId"] = max(int(c) for c in order) + 1
    p["NextAnswerId"] = 1
    if dl:
        p["DisplayLogic"] = dl
    return _register(tag, qid, p, "MC", multi=multi, ck=keymap, clabels=labels,
                     force=force, maxc=maxc)


def matrix(tag, text, rows, cols, multi=False, force=True, excl_cols=(), rand_rows=False,
           width=25, dl=None):
    qid = _new_qid()
    choices = OrderedDict((str(i + 1), OrderedDict([("Display", r)])) for i, r in enumerate(rows))
    answers = OrderedDict()
    for j, a in enumerate(cols):
        d = OrderedDict([("Display", a)])
        if (j + 1) in excl_cols:
            d["ExclusiveAnswer"] = True
        answers[str(j + 1)] = d
    p = _base_payload(tag, qid, text, "Matrix", "Likert",
                      "MultipleAnswer" if multi else "SingleAnswer")
    p["Configuration"].update(OrderedDict([("TextPosition", "inline"),
                                           ("ChoiceColumnWidth", width),
                                           ("RepeatHeaders", "none"),
                                           ("WhiteSpace", "OFF"),
                                           ("MobileFirst", True)]))
    p["Choices"] = choices
    p["ChoiceOrder"] = list(choices.keys())
    if rand_rows:
        p["Randomization"] = OrderedDict([("Advanced", None), ("TotalRandSubset", ""),
                                          ("Type", "All")])
    p["Validation"] = _validation(force)
    p["GradingData"] = []
    p["Language"] = []
    p["NextChoiceId"] = len(rows) + 1
    p["NextAnswerId"] = len(cols) + 1
    p["Answers"] = answers
    p["AnswerOrder"] = list(answers.keys())
    p["ChoiceDataExportTags"] = False
    if dl:
        p["DisplayLogic"] = dl
    return _register(tag, qid, p, "Matrix", multi=multi, force=force,
                     rlabels={str(i + 1): plain(r) for i, r in enumerate(rows)},
                     alabels={str(j + 1): plain(a) for j, a in enumerate(cols)},
                     excl_cols=[str(c) for c in excl_cols])


def te(tag, text, force=True, email=False, default=None):
    qid = _new_qid()
    p = _base_payload(tag, qid, text, "TE", "SL")
    if default:
        p["DefaultChoices"] = {"TEXT": {"Text": default}}
    if email:
        p["Validation"] = _validation(force, "ContentType", ContentType="ValidEmail",
                                      ValidDateType="DateWithFormat",
                                      ValidPhoneType="ValidUSPhone",
                                      ValidZipType="ValidUSZip",
                                      ValidNumber={"Min": "", "Max": "", "NumDecimals": ""})
    else:
        p["Validation"] = _validation(force)
    p["GradingData"] = []
    p["Language"] = []
    p["NextChoiceId"] = 4
    p["NextAnswerId"] = 1
    p["SearchSource"] = {"AllowFreeResponse": "false"}
    return _register(tag, qid, p, "TE", force=force, email=email)


def db(tag, text, dl=None):
    qid = _new_qid()
    p = _base_payload(tag, qid, text, "DB", "TB")
    p["ChoiceOrder"] = []
    p["Validation"] = {"Settings": {"Type": "None"}}
    p["GradingData"] = []
    p["Language"] = []
    p["NextChoiceId"] = 4
    p["NextAnswerId"] = 1
    if dl:
        p["DisplayLogic"] = dl
    return _register(tag, qid, p, "DB")


def cs(tag, text, items, total=100, force=True, inpage_dl=None):
    """Somma costante (constant sum) con vincolo 'Must total'."""
    qid = _new_qid()
    choices = OrderedDict((str(i + 1), OrderedDict([("Display", t)])) for i, t in enumerate(items))
    p = _base_payload(tag, qid, text, "CS", "VRTL")
    p["Choices"] = choices
    p["ChoiceOrder"] = list(choices.keys())
    p["Validation"] = _validation(force, "ChoicesTotal", ChoiceTotal=str(total),
                                  EnforceRange=None)
    p["GradingData"] = []
    p["Language"] = []
    p["NextChoiceId"] = len(items) + 1
    p["NextAnswerId"] = 1
    if inpage_dl:
        p["InPageDisplayLogic"] = inpage_dl
    return _register(tag, qid, p, "CS", force=force, total=total,
                     clabels={str(i + 1): plain(t) for i, t in enumerate(items)})


# --------------------------------------------------------------------------
# Condizioni logiche (display logic / branch logic)
# --------------------------------------------------------------------------
OPDESC = {"Selected": "Is Selected", "NotSelected": "Is Not Selected",
          "EqualTo": "Is Equal to", "NotEqualTo": "Is Not Equal to"}


def c_sel(tag, key, op="Selected"):
    """Opzione `key` (lettera del documento) della domanda MC `tag`."""
    q = QUESTIONS[tag]
    cid = q["ck"][key]
    loc = "q://%s/SelectableChoice/%s" % (q["qid"], cid)
    return dict(_kind="q", _qdesc=short(q["text"]), _cdesc=q["clabels"][cid],
                LogicType="Question", QuestionID=q["qid"], QuestionIsInLoop="no",
                ChoiceLocator=loc, Operator=op, QuestionIDFromLocator=q["qid"],
                LeftOperand=loc, Type="Expression")


def c_cell(tag, row, col, op="Selected"):
    """Cella (riga, colonna) della matrice `tag` (numerazione 1..n come nel documento)."""
    q = QUESTIONS[tag]
    r, a = str(row), str(col)
    assert r in q["rlabels"] and a in q["alabels"], (tag, row, col)
    loc = "q://%s/SelectableChoice/%s/%s" % (q["qid"], r, a)
    return dict(_kind="q", _qdesc=short(q["text"]),
                _cdesc="%s - %s" % (short(q["rlabels"][r], 60), q["alabels"][a]),
                LogicType="Question", QuestionID=q["qid"], QuestionIsInLoop="no",
                ChoiceLocator=loc, Operator=op, QuestionIDFromLocator=q["qid"],
                LeftOperand=loc, Type="Expression")


def c_ed(field, op, value):
    """Condizione su embedded data."""
    return dict(_kind="ed", LogicType="EmbeddedField", LeftOperand=field, Operator=op,
                RightOperand=value, _HiddenExpression=False, Type="Expression")


def _finalize(cond, word):
    c = OrderedDict((k, v) for k, v in cond.items() if not k.startswith("_") or k == "_HiddenExpression")
    if cond["_kind"] == "q":
        c["Description"] = ('<span class="ConjDesc">%s</span> <span class="QuestionDesc">%s</span> '
                            '<span class="LeftOpDesc">%s</span> <span class="OpDesc">%s</span> '
                            % (word, cond["_qdesc"], cond["_cdesc"], OPDESC[cond["Operator"]]))
    else:
        c["Description"] = ('<span class="ConjDesc">%s</span>  <span class="LeftOpDesc">%s</span> '
                            '<span class="OpDesc">%s</span> <span class="RightOpDesc"> %s </span>'
                            % (word, cond["LeftOperand"], OPDESC[cond["Operator"]],
                               cond["RightOperand"]))
    return c


def logic(conds, conj="Or", inpage=False, branch=False):
    """Insieme di condizioni unite da un solo connettivo (tutte Or oppure tutte And)."""
    assert conj in ("Or", "And")
    grp = OrderedDict()
    for i, cond in enumerate(conds):
        c = _finalize(cond, "If" if i == 0 else conj)
        if i > 0:
            c["Conjuction"] = conj   # sic: grafia usata da Qualtrics
        grp[str(i)] = c
    grp["Type"] = "If"
    out = OrderedDict([("0", grp), ("Type", "BooleanExpression")])
    if not branch:
        out["inPage"] = inpage
    return out


def blogic(conds, conj="Or"):
    return logic(conds, conj, branch=True)


def adv_rand_fixed_last(order, n_fixed_last=1):
    """Randomizza tutte le opzioni tranne le ultime n (che restano in fondo)."""
    rnd, fixed = order[:-n_fixed_last], order[-n_fixed_last:]
    return OrderedDict([
        ("Type", "Advanced"),
        ("Advanced", OrderedDict([("FixedOrder", ["{~SubSet~}"] * len(rnd) + fixed),
                                  ("RandomizeAll", []), ("RandomSubSet", rnd),
                                  ("ScaleReversal", []), ("Undisplayed", []),
                                  ("TotalRandSubset", len(rnd))])),
        ("ConsistentScaleReversal", False), ("EvenPresentation", False),
        ("TotalRandSubset", "")])


# ==========================================================================
# CONTENUTI DEL QUESTIONARIO
# ==========================================================================
ALTRO = {"t": "Altro (specificare):", "te": True}

# ---------------- Sezione 1. Anagrafica ----------------
db("INTRO",
   '<div style="text-align:center;">'
   '<span style="color:#595959;">Osservatorio Intelligent Business Process Automation – Politecnico di Milano</span><br>'
   '<span style="font-size:1.4em;font-weight:bold;color:#1F3864;">Survey di Ricerca 2026/2027</span>'
   '</div>')
te("Q1.1", Q("Nome:", head="Anagrafica"), default="${m://FirstName}")
te("Q1.2", Q("Cognome:"), default="${m://LastName}")
te("Q1.3", Q("E-mail aziendale:"), email=True, default="${m://Email1}")
te("Q1.4", Q("Ragione sociale dell’azienda:"))
te("Q1.5", Q("Job title:"))
mc("Q1.6", Q("Settore di attività (selezionare quello prevalente)"), [
    "Aerospace & Defence", "Automotive", "Banking and Finance", "Chemical", "Construction",
    "Education", "Energy, Resources & Utility", "Food & Beverage", "Healthcare & Assistance",
    "Hospitality", "ICT & Electronics", "Insurance", "Logistics, Transportation",
    "Manufacturing", "Media and Entertainment", "Pharma", "Public Administration",
    "GDO & Retail", "Services", "Telco", "Tourism", ALTRO])
mc("Q1.7", Q("Dimensione aziendale (numero di dipendenti)"), [
    "Fino a 49 dipendenti", "Da 50 a 249 dipendenti", "Da 250 a 999 dipendenti",
    "Oltre 1.000 dipendenti"])

# ---------------- Sezione 2. Maturità digitale e gestione per processi ----------------
mc("Q2.1", Q("Quale affermazione rispecchia meglio l’orientamento al digitale della sua azienda?",
             "(Risposta singola)", head="Maturità digitale e gestione per processi"), [
    "Investiamo in modo significativo nel digitale, con progetti trasversali su tutte le aree aziendali.",
    "Investiamo in modo significativo nel digitale, ma solo in alcune aree aziendali specifiche.",
    "Investiamo poco nel digitale perché i benefici attesi non sono ancora pienamente chiari alla nostra organizzazione.",
    "Investiamo poco nel digitale perché nel nostro settore il digitale è considerato poco rilevante.",
    "Investiamo poco o nulla nel digitale principalmente per via dei costi (tempi, competenze, risorse) giudicati troppo elevati rispetto ai benefici.",
    ALTRO])
mc("Q2.2", Q("Come descriverebbe il livello di digitalizzazione documentale e di interconnessione dei processi nella sua azienda?",
             "(Risposta singola)"), [
    "I principali processi aziendali utilizzano ancora documenti cartacei o non digitalizzati.",
    "L’azienda ha iniziato a digitalizzare i documenti, ma molte aree rimangono isolate (i sistemi non dialogano tra loro).",
    "La maggior parte dei processi è digitalizzata, ma i sistemi non sono completamente integrati (esistono ancora barriere o silos informativi).",
    "I processi principali sono completamente digitalizzati e integrati su piattaforme che consentono lo scambio di dati tra sistemi diversi.",
    "I sistemi sono integrati, automatizzati e monitorati in tempo reale tramite infrastruttura cloud, con strumenti che aiutano a prevenire disallineamenti tra i dati dei diversi processi."])
matrix("Q2.3", Q("Quali dei seguenti elementi di gestione per processi sono presenti nella sua azienda?",
                 "(Una risposta per riga)"), [
    "Un inventario o mappa dei processi aziendali (process landscape)",
    "Process owner formalmente identificati, con responsabilità definite",
    "Process owner con autorità formale sul ridisegno del processo e sulle sue priorità",
    "KPI di processo con target definiti e monitorati nel tempo",
    "Modellazione dei processi con notazioni standard (es. BPMN, swimlane, SIPOC)<sup>1</sup>",
    "Un repository centrale di processi, procedure e linee guida operative"],
    ["Sì, presente e mantenuto aggiornato", "Sì, ma non aggiornato regolarmente",
     "In corso di definizione", "No"], width=40)
db("Q2.3_NOTA",
   '<span style="font-size:0.8em;color:#595959;"><sup>1</sup> BPMN (Business Process Model and Notation): '
   'standard internazionale per rappresentare graficamente i processi con una simbologia condivisa, che rende '
   'la mappa leggibile allo stesso modo da funzioni e fornitori diversi. Swimlane: diagramma a corsie, in cui '
   'ogni corsia raccoglie le attività di un ruolo o di una funzione, così da rendere visibili i passaggi di '
   'responsabilità lungo il processo. SIPOC (Supplier, Input, Process, Output, Customer): schema sintetico che '
   'descrive un processo elencandone fornitori, input, fasi principali, output e destinatari, usato per '
   'delimitarne il perimetro prima di analizzarlo.</span>')
# Filtro 2.4: mostrata a chi, alla prima riga della 2.3, non ha risposto «No»
mc("Q2.4", Q("Che quota dei processi aziendali stima sia oggi formalmente mappata?", "(Risposta singola)"), [
    "Meno del 25%", "Tra il 25% e il 50%", "Tra il 51% e il 75%", "Oltre il 75%", "Non so"],
    dl=logic([c_cell("Q2.3", 1, 4, "NotSelected")]))

# ---------------- Sezione 3. Approccio alla Process Automation ----------------
db("S3_DEF", H("Approccio alla Process Automation") + BOX(
    "Per Process Automation si intende l’insieme di tecnologie, strumenti e metodologie che consentono di "
    "automatizzare attività e processi aziendali per aumentare efficienza, precisione e velocità, riducendo "
    "l’intervento manuale. Rientrano in questa definizione sia l’automazione tradizionale di attività ripetitive "
    "e regolari (workflow automatici, API, Robotic Process Automation), sia l’automazione intelligente, che "
    "integra machine learning e analisi dei dati e permette di automatizzare attività non rigidamente "
    "strutturate, sia le soluzioni agentiche, in cui sistemi basati su AI pianificano ed eseguono autonomamente "
    "sequenze di azioni per raggiungere un obiettivo. Salvo diversa indicazione, non si faccia riferimento ai "
    "processi fisici (produzione, manutenzione, movimentazione)."))
mc("Q3.1", Q("Quale affermazione rispecchia meglio l’attuale approccio alla Process Automation nella sua azienda?",
             "(Risposta singola)"), [
    "L’automazione è applicata a specifici dipartimenti o processi, senza una strategia aziendale centralizzata (es. automazione limitata a HR o gestione ordini).",
    "L’automazione è adottata in diversi dipartimenti o processi, ma non è ancora trasversale o parte di una strategia aziendale complessiva (es. automazione in finanza e HR, ma non in supply chain o customer service).",
    "L’automazione è integrata trasversalmente nella strategia aziendale, coinvolgendo più dipartimenti e processi.",
    "Non applichiamo la Process Automation.",
    {"t": "Altro (specificare il tipo di approccio adottato):", "te": True}])
matrix("Q3.2", Q("Come descriverebbe l’atteggiamento prevalente verso l’automazione ai diversi livelli organizzativi?",
                 "(Una risposta per riga)"),
       ["Top management", "Middle management", "Ruoli operativi"],
       ["Preoccupazione per la sostituzione o la perdita di controllo",
        "Scarsa consapevolezza dei benefici, senza resistenza esplicita",
        "Consapevolezza crescente e interesse a sperimentare",
        "Automazione e AI viste come leva per il valore del lavoro"], width=22)
NOT_PA = lambda: logic([c_sel("Q3.1", "d", "NotSelected")])   # non mostrata a chi ha risposto d) alla 3.1
mc("Q3.3", Q("In quale fase del percorso di automazione collocherebbe attualmente la sua azienda?",
             "(Risposta singola. Si consideri come unità di conteggio il singolo flusso automatizzato, "
             "indipendentemente dalla sua ampiezza)"), [
    "Sperimentazione iniziale (progetti pilota, indicativamente meno di 10 processi automatizzati).",
    "Implementazione (indicativamente tra 10 e 50 processi automatizzati, estesi a processi trasversali).",
    "Scalabilità aziendale (indicativamente oltre 50 processi automatizzati, integrati in più dipartimenti).",
    "Automazione sospesa o progetti “abbandonati”"], dl=NOT_PA())
mc("Q3.4A", Q("Con riferimento alla modalità prevalente con cui viene introdotta la Process Automation, indichi "
              "la situazione più vicina alla sua azienda per ciascuno dei due aspetti seguenti.",
              "(Una risposta per ciascun aspetto)", sub="A — Ampiezza dell’unità automatizzata"), [
    "Prevalentemente singoli task all’interno di una funzione.",
    "Processi completi, ma contenuti all’interno di una singola funzione.",
    "Processi end-to-end che attraversano più funzioni (es. order-to-cash, purchase-to-pay, hire-to-retire).",
    "Non siamo in grado di rispondere."], dl=NOT_PA())
mc("Q3.4B", Q(sub="B — Ruolo dell’analisi di processo"), [
    "I processi sono già mappati e ottimizzati in azienda, solo quando si vuole introdurre un’automazione, si analizza il processo ed eventualmente lo si ridisegna;",
    "Processo e automazione vengono progettati insieme, in un unico percorso, senza una fase di ridisegno preliminare.",
    "L’analisi approfondita del processo viene svolta soltanto in una minoranza di occasioni, per i progetti più complessi.",
    "L’automazione viene introdotta senza una preventiva analisi o revisione del processo."], dl=NOT_PA())

# ---------------- Sezione 4. Tecnologie di automazione ----------------
mc("Q4.1", Q("Quali di questi strumenti sono presenti nella sua realtà?",
             "(Risposta multipla – selezionare tutte le opzioni applicabili)", head="Tecnologie di automazione"), [
    "Soluzioni di Robotic Process Automation – esempi: UiPath, Blue Prism, Automation Anywhere",
    "Soluzioni di API automation e integrazione tra sistemi – esempi: Boomi, MuleSoft, Workato",
    "Strumenti di Business Process Management – esempi: Camunda, Appian, Pega",
    "Strumenti di Workflow Automation o piattaforme low-code – esempi: n8n, Nintex, Power Automate, Zapier",
    "Strumenti di Process Mining o Process Intelligence – esempi: Celonis, Apromore",
    "Strumenti di Intelligent Document Processing – esempi: ABBYY, Rossum, moduli IDP delle piattaforme di automazione",
    "Piattaforme di sviluppo o orchestrazione di agenti AI – esempi: Microsoft Copilot Studio, Google Vertex AI Agent Builder, LangGraph, CrewAI, moduli agentici delle piattaforme RPA",
    {"t": "Nessuno di questi", "excl": True}], multi=True, rand=adv_rand_fixed_last)

# ---------------- Sezione 5. Mappatura dei processi automatizzati ----------------
db("S5_INTRO", H("Mappatura dei processi automatizzati") + BOX(
    "In questa sezione le chiediamo di indicare dove l’automazione è effettivamente applicata, utilizzando una "
    "classificazione per famiglie di processo anziché per aree organizzative. Le famiglie elencate sono "
    "indipendenti dalla struttura organizzativa della sua azienda: le consideri come raggruppamenti di attività, "
    "a prescindere da quale funzione le presidia.<br><br>"
    "<b>Automazione tradizionale</b>: tecnologie che automatizzano attività ripetitive e basate su regole "
    "predeterminate (workflow, RPA, integrazioni via API).<br>"
    "<b>Automazione intelligente</b>: soluzioni che integrano AI, machine learning e analisi dei dati, "
    "estendendo l’automazione ad attività non rigidamente strutturate.<br>"
    "<b>Agenti AI autonomi</b>: sistemi che pianificano ed eseguono autonomamente sequenze di azioni per "
    "raggiungere un obiettivo definito, attivando altri sistemi aziendali."))
FAMIGLIE = [
    ROW("Strategia, governance e organizzazione", "pianificazione strategica, performance management, policy e deleghe, struttura organizzativa"),
    ROW("Risorse umane e sviluppo delle persone", "selezione e onboarding, formazione, valutazione della performance, welfare, workforce planning"),
    ROW("Ricerca, sviluppo e innovazione dell’offerta", "scouting tecnologico, ideazione, sviluppo prodotto, prototipazione, test, lancio, proprietà intellettuale"),
    ROW("Marketing, vendite e canali commerciali", "analisi di mercato, brand, campagne, advertising, contenuti, gestione lead, offerte e preventivi, digital commerce"),
    ROW("Acquisti e gestione dei fornitori", "strategie di sourcing, scouting e qualifica, contrattualizzazione, procurement operativo, vendor rating"),
    ROW("Operations, produzione, logistica e fulfillment", "pianificazione della domanda e degli approvvigionamenti, esecuzione, magazzino, evasione ordini, trasporti, qualità, resi"),
    ROW("Customer service e gestione della relazione con il cliente", "assistenza, dati cliente, reclami, post-vendita, esperienza e fidelizzazione, misurazione della soddisfazione"),
    ROW("Amministrazione, finanza e controllo", "contabilità e fatturazione, chiusure e bilancio, budgeting e controllo di gestione, tesoreria e pagamenti"),
    ROW("Legal, contrattualistica e gestione degli asset", "consulenza legale, ciclo di vita dei contratti, asset e facility management"),
    ROW("IT, dati e cybersecurity", "strategia e architetture IT, sviluppo e integrazione software, esercizio dei sistemi, gestione dei dati, sicurezza, identità digitali"),
    ROW("Risk management, compliance e sostenibilità", "gestione dei rischi, conformità normativa, audit interno, continuità operativa, ESG, relazioni istituzionali"),
]
matrix("Q5.1", Q("Per ciascuna famiglia di processo, indichi quali tipologie di automazione sono oggi in uso nella sua azienda.",
                 "(Risposta multipla per riga sulle prime tre colonne; le ultime due colonne sono esclusive)"),
       FAMIGLIE,
       ["Automazione tradizionale", "Automazione intelligente (AI)", "Agenti AI autonomi",
        "Nessuna automazione", "Non applicabile"],
       multi=True, excl_cols=(4, 5), rand_rows=True, width=40)

# Famiglie approfondibili (5.2/5.3) -> riga corrispondente nella 5.1
FAM_52 = [  # (codice embedded data, lettera 5.2, riga 5.1, etichetta, pattern "solo questa")
    ("AFC", "a", 8, "Amministrazione, finanza e controllo", "P1000"),
    ("ACQ", "b", 5, "Acquisti e gestione dei fornitori", "P0100"),
    ("OPS", "c", 6, "Operations, produzione, logistica e fulfillment", "P0010"),
    ("CS", "d", 7, "Customer service e gestione della relazione con il cliente", "P0001"),
]
mc("Q5.2", Q("Tra le famiglie seguenti, selezioni al massimo due su cui desidera fornire un maggiore livello di dettaglio.",
             "(Risposta multipla, massimo 2) – Facoltativo"),
   [{"t": lab, "dl": logic([c_ed("elig_" + code, "EqualTo", "1")])} for code, _, _, lab, _ in FAM_52],
   multi=True, force=False, maxc=2, minc=0,
   # mostrata solo se almeno 2 famiglie sono selezionabili (pattern diverso da 0 o 1 famiglia)
   dl=logic([c_ed("elig_pattern", "NotEqualTo", p) for p in ("P0000", "P1000", "P0100", "P0010", "P0001")], "And"))

S53 = "Per le famiglie selezionate, indichi lo stato di automazione dei singoli processi."
I53 = "(Una risposta per riga) – Facoltativo"
COLS_53 = ["Automatizzato – automazione tradizionale",
           "Automatizzato – automazione intelligente o agentic",
           "Non automatizzato, prioritario nei prossimi 12 mesi",
           "Non automatizzato / non rilevante"]
ROWS_53 = {
    "AFC": ["Registrazione contabile e gestione del ciclo di fatturazione attiva e passiva, inclusa la fatturazione elettronica",
            "Controlli di coerenza tra fattura, ordine e contratto e gestione degli scostamenti",
            "Chiusure contabili periodiche e predisposizione del bilancio",
            "Budgeting, forecast e analisi degli scostamenti rispetto al consuntivo",
            "Gestione degli incassi, solleciti e riconciliazioni bancarie",
            "Adempimenti fiscali e conservazione digitale a norma"],
    "ACQ": ["Analisi della spesa per categoria e supply market intelligence",
            "Scouting, qualifica e onboarding dei fornitori (RFI, RFQ, RFP)",
            "Negoziazione e gestione del ciclo di vita dei contratti di fornitura",
            "Procurement operativo: richieste d’acquisto, emissione ordini, ricezione e ciclo procure-to-pay",
            "Vendor rating e monitoraggio delle performance dei fornitori",
            "Qualifica ESG dei fornitori e monitoraggio della compliance di filiera"],
    "OPS": ["Previsione della domanda e Sales & Operations Planning",
            "Pianificazione degli approvvigionamenti e ottimizzazione delle scorte",
            "Schedulazione e controllo dell’esecuzione produttiva o dell’erogazione del servizio",
            "Gestione del magazzino e delle movimentazioni (inventari, picking, packing)",
            "Gestione degli ordini cliente ed evasione (order fulfillment)",
            "Pianificazione dei trasporti, tracciamento e notifiche di consegna",
            "Controllo qualità e gestione dei resi (reverse logistics)"],
    "CS": ["Gestione delle anagrafiche cliente, single customer view e qualità del dato CRM",
           "Ricezione e smistamento delle richieste (ticketing, classificazione, routing)",
           "Risoluzione delle richieste e gestione delle escalation",
           "Gestione dei reclami e analisi delle cause",
           "Servizi post-vendita e pianificazione degli interventi tecnici",
           "Raccolta dei feedback e misurazione della soddisfazione (NPS, CSAT, CES)",
           "Programmi di loyalty, retention e personalizzazione"],
}
for (code, key, _, lab, solo), suffix in zip(FAM_52, "abcd"):
    # mostrata se la famiglia è stata scelta alla 5.2 oppure se era l'unica selezionabile (5.2 saltata)
    matrix("Q5.3" + suffix, Q(S53, I53, sub=lab), ROWS_53[code], COLS_53, force=False, width=40,
           dl=logic([c_sel("Q5.2", key), c_ed("elig_pattern", "EqualTo", solo)], "Or"))

# ---------------- Sezione 6. Agentic Automation ----------------
mc("Q6.1", Q("In relazione all’Agentic AI, dove posizionerebbe la sua realtà aziendale?",
             "(Risposta singola – indichi la situazione più vicina alla vostra realtà)", head="Agentic Automation"), [
    "Non ho mai sentito il termine.",
    "Conosco personalmente il tema, ma non è mai stato discusso in azienda.",
    "Abbiamo discusso del tema in azienda, ma non abbiamo ancora avviato valutazioni o sperimentazioni.",
    "Stiamo analizzando le potenzialità o conducendo studi interni sul tema.",
    "Abbiamo avviato sperimentazioni su ambiti o processi selezionati.",
    "Stiamo estendendo l’utilizzo di agenti autonomi in alcuni processi aziendali.",
    "L’Agentic AI è parte integrante della strategia di automazione o dei sistemi operativi interni."])
mc("Q6.2", Q("Quali capacità hanno le soluzioni di Agentic AI presenti in azienda o in fase di valutazione?",
             "(Risposta multipla – selezionare tutte le opzioni applicabili)"), [
    "Autonomia operativa – la soluzione esegue attività o processi senza intervento umano costante.",
    "Collaborazione e adattamento multi-agente – più agenti cooperano e si coordinano per obiettivi comuni.",
    "Uso di strumenti – l’agente attiva autonomamente altri sistemi o applicazioni aziendali (CRM, ERP, ticketing).",
    "Accesso a memoria e apprendimento continuo – la soluzione conserva informazioni e migliora le proprie azioni nel tempo.",
    "Orientamento agli obiettivi – l’agente pianifica e sceglie autonomamente le azioni necessarie.",
    "Interazione conversazionale – l’agente risponde a domande degli utenti o fornisce informazioni.",
    "Esecuzione di flussi di lavoro predefiniti – la soluzione segue script o regole fisse senza adattarsi al contesto.",
    "Generazione di contenuti – l’agente produce testi, immagini o report su richiesta.",
    "Supporto all’utente tramite suggerimenti o raccomandazioni, senza agire autonomamente.",
    ALTRO,
    {"t": "Non ho abbastanza informazioni per rispondere.", "excl": True}], multi=True,
    dl=logic([c_sel("Q6.1", k, "NotSelected") for k in "abc"], "And"))

# ---------------- Sezione 7. Organizzazione e competenze ----------------
mc("Q7.1", Q("Esiste in azienda una funzione o un ruolo che presidia la gestione dei processi (BPM, Process Excellence, Organizzazione)?",
             "(Risposta singola)", head="Organizzazione e competenze"), [
    "Sì, una funzione dedicata, con risorse proprie e un mandato formalizzato",
    "Sì, un presidio part-time collocato all’interno di un’altra funzione (es. Organizzazione, IT, Operations)",
    "No, ma i process owner operano in autonomia nelle rispettive aree",
    "No, non esiste un presidio strutturato sulla gestione dei processi"])
mc("Q7.2", Q("Come sono organizzati i presidi sull’automazione dei processi e sull’intelligenza artificiale?",
             "(Risposta singola)"), [
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
             "(Risposta multipla – selezionare tutte le opzioni applicabili)"), [
    "Un budget unico per i due presidi",
    "Una pipeline o un backlog unico dei casi d’uso",
    "Criteri di prioritizzazione comuni",
    "Piattaforme tecnologiche comuni",
    "Metriche e KPI comuni",
    "Un unico sponsor o referente a livello di direzione",
    "Processi comuni di risk management e compliance",
    {"t": "Nessuno di questi elementi è condiviso", "excl": True}], multi=True,
    dl=logic([c_sel("Q7.2", k) for k in "bcd"], "Or"))
mc("Q7.4", Q("Chi detiene il budget per le iniziative di automazione?", "(Risposta singola)"), [
    "Il presidio dell’automazione, con un budget dedicato e autonomo",
    "Il presidio dell’automazione, ma all’interno di un budget più ampio (IT, trasformazione, innovazione)",
    "Comitato esecutivo o Consiglio di amministrazione",
    "Amministratore delegato o Direzione generale",
    "Direzione Sistemi Informativi (CIO/CTO)",
    "Direzione Operations",
    "Direzione Amministrazione, Finanza e Controllo",
    "Le singole funzioni di business, con budget autonomi",
    "Non esiste un budget dedicato all’automazione: le iniziative sono finanziate di volta in volta",
    ALTRO], dl=logic([c_sel("Q7.3", "a", "NotSelected")]))
mc("Q7.5", Q("Quali sono le principali motivazioni per cui la sua azienda non dispone di figure dedicate all’automazione?",
             "(Risposta multipla – selezionare i due fattori principali)"), [
    "Competenze interne limitate sui temi di automazione",
    "Difficoltà a reperire sul mercato le figure necessarie",
    "Priorità aziendali concentrate su altri ambiti strategici",
    "Costi considerati troppo elevati per creare o mantenere un team interno",
    "Scarsa consapevolezza o visione strategica sul valore dell’automazione",
    "Cultura aziendale ancora poco orientata all’innovazione o alla sperimentazione",
    "Preferenza per il supporto di consulenti o fornitori esterni",
    ALTRO], multi=True, maxc=2,
    dl=logic([c_sel("Q7.2", k) for k in "fghi"], "Or"))
mc("Q7.6", Q("Nei prossimi 12 mesi è previsto un impatto sull’organico delle aree interessate dall’automazione?",
             "(Risposta singola)"), [
    "Riduzione significativa dell’organico",
    "Riduzione contenuta, gestita prevalentemente attraverso il turnover naturale",
    "Organico invariato, con ricollocazione delle persone su attività diverse",
    "Organico invariato, senza modifiche sostanziali alle mansioni",
    "Crescita dell’organico, per l’ingresso di nuove competenze",
    "Non siamo in grado di formulare una previsione"])

# ---------------- Sezione 8. Esternalizzazione ----------------
mc("Q8.1", Q("In che modo l’automazione e l’intelligenza artificiale stanno modificando il ricorso a servizi o attività esternalizzate nella sua azienda?",
             "(Risposta multipla – selezionare tutte le opzioni applicabili)",
             note=BOX("Tra le attività potenzialmente esternalizzate rientrano, ad esempio: contabilità e gestione "
                      "finanziaria, payroll, customer service, data entry, gestione documentale, reportistica e "
                      "analisi dati, supporto IT di primo livello, gestione ordini o approvazioni cicliche, "
                      "amministrazione del personale, risposte a richieste standard di clienti o fornitori."),
             head="Esternalizzazione"), [
    "Abbiamo riportato completamente all’interno alcune attività prima gestite interamente da fornitori esterni, grazie alla possibilità di automatizzarle.",
    "Abbiamo parzialmente ridotto il ricorso a fornitori esterni, automatizzando internamente alcune attività prima affidate all’esterno.",
    "Vorremmo automatizzare processi oggi gestiti da fornitori esterni entro 12 mesi.",
    "Stiamo valutando di automatizzare processi oggi gestiti da fornitori esterni, senza obiettivi temporali definiti.",
    "Abbiamo aumentato il ricorso a fornitori esterni",
    {"t": "Al momento non sono avvenuti cambiamenti significativi nel livello di esternalizzazione.", "excl": True},
    ALTRO], multi=True)
mc("Q8.2", Q("Quali di questi servizi precedentemente esternalizzati sono stati maggiormente impattati?",
             "(Risposta multipla – massimo 3 opzioni)"), [
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
    ALTRO], multi=True, maxc=3,
    dl=logic([c_sel("Q8.1", "a"), c_sel("Q8.1", "b")], "Or"))

# ---------------- Sezione 9. Aspettative e risultati ----------------
db("S9_INTRO", H("Aspettative e risultati") + BOX(
    "Le domande seguenti non chiedono quanto bene abbiano funzionato le iniziative, ma quanto si siano "
    "discostate da ciò che l’azienda si attendeva prima di avviarle. Risponda sulla base delle iniziative "
    "effettivamente avviate, non di quelle soltanto valutate."))
matrix("Q9.1", Q("Rispetto alle aspettative iniziali, come si sono rivelate le seguenti dimensioni nelle iniziative "
                 "di automazione intelligente o agentica avviate negli ultimi 24 mesi?", "(Una risposta per riga)"), [
    "Qualità e completezza dei dati disponibili",
    "Affidabilità e prevedibilità degli output prodotti dall’AI",
    "Sforzo di progettazione e messa a punto delle soluzioni (prompt, flussi, guardrail)",
    "Facilità di integrazione con i sistemi aziendali esistenti",
    "Tempo necessario per portare la soluzione a regime",
    "Adozione da parte degli utenti",
    "Beneficio economico effettivamente ottenuto"],
    ["Meglio del previsto", "In linea con le aspettative", "Peggio del previsto",
     "Molto peggio del previsto", "Non applicabile"], width=35)
mc("Q9.2", Q("Quale affermazione descrive meglio la vostra esperienza rispetto agli scostamenti rilevati?",
             "(Risposta singola)"), [
    "I problemi emersi erano criticità preesistenti che l’automazione ha reso visibili (qualità dei dati, processi non standardizzati, responsabilità non definite)",
    "I problemi erano specifici della tecnologia e non prevedibili in fase di valutazione",
    "Le aspettative iniziali erano state fissate senza un’analisi sufficiente",
    "Le aspettative erano corrette, ma i tempi di realizzazione si sono allungati",
    "Non sapremmo attribuire lo scostamento"],
    dl=logic([c_cell("Q9.1", r, c) for r in range(1, 8) for c in (3, 4)], "Or"))

# ---------------- Sezione 10. Barriere, investimenti e prossimi passi ----------------
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
    "Affidabilità e prevedibilità degli output prodotti dall’AI",                 # riga 15: non per tradizionale
    "Assenza di responsabilità chiare sugli output e sulle azioni dei sistemi automatici",  # riga 16: idem
    "Nessuna barriera rilevante",                                                  # riga 17: esclusiva
]


def barriere(skip=()):
    out = []
    for i, t in enumerate(BARRIERE, start=1):
        if i in skip:
            continue
        out.append({"t": t, "id": i, "key": str(i), "excl": i == 17})
    return out


S101 = "Quali sono le principali barriere che la sua azienda percepisce oggi nell’introduzione di soluzioni di automazione?"
I101 = "(Selezionare al massimo 3 barriere per ciascuna tipologia di automazione)"
mc("Q10.1a", Q(S101, I101, head="Barriere, investimenti e prossimi passi", sub="Automazione tradizionale"),
   barriere(skip=(15, 16)), multi=True, maxc=3)
mc("Q10.1b", Q(S101, I101, sub="Automazione intelligente"), barriere(), multi=True, maxc=3)
mc("Q10.1c", Q(S101, I101, sub="Soluzioni agentiche"), barriere(), multi=True, maxc=3)
mc("Q10.2", Q("In quale fascia di spesa rientra, per il 2026, la spesa della sua azienda in software e servizi legati all’automazione dei processi?",
              "(Risposta singola. Si considerino, ad esempio: licenze software per workflow automation, RPA, "
              "process mining, piattaforme AI e agentiche; progetti avviati con partner tecnologici o consulenti "
              "esterni sul tema)"), [
    "Nessuna spesa", "Inferiore a 10.000 euro", "Tra 10.000 e 25.000 euro", "Tra 25.001 e 50.000 euro",
    "Tra 50.001 e 100.000 euro", "Tra 100.001 e 250.000 euro", "Tra 250.001 e 500.000 euro",
    "Tra 500.001 e 1 milione di euro", "Oltre 1 milione di euro", "Non so / dato non disponibile"])

S103 = "Qual è la dinamica della spesa rispetto al 2025 e la previsione per il 2027?"
mc("Q10.3a", Q(S103, "(Una risposta per ciascuna voce)", sub="Variazione rispetto al 2025"), [
    "Più che raddoppiata", "Raddoppiata", "In crescita tra il 50% e il 100%", "In crescita tra il 20% e il 50%",
    "In crescita tra il 10% e il 20%", "In crescita di meno del 10%", "Stabile", "In diminuzione", "Non so"])
mc("Q10.3b", Q(sub="Previsione sul 2027"), [
    "Più che raddoppierà", "Raddoppierà", "In crescita tra il 50% e il 100%", "In crescita tra il 20% e il 50%",
    "In crescita tra il 10% e il 20%", "In crescita di meno del 10%", "Stabile", "In diminuzione", "Non so"])
mc("Q10.4_ns", Q("Come si ripartisce approssimativamente la spesa 2026 tra le diverse tipologie di automazione?"),
   ["Non siamo in grado di stimare la ripartizione"], multi=True, force=False)
cs("Q10.4", Q(instr="(Indicare una percentuale approssimativa; il totale deve essere pari a 100%)"), [
    "Automazione tradizionale (RPA, workflow, integrazioni via API)",
    "Automazione intelligente non agentica (AI applicata ai processi, IDP, modelli predittivi, elaborazione del linguaggio)",
    "Soluzioni agentiche (agenti autonomi, orchestrazione multi-agente)"],
   total=100, force=True,
   # in-page: il campo percentuali scompare se si spunta "Non siamo in grado di stimare la ripartizione"
   inpage_dl=logic([c_sel("Q10.4_ns", "a", "NotSelected")], inpage=True))

mc("Q10.5", Q("La sua azienda è in grado di quantificare il beneficio economico delle iniziative di automazione?",
              "(Risposta singola)"), [
    "Sì, con una metodologia strutturata, applicata sistematicamente e validata dal controllo di gestione",
    "Sì, con una metodologia strutturata applicata dal team di automazione, non validata dal controllo di gestione",
    "Solo per alcuni progetti, con stime ad hoc",
    "No, ma stiamo introducendo una misurazione strutturata",
    "No, e al momento non è una priorità"])
S106 = "Qual è l’ordine di grandezza del beneficio economico annuo attribuito all’automazione dei processi per il 2026?"
I106 = "(Compili almeno una delle due righe, nell’unità di misura che utilizzate internamente)"
DL106 = lambda: logic([c_sel("Q10.5", k) for k in "abc"], "Or")
mc("Q10.6a", Q(S106, I106, sub="Beneficio economico annuo, espresso in euro"), [
    "Nessun beneficio netto", "Inferiore a 10.000 euro", "Tra 10.000 e 25.000", "Tra 25.001 e 50.000",
    "Tra 50.001 e 100.000", "Tra 100.001 e 250.000", "Tra 250.001 e 500.000", "Tra 500.001 e 1 milione",
    "Tra 1 e 2,5 milioni", "Tra 2,5 e 5 milioni", "Oltre 5 milioni",
    {"t": "Non applicabile", "key": "na"}], dl=DL106())
mc("Q10.6b", Q(S106, I106, sub="Beneficio annuo, espresso in FTE equivalenti liberati"), [
    "Meno di 1", "Tra 1 e 3", "Tra 4 e 10", "Tra 11 e 25", "Tra 26 e 50", "Tra 51 e 100", "Oltre 100",
    # "Compili almeno una delle due righe": se la riga in euro è "Non applicabile", qui l'opzione non compare
    {"t": "Non applicabile", "key": "na", "dl": logic([c_sel("Q10.6a", "na", "NotSelected")])}],
    dl=DL106())
mc("Q10.7", Q("Quali sono i prossimi passi che la sua azienda intende compiere in ambito automazione nei prossimi 12 mesi?",
              "(Risposta multipla – selezionare al massimo tre priorità già identificate come rilevanti o su cui si sta già lavorando)"), [
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

# ==========================================================================
# BLOCCHI
# ==========================================================================
BLOCKS = []
PB = "PB"


def block(desc, items, default=False):
    els = []
    for it in items:
        if it == PB:
            els.append({"Type": "Page Break"})
        else:
            els.append({"Type": "Question", "QuestionID": QUESTIONS[it]["qid"]})
    b = OrderedDict([("Type", "Default" if default else "Standard")])
    if not default:
        b["SubType"] = ""
    b["Description"] = desc
    b["ID"] = rid("BL_")
    b["BlockElements"] = els
    b["Options"] = OrderedDict([("BlockLocking", "false"), ("RandomizeQuestions", "false"),
                                ("BlockVisibility", "Expanded")])
    BLOCKS.append(b)
    return b["ID"]


B1 = block("S1 - Anagrafica", ["INTRO", "Q1.1", "Q1.2", "Q1.3", "Q1.4", "Q1.5", PB, "Q1.6", "Q1.7"], default=True)
B2 = block("S2 - Maturità digitale e gestione per processi", ["Q2.1", "Q2.2", PB, "Q2.3", "Q2.3_NOTA", PB, "Q2.4"])
B3 = block("S3 - Approccio alla Process Automation", ["S3_DEF", "Q3.1", PB, "Q3.2", "Q3.3", PB, "Q3.4A", "Q3.4B"])
B4 = block("S4 - Tecnologie di automazione", ["Q4.1"])
B5A = block("S5 - Mappatura processi (5.1)", ["S5_INTRO", "Q5.1"])
B5B = block("S5 - Approfondimento famiglie (5.2-5.3)", ["Q5.2", PB, "Q5.3a", PB, "Q5.3b", PB, "Q5.3c", PB, "Q5.3d"])
B6 = block("S6 - Agentic Automation", ["Q6.1", PB, "Q6.2"])
B7A = block("S7 - Organizzazione e competenze (7.1, tutti)", ["Q7.1"])
B7B = block("S7 - Organizzazione e competenze (7.2-7.6)", ["Q7.2", PB, "Q7.3", PB, "Q7.4", PB, "Q7.5", PB, "Q7.6"])
B8 = block("S8 - Esternalizzazione", ["Q8.1", PB, "Q8.2"])
B9 = block("S9 - Aspettative e risultati", ["S9_INTRO", "Q9.1", PB, "Q9.2"])
B10A = block("S10 - Barriere e spesa (10.1-10.2)", ["Q10.1a", PB, "Q10.1b", PB, "Q10.1c", PB, "Q10.2"])
B10B = block("S10 - Dinamica e ripartizione spesa (10.3-10.4)", ["Q10.3a", "Q10.3b", PB, "Q10.4_ns", "Q10.4"])
B10C = block("S10 - Benefici e prossimi passi (10.5-10.7)", ["Q10.5", PB, "Q10.6a", PB, "Q10.6b", PB, "Q10.7"])
TRASH = OrderedDict([("Type", "Trash"), ("Description", "Trash / Unused Questions"),
                     ("ID", rid("BL_")), ("BlockElements", [])])
BLOCKS.insert(1, TRASH)

# controllo: ogni domanda in esattamente un blocco
_used = [e["QuestionID"] for b in BLOCKS for e in b["BlockElements"] if e["Type"] == "Question"]
assert sorted(_used) == sorted(q["qid"] for q in QUESTIONS.values()), "domande non assegnate o duplicate"

# ==========================================================================
# SURVEY FLOW
# ==========================================================================
_fid = [1]


def nf():
    _fid[0] += 1
    return "FL_%d" % _fid[0]


def f_block(bid, default=False):
    return OrderedDict([("Type", "Block" if default else "Standard"), ("ID", bid),
                        ("FlowID", nf()), ("Autofill", [])])


def f_branch(blog, flow):
    fl = nf()
    return OrderedDict([("Type", "Branch"), ("FlowID", fl), ("Description", "New Branch"),
                        ("BranchLogic", blog), ("Flow", flow)])


def f_ed(pairs):
    return OrderedDict([("Type", "EmbeddedData"), ("FlowID", nf()), ("EmbeddedData", [
        OrderedDict([("Description", k), ("Type", "Custom"), ("Field", k), ("VariableType", "String"),
                     ("DataVisibility", []), ("AnalyzeText", False), ("Value", v)]) for k, v in pairs])])


def f_end():
    return OrderedDict([("Type", "EndSurvey"), ("FlowID", nf())])


def ADOPTER():
    # Prosegue chi NON è (3.1 = d) E (4.1 = h)  <=>  3.1 d non selezionata OPPURE 4.1 h non selezionata
    return blogic([c_sel("Q3.1", "d", "NotSelected"), c_sel("Q4.1", "h", "NotSelected")], "Or")


FLOW = []
FLOW.append(f_ed([("elig_AFC", "0"), ("elig_ACQ", "0"), ("elig_OPS", "0"), ("elig_CS", "0")]))
FLOW.append(f_block(B1, default=True))
# Screen-out
FLOW.append(f_branch(blogic([c_sel("Q1.6", "q")]),                       # Public Administration
                     [f_ed([("screen_out", "Public Administration")]), f_end()]))
FLOW.append(f_branch(blogic([c_sel("Q1.7", "a")]),                       # Fino a 49 dipendenti
                     [f_ed([("screen_out", "Fino a 49 dipendenti")]), f_end()]))
FLOW += [f_block(B2), f_block(B3), f_block(B4)]

# Sezione 5: saltata da chi ha risposto d) alla 3.1 E h) alla 4.1
sec5 = [f_block(B5A)]
# azzeramento prima del calcolo: se il rispondente torna indietro e modifica la 5.1, i flag vengono ricalcolati
sec5.append(f_ed([("elig_AFC", "0"), ("elig_ACQ", "0"), ("elig_OPS", "0"), ("elig_CS", "0")]))
for code, key, row, lab, solo in FAM_52:
    # famiglia selezionabile alla 5.2 se alla 5.1 ha almeno una delle prime tre colonne
    sec5.append(f_branch(blogic([c_cell("Q5.1", row, col) for col in (1, 2, 3)], "Or"),
                         [f_ed([("elig_" + code, "1")])]))
sec5.append(f_ed([("elig_pattern",
                   "P${e://Field/elig_AFC}${e://Field/elig_ACQ}${e://Field/elig_OPS}${e://Field/elig_CS}")]))
sec5.append(f_block(B5B))
FLOW.append(f_branch(ADOPTER(), sec5))

FLOW += [f_block(B6), f_block(B7A)]
# Sezioni 7 (dalla 7.2) e 8: saltate da chi ha risposto d) alla 3.1 E h) alla 4.1
FLOW.append(f_branch(ADOPTER(), [f_block(B7B), f_block(B8)]))
# Sezione 9: saltata da chi ha risposto d) alla 3.1, oppure non ha selezionato alla 5.1 alcuna casella
# nelle colonne «Automazione intelligente» e «Agenti AI autonomi»
FLOW.append(f_branch(blogic([c_sel("Q3.1", "d", "NotSelected")]), [
    f_branch(blogic([c_cell("Q5.1", r, c) for r in range(1, 12) for c in (2, 3)], "Or"),
             [f_block(B9)])]))
FLOW.append(f_block(B10A))
# 10.3 e 10.4: mostrate a chi alla 10.2 ha selezionato una fascia da b) a i)
FLOW.append(f_branch(blogic([c_sel("Q10.2", k) for k in "bcdefghi"], "Or"), [f_block(B10B)]))
FLOW.append(f_block(B10C))

FLOW_ROOT = OrderedDict([("Type", "Root"), ("FlowID", "FL_1"), ("Flow", FLOW),
                         ("Properties", OrderedDict([("Count", _fid[0]), ("RemovedFieldsets", [])]))])

# ==========================================================================
# ASSEMBLAGGIO QSF
# ==========================================================================


def element(el, primary, secondary, tertiary, payload):
    return OrderedDict([("SurveyID", SURVEY_ID), ("Element", el), ("PrimaryAttribute", primary),
                        ("SecondaryAttribute", secondary), ("TertiaryAttribute", tertiary),
                        ("Payload", payload)])


SURVEY_OPTIONS = OrderedDict([
    ("BackButton", "true"), ("SaveAndContinue", "true"), ("SurveyProtection", "PublicSurvey"),
    ("BallotBoxStuffingPrevention", "false"), ("NoIndex", "Yes"), ("SecureResponseFiles", "true"),
    ("SurveyExpiration", "None"), ("SurveyTermination", "DefaultMessage"), ("Header", ""), ("Footer", ""),
    ("ProgressBarDisplay", "NoText"), ("PartialData", "+1 week"), ("ValidationMessage", None),
    ("PreviousButton", " ← "), ("NextButton", " → "),
    ("SurveyTitle", "Survey IBPA 2026/2027 – Osservatorio Intelligent Business Process Automation"),
    ("NewScoring", 1),
    ("SurveyMetaDescription", "Osservatorio Intelligent Business Process Automation – Politecnico di Milano"),
    ("ShowExportTags", "false"), ("CollectGeoLocation", "false"), ("PasswordProtection", "No"),
    ("AnonymizeResponse", "No"), ("RefererCheck", "No"), ("RecaptchaV3", "false"),
    ("ConfirmStart", False), ("AutoConfirmStart", False), ("ResponseSummary", "No"),
    ("EOSMessageLibrary", None), ("EOSMessage", None), ("EOSRedirectURL", None),
    ("EmailThankYou", "false"), ("ThankYouEmailMessageLibrary", None), ("ThankYouEmailMessage", None),
    ("ValidateMessage", "false"), ("ValidationMessageLibrary", None), ("InactiveSurvey", "DefaultMessage"),
    ("PartialDeletion", None), ("PartialDataCloseAfter", "LastActivity"), ("InactiveMessageLibrary", None),
    ("InactiveMessage", None), ("AvailableLanguages", {"IT": []}), ("SurveyName", SURVEY_NAME),
])

elements = [
    element("BL", "Survey Blocks", None, None, BLOCKS),
    element("FL", "Survey Flow", None, None, FLOW_ROOT),
    element("PROJ", "CORE", None, "1.1.0", {"ProjectCategory": "CORE", "SchemaVersion": "1.1.0"}),
    element("QC", "Survey Question Count", str(len(QUESTIONS)), None, None),
    element("RS", RS_ID, "Default Response Set", None, None),
    element("SCO", "Scoring", None, None, OrderedDict([
        ("ScoringCategories", []), ("ScoringCategoryGroups", []), ("ScoringSummaryCategory", None),
        ("ScoringSummaryAfterQuestions", 0), ("ScoringSummaryAfterSurvey", 0),
        ("DefaultScoringCategory", None), ("AutoScoringCategory", None)])),
    element("SO", "Survey Options", None, None, SURVEY_OPTIONS),
]
for tag, q in QUESTIONS.items():
    elements.append(element("SQ", q["qid"], short(q["text"]), None, q["payload"]))
elements.append(element("STAT", "Survey Statistics", None, None,
                        {"MobileCompatible": True, "ID": "Survey Statistics"}))

QSF = OrderedDict([
    ("SurveyEntry", OrderedDict([
        ("SurveyID", SURVEY_ID), ("SurveyName", SURVEY_NAME), ("SurveyDescription", None),
        ("SurveyOwnerID", OWNER_ID), ("SurveyBrandID", "default"), ("DivisionID", None),
        ("SurveyLanguage", "IT"), ("SurveyActiveResponseSet", RS_ID), ("SurveyStatus", "Inactive"),
        ("SurveyStartDate", "0000-00-00 00:00:00"), ("SurveyExpirationDate", "0000-00-00 00:00:00"),
        ("SurveyCreationDate", NOW), ("CreatorID", OWNER_ID), ("LastModified", NOW),
        ("LastAccessed", "0000-00-00 00:00:00"), ("LastActivated", "0000-00-00 00:00:00"),
        ("Deleted", None)])),
    ("SurveyElements", elements),
])

with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(QSF, fh, ensure_ascii=False, separators=(",", ":"))

print("Scritto %s: %d domande (%d SQ), %d blocchi, flow fino a FL_%d"
      % (OUT, sum(1 for q in QUESTIONS.values() if q["kind"] != "DB"), len(QUESTIONS),
         len(BLOCKS), _fid[0]))
