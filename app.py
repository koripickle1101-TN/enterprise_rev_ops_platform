import csv
from datetime import date
from io import StringIO
import streamlit as st

st.set_page_config(
    page_title="Enterprise Revenue Operations Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

DEFAULT_CASES = [
    {"Case ID":"REV-0001","Payer Group":"Commercial","Workflow Domain":"Patient Access","Service Line":"Orthopedics","Risk":"High","Owner":"Patient Access Lead","Days Open":7,"SLA Limit":5,"Exposure":18450,"Status":"Needs Documentation","Required Docs":"Order;Insurance Card;Clinical Note;Medical Necessity Note","Present Docs":"Order;Insurance Card","First Control Loss":"Documentation Control","Payer Rule":"Medical necessity narrative required before authorization submission.","Next Action":"Validate documentation packet and assign same day authorization follow up."},
    {"Case ID":"REV-0002","Payer Group":"Medicare Advantage","Workflow Domain":"Authorization Control","Service Line":"Neurology","Risk":"High","Owner":"Prior Authorization Lead","Days Open":9,"SLA Limit":5,"Exposure":32700,"Status":"Escalate","Required Docs":"Order;Neuro Exam;Failed Conservative Therapy;Imaging Rationale","Present Docs":"Order;Neuro Exam","First Control Loss":"Authorization Readiness Control","Payer Rule":"Conservative therapy evidence and imaging rationale required.","Next Action":"Escalate payer follow up and request missing medical necessity support."},
    {"Case ID":"REV-0003","Payer Group":"Medicaid","Workflow Domain":"Documentation Readiness","Service Line":"Rehabilitation","Risk":"Moderate","Owner":"Documentation Specialist","Days Open":4,"SLA Limit":5,"Exposure":12600,"Status":"Needs Eligibility Review","Required Docs":"Plan of Care;Therapy Evaluation;Frequency Order","Present Docs":"Plan of Care;Therapy Evaluation","First Control Loss":"Documentation Control","Payer Rule":"Therapy frequency order must match requested treatment period.","Next Action":"Confirm therapy frequency order before submission."},
    {"Case ID":"REV-0004","Payer Group":"Commercial","Workflow Domain":"Routing Intelligence","Service Line":"Cardiology","Risk":"High","Owner":"RCM Analyst","Days Open":8,"SLA Limit":4,"Exposure":28600,"Status":"Routing Review","Required Docs":"Referral;Cardiology Note;Payer Route;Procedure Code","Present Docs":"Referral;Cardiology Note;Procedure Code","First Control Loss":"Ownership Control","Payer Rule":"Correct payer route must be established before submission.","Next Action":"Correct payer route and document escalation owner."},
    {"Case ID":"REV-0005","Payer Group":"Marketplace","Workflow Domain":"Eligibility Verification","Service Line":"Imaging","Risk":"Moderate","Owner":"Eligibility Specialist","Days Open":5,"SLA Limit":5,"Exposure":11250,"Status":"Needs Eligibility Review","Required Docs":"Eligibility Response;Benefit Check;Order","Present Docs":"Order","First Control Loss":"Patient Access Control","Payer Rule":"Eligibility response and benefit confirmation required before scheduling clearance.","Next Action":"Complete eligibility response and benefit confirmation."},
    {"Case ID":"REV-0006","Payer Group":"Self Pay","Workflow Domain":"Financial Clearance","Service Line":"Surgery","Risk":"Low","Owner":"Financial Counselor","Days Open":2,"SLA Limit":5,"Exposure":7200,"Status":"Financial Review","Required Docs":"Estimate;Payment Plan Review","Present Docs":"Estimate","First Control Loss":"Patient Access Control","Payer Rule":"Financial pathway review required before scheduled procedure date.","Next Action":"Complete patient financial pathway review."},
    {"Case ID":"REV-0007","Payer Group":"Commercial","Workflow Domain":"Denial Prevention","Service Line":"Oncology","Risk":"High","Owner":"Denial Prevention Lead","Days Open":10,"SLA Limit":5,"Exposure":44200,"Status":"Pre Denial Review","Required Docs":"Treatment Plan;Medical Necessity Note;Prior Therapy History;Payer Policy Match","Present Docs":"Treatment Plan;Medical Necessity Note","First Control Loss":"Time Control","Payer Rule":"Policy matched documentation required for high cost treatment authorization.","Next Action":"Run pre denial review and attach policy matched documentation."},
    {"Case ID":"REV-0008","Payer Group":"Medicare Advantage","Workflow Domain":"Authorization Control","Service Line":"Imaging","Risk":"High","Owner":"Prior Authorization Lead","Days Open":6,"SLA Limit":5,"Exposure":19600,"Status":"Needs Documentation","Required Docs":"Order;Clinical Note;Failed Therapy Evidence;Imaging Rationale","Present Docs":"Order;Clinical Note","First Control Loss":"Authorization Readiness Control","Payer Rule":"Failed therapy evidence must be documented for advanced imaging authorization.","Next Action":"Request therapy evidence and attach imaging rationale."},
    {"Case ID":"REV-0009","Payer Group":"Medicaid","Workflow Domain":"Documentation Readiness","Service Line":"Behavioral Health","Risk":"Moderate","Owner":"Clinical Documentation Liaison","Days Open":6,"SLA Limit":5,"Exposure":9800,"Status":"Needs Documentation","Required Docs":"Assessment;Treatment Plan;Provider Attestation","Present Docs":"Assessment","First Control Loss":"Documentation Control","Payer Rule":"Provider attestation and treatment plan must be present before routing.","Next Action":"Secure treatment plan and attestation before routing."},
    {"Case ID":"REV-0010","Payer Group":"Commercial","Workflow Domain":"Eligibility Verification","Service Line":"Primary Care","Risk":"Low","Owner":"Patient Access Specialist","Days Open":1,"SLA Limit":5,"Exposure":2600,"Status":"Ready","Required Docs":"Eligibility Response;Benefit Check","Present Docs":"Eligibility Response;Benefit Check","First Control Loss":"None","Payer Rule":"Standard eligibility confirmation complete.","Next Action":"Proceed with standard review."},
    {"Case ID":"REV-0011","Payer Group":"Medicare Advantage","Workflow Domain":"Patient Access","Service Line":"Rehabilitation","Risk":"High","Owner":"Access Operations Manager","Days Open":7,"SLA Limit":5,"Exposure":22300,"Status":"Escalate","Required Docs":"Order;Eligibility Response;Plan of Care;Authorization Pathway","Present Docs":"Order;Plan of Care","First Control Loss":"Patient Access Control","Payer Rule":"Eligibility pathway and authorization route must be confirmed before start of care.","Next Action":"Escalate access pathway and complete eligibility validation."},
    {"Case ID":"REV-0012","Payer Group":"Commercial","Workflow Domain":"Routing Intelligence","Service Line":"Neurology","Risk":"Moderate","Owner":"RCM Analyst","Days Open":5,"SLA Limit":5,"Exposure":14100,"Status":"Routing Review","Required Docs":"Payer Route;Order;Clinical Note","Present Docs":"Order;Clinical Note","First Control Loss":"Ownership Control","Payer Rule":"Correct payer route required to prevent duplicate submission.","Next Action":"Confirm payer route and prevent duplicate submission."},
    {"Case ID":"REV-0013","Payer Group":"Marketplace","Workflow Domain":"Denial Prevention","Service Line":"Cardiology","Risk":"High","Owner":"Revenue Integrity Analyst","Days Open":8,"SLA Limit":5,"Exposure":24250,"Status":"Pre Denial Review","Required Docs":"Cardiology Note;Medical Necessity Note;Payer Policy Match;Procedure Code","Present Docs":"Cardiology Note;Procedure Code","First Control Loss":"Documentation Control","Payer Rule":"Payer policy match and medical necessity support required before submission.","Next Action":"Attach payer policy match and medical necessity support."},
    {"Case ID":"REV-0014","Payer Group":"Commercial","Workflow Domain":"Authorization Control","Service Line":"Surgery","Risk":"Moderate","Owner":"Prior Authorization Coordinator","Days Open":3,"SLA Limit":5,"Exposure":17300,"Status":"Ready for Submission","Required Docs":"Order;Surgical Note;Procedure Code;Site of Service","Present Docs":"Order;Surgical Note;Procedure Code;Site of Service","First Control Loss":"None","Payer Rule":"Required surgical authorization packet complete.","Next Action":"Submit and monitor payer response window."}
]

REQUIRED_COLUMNS = list(DEFAULT_CASES[0].keys())
CONTROL_DOMAINS = [
    ("Patient Access Control", "Eligibility, benefits, scheduling pathway, and financial clearance stability."),
    ("Authorization Readiness Control", "Required evidence, payer rule alignment, and submission readiness."),
    ("Documentation Control", "Clinical packet completeness, medical necessity support, and attestation status."),
    ("Ownership Control", "Assigned human owner, routing clarity, escalation pathway, and handoff accountability."),
    ("Time Control", "Aging, SLA pressure, stalled work, and delay prevention before denial risk grows.")
]


def money(value):
    return "${:,.0f}".format(float(value))


def safe(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def split_docs(value):
    if isinstance(value, list):
        return value
    return [item.strip() for item in str(value).split(";") if item.strip()]


def missing_docs(case):
    required = split_docs(case.get("Required Docs", ""))
    present = set(split_docs(case.get("Present Docs", "")))
    return [doc for doc in required if doc not in present]


def readiness_score(case):
    doc_penalty = len(missing_docs(case)) * 13
    aging_penalty = max(0, int(case.get("Days Open", 0)) - int(case.get("SLA Limit", 0))) * 8
    risk_penalty = {"Low": 0, "Moderate": 7, "High": 17}.get(case.get("Risk"), 0)
    return max(0, min(100, 100 - doc_penalty - aging_penalty - risk_penalty))


def workflow_loss_index(case):
    base = {"Low": 10, "Moderate": 30, "High": 50}.get(case.get("Risk"), 20)
    score = base + len(missing_docs(case)) * 9 + max(0, int(case.get("Days Open", 0)) - int(case.get("SLA Limit", 0))) * 8
    if case.get("First Control Loss") == "Ownership Control":
        score += 10
    if case.get("Status") in ["Escalate", "Pre Denial Review"]:
        score += 8
    return max(0, min(100, score))


def loss_label(score):
    if score >= 76:
        return "Escalation Required"
    if score >= 51:
        return "Control Loss"
    if score >= 26:
        return "Watch"
    return "Stable"


def countdown(case):
    return int(case.get("SLA Limit", 0)) - int(case.get("Days Open", 0))


def load_uploaded_cases(uploaded_file):
    if uploaded_file is None:
        return DEFAULT_CASES
    text = uploaded_file.getvalue().decode("utf-8")
    reader = csv.DictReader(StringIO(text))
    rows = []
    for row in reader:
        clean = {column: row.get(column, "") for column in REQUIRED_COLUMNS}
        for numeric in ["Days Open", "SLA Limit", "Exposure"]:
            try:
                clean[numeric] = int(float(clean[numeric]))
            except Exception:
                clean[numeric] = 0
        rows.append(clean)
    return rows if rows else DEFAULT_CASES


def table_html(rows, columns):
    head = "".join(["<th>{}</th>".format(safe(c)) for c in columns])
    body = ""
    for row in rows:
        body += "<tr>" + "".join(["<td>{}</td>".format(safe(row.get(c, ""))) for c in columns]) + "</tr>"
    return '<div class="table-scroll"><table class="queue-table"><thead><tr>{}</tr></thead><tbody>{}</tbody></table></div>'.format(head, body)


def bar_html(label, value, max_value):
    width = 0 if max_value == 0 else (value / max_value) * 100
    return '<div class="bar-row"><div class="bar-label">{}</div><div class="track"><div class="fill" style="width:{}%"></div></div><div class="bar-value">{}</div></div>'.format(safe(label), width, value)


def metric_card(label, value, note):
    return f'<div class="metric-card"><div class="metric-label">{safe(label)}</div><div class="metric-number">{safe(value)}</div><div class="metric-note">{safe(note)}</div></div>'


def brief_text(rows):
    total = len(rows)
    high = sum(1 for c in rows if c.get("Risk") == "High")
    sla = sum(1 for c in rows if int(c.get("Days Open", 0)) >= int(c.get("SLA Limit", 0)))
    exposure = sum(float(c.get("Exposure", 0)) for c in rows)
    owners = len(set(c.get("Owner") for c in rows))
    avg_ready = round(sum(readiness_score(c) for c in rows) / total, 1) if total else 0
    return f"""Enterprise Revenue Operations Platform
Created by Kori Pickle
Generated {date.today().isoformat()}

Synthetic Data Notice
This brief uses synthetic records only. It does not contain PHI. It does not make payer, clinical, billing, coding, or patient specific decisions.

Active Command View
Total synthetic records: {total}
High risk records: {high}
SLA pressure signals: {sla}
Distinct operational owners: {owners}
Average readiness score: {avg_ready}
Simulated exposure: {money(exposure)}

Kori Pickle Workflow Loss Control Method
Core question: where did the workflow first lose control?

Recommended Human Review Actions
1. Stabilize missing documentation before payer submission.
2. Escalate records at or beyond SLA limit to the assigned owner.
3. Validate payer rule requirements before resubmission or appeal work begins.
4. Document every human review action in the audit log.
5. Use readiness scoring as a prioritization signal only.
"""

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;500&display=swap');

:root { --orange: #FF8200; --black: #000000; --white: #FFFFFF; }

[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="collapsedControl"], header, footer {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}

html, body, [data-testid="stAppViewContainer"] { background: var(--white) !important; color: var(--black) !important; }
.block-container { max-width: 1380px !important; padding-top: 0 !important; padding-left: 3rem !important; padding-right: 3rem !important; padding-bottom: 5rem !important; }

p, div, span, label, input, textarea, button, select { font-family: Inter, Arial, sans-serif !important; color: var(--black) !important; }
h1, h2, h3 { font-family: "Playfair Display", Georgia, serif !important; font-weight: 400 !important; letter-spacing: -0.04em !important; color: var(--black) !important; }

[data-testid="stSidebar"] { background: var(--white) !important; border-right: 4px solid var(--orange) !important; }
[data-testid="stSidebar"] label { font-size: 0.67rem !important; letter-spacing: 0.18em !important; text-transform: uppercase !important; }
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, textarea { background: var(--white) !important; border: 1px solid var(--black) !important; border-radius: 0 !important; box-shadow: inset 6px 0 0 var(--orange) !important; }
span[data-baseweb="tag"], [data-baseweb="tag"] { background: var(--white) !important; color: var(--black) !important; border: 1px solid var(--orange) !important; border-radius: 0 !important; }

button, .stDownloadButton button { border-radius: 0 !important; border: 1px solid var(--black) !important; background: var(--white) !important; color: var(--black) !important; letter-spacing: 0.12em !important; text-transform: uppercase !important; box-shadow: inset 6px 0 0 var(--orange) !important; }

.brand-shell { border-left: 1px solid var(--black); border-right: 1px solid var(--black); border-top: 8px solid var(--orange); padding: 2rem 2.2rem 2.7rem 2.2rem; background: var(--white); }
.signature-name { font-family: "Great Vibes", cursive !important; font-weight: 400 !important; font-size: clamp(4.6rem, 8vw, 8.4rem); line-height: 0.82; color: var(--black) !important; }
.signature-subline { margin-top: 0.9rem; font-size: 0.78rem; letter-spacing: 0.44em; text-transform: uppercase; font-weight: 500; }
.signature-intelligence { margin-top: 0.42rem; font-size: 0.82rem; letter-spacing: 0.54em; text-transform: uppercase; color: var(--orange) !important; font-weight: 500; }
.signature-rule { height: 6px; background: var(--orange); margin: 1.5rem 0 2.4rem 0; }

.kicker { font-size: 0.68rem; letter-spacing: 0.34em; text-transform: uppercase; font-weight: 500; margin-bottom: 1rem; }
.hero-grid { display: grid; grid-template-columns: 0.9fr 0.75fr; gap: 2rem; align-items: stretch; }
.hero-title { font-family: "Playfair Display", Georgia, serif !important; font-size: clamp(4rem, 7vw, 7.6rem); line-height: 0.92; letter-spacing: -0.055em; font-weight: 400 !important; margin: 0; }
.hero-title span { color: var(--orange) !important; font-family: "Playfair Display", Georgia, serif !important; font-weight: 400 !important; }
.hero-copy { margin-top: 1.8rem; max-width: 850px; font-size: 1.04rem; line-height: 1.84; font-weight: 400; }
.identity-panel { border: 1px solid var(--black); border-top: 8px solid var(--orange); padding: 2rem; min-height: 410px; display: flex; flex-direction: column; justify-content: space-between; }
.identity-statement { font-family: "Playfair Display", Georgia, serif !important; font-size: clamp(2.35rem, 4.1vw, 4rem); line-height: 1.02; letter-spacing: -0.045em; }
.identity-domains { font-size: 0.86rem; letter-spacing: 0.24em; text-transform: uppercase; line-height: 2.1; font-weight: 500; }
.badge-row { display: flex; gap: 1rem; flex-wrap: wrap; margin: 2rem 0 2.5rem 0; }
.badge { border: 1px solid var(--black); border-left: 8px solid var(--orange); padding: 0.78rem 1rem; letter-spacing: 0.16em; text-transform: uppercase; font-size: 0.72rem; font-weight: 600; }

.metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.2rem; margin: 2.4rem 0; }
.metric-card { border: 1px solid var(--black); border-left: 8px solid var(--orange); padding: 1.8rem 1.5rem; min-height: 172px; background: var(--white); }
.metric-label { letter-spacing: 0.24em; text-transform: uppercase; font-size: 0.72rem; font-weight: 600; }
.metric-number { font-family: "Playfair Display", Georgia, serif !important; font-weight: 400 !important; letter-spacing: -0.055em; font-size: clamp(3.1rem, 5vw, 5.2rem); line-height: 1.05; color: var(--orange) !important; margin-top: 1.1rem; }
.metric-note { font-size: 0.9rem; line-height: 1.55; margin-top: 0.9rem; }

.stTabs [data-baseweb="tab-list"] { gap: 1rem; border-bottom: 2px solid var(--black); overflow-x: auto; }
.stTabs [data-baseweb="tab"] { border: 1px solid var(--black); border-radius: 0 !important; padding: 1rem 1.2rem; background: var(--white); }
.stTabs [aria-selected="true"] { background: var(--orange) !important; }
.stTabs [data-baseweb="tab"] p { font-size: 0.88rem; letter-spacing: 0.08em; }

.section-title { font-family: "Playfair Display", Georgia, serif !important; font-size: clamp(2.8rem, 5vw, 5rem); letter-spacing: -0.055em; line-height: 0.95; margin: 3rem 0 1.4rem 0; }
.section-copy { font-size: 1.03rem; line-height: 1.85; max-width: 900px; }
.panel { border: 1px solid var(--black); border-left: 8px solid var(--orange); padding: 2rem; margin: 1.4rem 0; }
.panel-title { letter-spacing: 0.24em; text-transform: uppercase; font-size: 0.72rem; font-weight: 600; margin-bottom: 1rem; }
.callout { border: 1px solid var(--black); border-top: 8px solid var(--orange); padding: 2rem; margin: 2rem 0; }

.table-scroll { overflow-x: auto; border: 1px solid var(--black); margin-top: 1.2rem; }
.queue-table { border-collapse: collapse; width: 100%; font-size: 0.92rem; }
.queue-table th { border-bottom: 1px solid var(--black); padding: 0.85rem; text-align: left; letter-spacing: 0.14em; text-transform: uppercase; font-size: 0.68rem; white-space: nowrap; }
.queue-table td { border-bottom: 1px solid var(--black); padding: 0.85rem; white-space: nowrap; }
.queue-table tr:last-child td { border-bottom: 0; }

.bar-row { display: grid; grid-template-columns: 150px 1fr 50px; align-items: center; gap: 1rem; margin: 1rem 0; }
.track { height: 22px; border: 1px solid var(--black); background: var(--white); }
.fill { height: 100%; background: var(--orange); }
.bar-label { font-weight: 500; }
.bar-value { font-family: "Playfair Display", Georgia, serif !important; font-size: 1.75rem; color: var(--orange) !important; }

.method-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; margin-top: 1.5rem; }
.method-card { border: 1px solid var(--black); border-top: 7px solid var(--orange); padding: 1.2rem; min-height: 210px; }
.method-card h4 { font-family: "Playfair Display", Georgia, serif !important; font-weight: 400 !important; font-size: 1.55rem; line-height: 1.05; margin: 0 0 1rem 0; }
.method-card p { font-size: 0.82rem; line-height: 1.65; }

.footer-lockup { margin-top: 4rem; border-top: 6px solid var(--orange); border-bottom: 6px solid var(--orange); padding: 2.2rem 0; text-align: center; }
.footer-signature { font-family: "Great Vibes", cursive !important; font-size: clamp(4rem, 8vw, 7rem); line-height: 0.9; }
.footer-links a { display: inline-block; border: 1px solid var(--black); padding: 0.8rem 1.1rem; margin: 1rem 0.4rem 0 0.4rem; text-decoration: none !important; color: var(--black) !important; letter-spacing: 0.15em; text-transform: uppercase; font-size: 0.75rem; box-shadow: inset 6px 0 0 var(--orange); }

@media (max-width: 900px) {
    .block-container { padding-left: 1.35rem !important; padding-right: 1.35rem !important; }
    .brand-shell { padding: 1.35rem; }
    .hero-grid, .metric-grid, .method-grid { grid-template-columns: 1fr; }
    .hero-title { font-size: 4.2rem; }
    .signature-name { font-size: 4.7rem; }
    .bar-row { grid-template-columns: 105px 1fr 35px; gap: 0.7rem; }
}
</style>
""", unsafe_allow_html=True)

uploaded = st.sidebar.file_uploader("Synthetic CSV upload only", type=["csv"])
all_cases = load_uploaded_cases(uploaded)

risk_options = sorted(set(c["Risk"] for c in all_cases))
payer_options = sorted(set(c["Payer Group"] for c in all_cases))
workflow_options = sorted(set(c["Workflow Domain"] for c in all_cases))
service_options = sorted(set(c["Service Line"] for c in all_cases))

risk_filter = st.sidebar.multiselect("Filter by risk level", risk_options, default=risk_options)
payer_filter = st.sidebar.multiselect("Filter by payer group", payer_options, default=payer_options)
workflow_filter = st.sidebar.multiselect("Filter by workflow area", workflow_options, default=workflow_options)
service_filter = st.sidebar.multiselect("Filter by service line", service_options, default=service_options)

active_cases = [c for c in all_cases if c["Risk"] in risk_filter and c["Payer Group"] in payer_filter and c["Workflow Domain"] in workflow_filter and c["Service Line"] in service_filter]
if not active_cases:
    active_cases = []

total = len(active_cases)
high_count = sum(1 for c in active_cases if c["Risk"] == "High")
sla_count = sum(1 for c in active_cases if int(c["Days Open"]) >= int(c["SLA Limit"]))
exposure_total = sum(float(c["Exposure"]) for c in active_cases)
readiness_avg = round(sum(readiness_score(c) for c in active_cases) / total) if total else 0
owners = len(set(c["Owner"] for c in active_cases)) if active_cases else 0
avg_age = round(sum(int(c["Days Open"]) for c in active_cases) / total, 1) if total else 0

st.markdown("""
<div class="brand-shell">
    <div class="signature-name">Kori Pickle</div>
    <div class="signature-subline">Healthcare Operations</div>
    <div class="signature-intelligence">Intelligence</div>
    <div class="signature-rule"></div>
    <div class="kicker">Kori Pickle • Healthcare Operations Intelligence</div>
    <div class="hero-grid">
        <div>
            <div class="hero-title">Enterprise<br>Revenue<br><span>Operations</span><br>Platform</div>
            <div class="hero-copy">A premium synthetic no PHI healthcare operations command center for patient access, eligibility verification, prior authorization pressure tracking, routing intelligence, documentation readiness, denial prevention, payer friction analysis, and responsible operational intelligence.</div>
            <div class="hero-copy">This build functions as an operational review workbench: filter synthetic cases, isolate ownership gaps, simulate stabilization impact, generate escalation language, and build a leadership brief from the active command view.</div>
            <div class="badge-row">
                <div class="badge">No PHI</div><div class="badge">Synthetic Data</div><div class="badge">Human Review Required</div><div class="badge">Built by Kori Pickle</div>
            </div>
        </div>
        <div class="identity-panel">
            <div class="panel-title">Operational Identity</div>
            <div class="identity-statement">Workflow visibility before revenue damage.</div>
            <div class="hero-copy">Designed around one question: where did the workflow first lose control?</div>
            <div class="identity-domains">Patient Access • Authorization Control • Documentation Readiness • Denial Prevention</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="metric-grid">' +
    metric_card("High Risk Records", str(high_count), "Prioritized operational review queue.") +
    metric_card("SLA Pressure", str(sla_count), "Records aged at or above SLA limit.") +
    metric_card("Synthetic Exposure", money(exposure_total), "Portfolio simulation only.") +
    metric_card("Readiness Average", str(readiness_avg), "Aggregate workflow readiness score.") +
    '</div>',
    unsafe_allow_html=True
)

tabs = st.tabs([
    "Command Center", "Workflow Loss Control", "Readiness Engine", "Documentation Detector", "Payer Rule Lab",
    "SLA Countdown", "Work Queue", "Audit Log", "Stabilization Simulator", "2027 API Checklist", "About Kori", "Brief Builder"
])

with tabs[0]:
    st.markdown('<div class="section-title">Live Command Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">Use the sidebar filters to isolate operational pressure across payer group, workflow domain, service line, and risk level.</div>', unsafe_allow_html=True)
    st.markdown(table_html(active_cases, ["Case ID", "Payer Group", "Workflow Domain", "Service Line", "Risk", "Owner", "Days Open", "Status"]), unsafe_allow_html=True)
    counts = {level: sum(1 for c in active_cases if c["Risk"] == level) for level in ["High", "Moderate", "Low"]}
    max_count = max(counts.values()) if counts else 1
    bars = "".join(bar_html(k, v, max_count) for k, v in counts.items())
    st.markdown(f'<div class="panel"><div class="panel-title">Risk Queue Distribution</div>{bars}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="callout"><div class="section-title">Executive Interpretation</div><div class="section-copy">The active view shows {total} synthetic records, {high_count} high risk records, {sla_count} SLA pressure signals, average aging of {avg_age} days, {owners} distinct owners, and {money(exposure_total)} in simulated exposure. These are prioritization signals for human review, not automated payer or clinical decisions.</div></div>', unsafe_allow_html=True)

with tabs[1]:
    st.markdown('<div class="section-title">Workflow Loss Control Method</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">A Kori Pickle method for identifying where a healthcare revenue workflow first lost control before it becomes a denial, delay, patient access issue, or avoidable rework.</div>', unsafe_allow_html=True)
    method_cards = ""
    for domain, desc in CONTROL_DOMAINS:
        method_cards += f'<div class="method-card"><h4>{safe(domain)}</h4><p>{safe(desc)}</p></div>'
    st.markdown(f'<div class="method-grid">{method_cards}</div>', unsafe_allow_html=True)
    if active_cases:
        selected = st.selectbox("Select synthetic case for workflow loss analysis", [c["Case ID"] for c in active_cases])
        case = next(c for c in active_cases if c["Case ID"] == selected)
        loss = workflow_loss_index(case)
        st.markdown(f'<div class="panel"><div class="panel-title">Case Control Finding</div><div class="section-copy">{safe(selected)} is classified as {safe(loss_label(loss))}. The first control loss appears in {safe(case["First Control Loss"])}. Next owner: {safe(case["Owner"])}. Recommended action: {safe(case["Next Action"])}</div></div>', unsafe_allow_html=True)

with tabs[2]:
    st.markdown('<div class="section-title">Authorization Readiness Engine</div>', unsafe_allow_html=True)
    readiness_rows = []
    for c in active_cases:
        readiness_rows.append({"Case ID": c["Case ID"], "Readiness Score": readiness_score(c), "Missing Docs": len(missing_docs(c)), "First Control Loss": c["First Control Loss"], "Next Action": c["Next Action"]})
    st.markdown(table_html(readiness_rows, ["Case ID", "Readiness Score", "Missing Docs", "First Control Loss", "Next Action"]), unsafe_allow_html=True)

with tabs[3]:
    st.markdown('<div class="section-title">Missing Documentation Detector</div>', unsafe_allow_html=True)
    doc_rows = []
    for c in active_cases:
        doc_rows.append({"Case ID": c["Case ID"], "Status": c["Status"], "Missing Documentation": ", ".join(missing_docs(c)) if missing_docs(c) else "Complete", "Owner": c["Owner"]})
    st.markdown(table_html(doc_rows, ["Case ID", "Status", "Missing Documentation", "Owner"]), unsafe_allow_html=True)

with tabs[4]:
    st.markdown('<div class="section-title">Payer Rule Lab</div>', unsafe_allow_html=True)
    if active_cases:
        selected_rule = st.selectbox("Select synthetic case", [c["Case ID"] for c in active_cases], key="payer_rule_case")
        case = next(c for c in active_cases if c["Case ID"] == selected_rule)
        st.markdown(f'<div class="panel"><div class="panel-title">Synthetic Payer Rule</div><div class="section-copy">{safe(case["Payer Rule"])}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="panel"><div class="panel-title">Human Review Translation</div><div class="section-copy">Before submission, the assigned owner should confirm whether the required documentation supports this payer rule. This lab does not approve, deny, code, bill, or make clinical decisions.</div></div>', unsafe_allow_html=True)

with tabs[5]:
    st.markdown('<div class="section-title">SLA Breach Countdown</div>', unsafe_allow_html=True)
    sla_rows = []
    for c in active_cases:
        remaining = countdown(c)
        sla_rows.append({"Case ID": c["Case ID"], "Days Open": c["Days Open"], "SLA Limit": c["SLA Limit"], "Countdown": remaining, "Signal": "Breached" if remaining < 0 else "Due Today" if remaining == 0 else "Open", "Owner": c["Owner"]})
    st.markdown(table_html(sla_rows, ["Case ID", "Days Open", "SLA Limit", "Countdown", "Signal", "Owner"]), unsafe_allow_html=True)

with tabs[6]:
    st.markdown('<div class="section-title">Operational Work Queue</div>', unsafe_allow_html=True)
    queue = sorted(active_cases, key=lambda c: (workflow_loss_index(c), int(c["Days Open"])), reverse=True)
    queue_rows = []
    for c in queue:
        queue_rows.append({"Priority": workflow_loss_index(c), "Case ID": c["Case ID"], "Owner": c["Owner"], "Status": c["Status"], "Next Action": c["Next Action"]})
    st.markdown(table_html(queue_rows, ["Priority", "Case ID", "Owner", "Status", "Next Action"]), unsafe_allow_html=True)

with tabs[7]:
    st.markdown('<div class="section-title">Audit Trail and Human Review Log</div>', unsafe_allow_html=True)
    if "audit_log" not in st.session_state:
        st.session_state.audit_log = []
    if active_cases:
        audit_case = st.selectbox("Case reviewed", [c["Case ID"] for c in active_cases], key="audit_case")
        audit_owner = st.text_input("Reviewer name or role", value="Human Reviewer")
        audit_action = st.text_area("Review note", value="Reviewed synthetic case for workflow readiness and escalation priority.")
        if st.button("Add review log entry"):
            st.session_state.audit_log.append({"Date": date.today().isoformat(), "Case ID": audit_case, "Reviewer": audit_owner, "Action": audit_action})
    st.markdown(table_html(st.session_state.audit_log, ["Date", "Case ID", "Reviewer", "Action"]), unsafe_allow_html=True)

with tabs[8]:
    st.markdown('<div class="section-title">Before and After Stabilization Simulator</div>', unsafe_allow_html=True)
    doc_capture = st.slider("Documentation capture improvement", 0, 50, 20)
    aging_reduction = st.slider("Average aging reduction", 0, 10, 3)
    stabilized_exposure = exposure_total * (doc_capture / 100) + high_count * aging_reduction * 1250
    st.markdown(f'<div class="panel"><div class="panel-title">Projected Stabilization Impact</div><div class="metric-number">{money(stabilized_exposure)}</div><div class="section-copy">Synthetic estimate of exposure stabilized when documentation capture improves by {doc_capture} percent and average aging drops by {aging_reduction} days.</div></div>', unsafe_allow_html=True)

with tabs[9]:
    st.markdown('<div class="section-title">2027 API Readiness Checklist</div>', unsafe_allow_html=True)
    checks = [
        "Prior authorization required check available before scheduling",
        "Required documentation identification before submission",
        "Submission status visible to operational owner",
        "Human review override documented",
        "Audit trail retained for every workflow action",
        "Synthetic testing environment separated from patient data",
        "No PHI stored in public portfolio environment"
    ]
    checklist_html = "".join([f'<div class="panel"><div class="section-copy">{safe(item)}</div></div>' for item in checks])
    st.markdown(checklist_html, unsafe_allow_html=True)

with tabs[10]:
    st.markdown('<div class="section-title">About Kori</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">Kori Pickle is a BSHA candidate at the University of Phoenix focused on healthcare operations, revenue cycle management, patient access, prior authorization, denial prevention, health informatics, workflow intelligence, and responsible operational AI. This platform reflects a patient to professional perspective and demonstrates practical systems thinking using synthetic data only.</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="panel-title">Branded Resume Positioning</div><div class="section-copy">Healthcare Operations Intelligence • Revenue Cycle Management • Patient Access • Prior Authorization • Denial Prevention • Health Informatics • Workflow Loss Control Method</div></div>', unsafe_allow_html=True)

with tabs[11]:
    st.markdown('<div class="section-title">Downloadable Executive Brief</div>', unsafe_allow_html=True)
    brief = brief_text(active_cases)
    st.text_area("Executive brief preview", brief, height=420)
    st.download_button("Download executive brief", data=brief, file_name="kori_pickle_enterprise_revenue_operations_brief.txt", mime="text/plain")

st.markdown("""
<div class="footer-lockup">
    <div class="kicker">Created by Kori Pickle</div>
    <div class="footer-signature">Kori Pickle</div>
    <div class="section-copy" style="margin-left:auto; margin-right:auto;">Healthcare Operations Intelligence • Revenue Cycle • Patient Access • Prior Authorization • Denial Prevention</div>
    <div class="footer-links"><a href="https://www.linkedin.com/" target="_blank">LinkedIn</a><a href="https://github.com/koripickle1101-TN" target="_blank">GitHub</a></div>
</div>
""", unsafe_allow_html=True)
