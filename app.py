from datetime import date
from io import StringIO
import csv
import streamlit as st

st.set_page_config(
    page_title="Enterprise Revenue Operations Platform",
    page_icon="KP",
    layout="wide",
    initial_sidebar_state="expanded",
)

ORANGE = "rgb(255, 130, 0)"
BLACK = "rgb(0, 0, 0)"
WHITE = "rgb(255, 255, 255)"

def money(value):
    return "${:,.0f}".format(value)

def pct(value):
    return "{}%".format(int(round(value)))

def html_escape(value):
    text = str(value)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )

synthetic_cases = [
    {
        "Case ID": "REV-0001",
        "Payer Group": "Commercial",
        "Workflow Domain": "Patient Access",
        "Service Line": "Orthopedics",
        "Risk": "High",
        "Owner": "Patient Access Lead",
        "Days Open": 7,
        "SLA Limit": 5,
        "Exposure": 18450,
        "Status": "Needs Documentation",
        "Required Docs": ["order", "insurance card", "clinical note", "medical necessity note"],
        "Present Docs": ["order", "insurance card"],
        "Next Action": "Validate documentation packet and assign same day authorization follow up.",
        "First Control Loss": "Documentation Control",
    },
    {
        "Case ID": "REV-0002",
        "Payer Group": "Medicare Advantage",
        "Workflow Domain": "Authorization Control",
        "Service Line": "Neurology",
        "Risk": "High",
        "Owner": "Prior Authorization Lead",
        "Days Open": 9,
        "SLA Limit": 5,
        "Exposure": 32700,
        "Status": "Escalate",
        "Required Docs": ["order", "neuro exam", "failed conservative therapy", "imaging rationale"],
        "Present Docs": ["order", "neuro exam"],
        "Next Action": "Escalate payer follow up and request missing medical necessity support.",
        "First Control Loss": "Authorization Readiness Control",
    },
    {
        "Case ID": "REV-0003",
        "Payer Group": "Medicaid",
        "Workflow Domain": "Documentation Readiness",
        "Service Line": "Rehabilitation",
        "Risk": "Moderate",
        "Owner": "Documentation Specialist",
        "Days Open": 4,
        "SLA Limit": 5,
        "Exposure": 12600,
        "Status": "Needs Eligibility Review",
        "Required Docs": ["plan of care", "therapy evaluation", "frequency order"],
        "Present Docs": ["plan of care", "therapy evaluation"],
        "Next Action": "Confirm therapy frequency order before submission.",
        "First Control Loss": "Documentation Control",
    },
    {
        "Case ID": "REV-0004",
        "Payer Group": "Commercial",
        "Workflow Domain": "Routing Intelligence",
        "Service Line": "Cardiology",
        "Risk": "High",
        "Owner": "RCM Analyst",
        "Days Open": 8,
        "SLA Limit": 4,
        "Exposure": 28600,
        "Status": "Routing Review",
        "Required Docs": ["referral", "cardiology note", "payer route", "procedure code"],
        "Present Docs": ["referral", "cardiology note", "procedure code"],
        "Next Action": "Correct payer route and document escalation owner.",
        "First Control Loss": "Ownership Control",
    },
    {
        "Case ID": "REV-0005",
        "Payer Group": "Marketplace",
        "Workflow Domain": "Eligibility Verification",
        "Service Line": "Imaging",
        "Risk": "Moderate",
        "Owner": "Eligibility Specialist",
        "Days Open": 5,
        "SLA Limit": 5,
        "Exposure": 11250,
        "Status": "Needs Eligibility Review",
        "Required Docs": ["eligibility response", "benefit check", "order"],
        "Present Docs": ["order"],
        "Next Action": "Complete eligibility response and benefit confirmation.",
        "First Control Loss": "Patient Access Control",
    },
    {
        "Case ID": "REV-0006",
        "Payer Group": "Self Pay",
        "Workflow Domain": "Financial Clearance",
        "Service Line": "Surgery",
        "Risk": "Low",
        "Owner": "Financial Counselor",
        "Days Open": 2,
        "SLA Limit": 5,
        "Exposure": 7200,
        "Status": "Financial Review",
        "Required Docs": ["estimate", "payment plan review"],
        "Present Docs": ["estimate"],
        "Next Action": "Complete patient financial pathway review.",
        "First Control Loss": "Patient Access Control",
    },
    {
        "Case ID": "REV-0007",
        "Payer Group": "Commercial",
        "Workflow Domain": "Denial Prevention",
        "Service Line": "Oncology",
        "Risk": "High",
        "Owner": "Denial Prevention Lead",
        "Days Open": 10,
        "SLA Limit": 5,
        "Exposure": 44200,
        "Status": "Pre Denial Review",
        "Required Docs": ["treatment plan", "medical necessity note", "prior therapy history", "payer policy match"],
        "Present Docs": ["treatment plan", "medical necessity note"],
        "Next Action": "Run pre denial review and attach policy matched documentation.",
        "First Control Loss": "Time Control",
    },
    {
        "Case ID": "REV-0008",
        "Payer Group": "Medicare Advantage",
        "Workflow Domain": "Authorization Control",
        "Service Line": "Imaging",
        "Risk": "High",
        "Owner": "Prior Authorization Lead",
        "Days Open": 6,
        "SLA Limit": 5,
        "Exposure": 19600,
        "Status": "Needs Documentation",
        "Required Docs": ["order", "clinical note", "failed therapy evidence", "imaging rationale"],
        "Present Docs": ["order", "clinical note"],
        "Next Action": "Request therapy evidence and attach imaging rationale.",
        "First Control Loss": "Authorization Readiness Control",
    },
    {
        "Case ID": "REV-0009",
        "Payer Group": "Medicaid",
        "Workflow Domain": "Documentation Readiness",
        "Service Line": "Behavioral Health",
        "Risk": "Moderate",
        "Owner": "Clinical Documentation Liaison",
        "Days Open": 6,
        "SLA Limit": 5,
        "Exposure": 9800,
        "Status": "Needs Documentation",
        "Required Docs": ["assessment", "treatment plan", "provider attestation"],
        "Present Docs": ["assessment"],
        "Next Action": "Secure treatment plan and attestation before routing.",
        "First Control Loss": "Documentation Control",
    },
    {
        "Case ID": "REV-0010",
        "Payer Group": "Commercial",
        "Workflow Domain": "Eligibility Verification",
        "Service Line": "Primary Care",
        "Risk": "Low",
        "Owner": "Patient Access Specialist",
        "Days Open": 1,
        "SLA Limit": 5,
        "Exposure": 2600,
        "Status": "Ready",
        "Required Docs": ["eligibility response", "benefit check"],
        "Present Docs": ["eligibility response", "benefit check"],
        "Next Action": "Proceed with standard review.",
        "First Control Loss": "None",
    },
    {
        "Case ID": "REV-0011",
        "Payer Group": "Medicare Advantage",
        "Workflow Domain": "Patient Access",
        "Service Line": "Rehabilitation",
        "Risk": "High",
        "Owner": "Access Operations Manager",
        "Days Open": 7,
        "SLA Limit": 5,
        "Exposure": 22300,
        "Status": "Escalate",
        "Required Docs": ["order", "eligibility response", "plan of care", "authorization pathway"],
        "Present Docs": ["order", "plan of care"],
        "Next Action": "Escalate access pathway and complete eligibility validation.",
        "First Control Loss": "Patient Access Control",
    },
    {
        "Case ID": "REV-0012",
        "Payer Group": "Commercial",
        "Workflow Domain": "Routing Intelligence",
        "Service Line": "Neurology",
        "Risk": "Moderate",
        "Owner": "RCM Analyst",
        "Days Open": 5,
        "SLA Limit": 5,
        "Exposure": 14100,
        "Status": "Routing Review",
        "Required Docs": ["payer route", "order", "clinical note"],
        "Present Docs": ["order", "clinical note"],
        "Next Action": "Confirm payer route and prevent duplicate submission.",
        "First Control Loss": "Ownership Control",
    },
    {
        "Case ID": "REV-0013",
        "Payer Group": "Marketplace",
        "Workflow Domain": "Denial Prevention",
        "Service Line": "Cardiology",
        "Risk": "High",
        "Owner": "Revenue Integrity Analyst",
        "Days Open": 8,
        "SLA Limit": 5,
        "Exposure": 24250,
        "Status": "Pre Denial Review",
        "Required Docs": ["cardiology note", "medical necessity note", "payer policy match", "procedure code"],
        "Present Docs": ["cardiology note", "procedure code"],
        "Next Action": "Attach payer policy match and medical necessity support.",
        "First Control Loss": "Documentation Control",
    },
    {
        "Case ID": "REV-0014",
        "Payer Group": "Commercial",
        "Workflow Domain": "Authorization Control",
        "Service Line": "Surgery",
        "Risk": "Moderate",
        "Owner": "Prior Authorization Coordinator",
        "Days Open": 3,
        "SLA Limit": 5,
        "Exposure": 17300,
        "Status": "Ready for Submission",
        "Required Docs": ["order", "surgical note", "procedure code", "site of service"],
        "Present Docs": ["order", "surgical note", "procedure code", "site of service"],
        "Next Action": "Submit and monitor payer response window.",
        "First Control Loss": "None",
    },
]

def missing_docs(case):
    return [doc for doc in case["Required Docs"] if doc not in case["Present Docs"]]

def readiness_score(case):
    missing_count = len(missing_docs(case))
    doc_penalty = missing_count * 14
    aging_penalty = max(0, case["Days Open"] - case["SLA Limit"]) * 8
    risk_penalty = {"Low": 0, "Moderate": 8, "High": 18}.get(case["Risk"], 0)
    return max(0, min(100, 100 - doc_penalty - aging_penalty - risk_penalty))

def workflow_loss_index(case):
    missing_count = len(missing_docs(case))
    sla_over = max(0, case["Days Open"] - case["SLA Limit"])
    base = {"Low": 10, "Moderate": 32, "High": 52}.get(case["Risk"], 20)
    score = base + missing_count * 9 + sla_over * 8
    if case["First Control Loss"] == "Ownership Control":
        score += 10
    if case["Status"] in ["Escalate", "Pre Denial Review"]:
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

def filtered_cases():
    cases = synthetic_cases
    if selected_risks:
        cases = [c for c in cases if c["Risk"] in selected_risks]
    if selected_payers:
        cases = [c for c in cases if c["Payer Group"] in selected_payers]
    if selected_domains:
        cases = [c for c in cases if c["Workflow Domain"] in selected_domains]
    if selected_lines:
        cases = [c for c in cases if c["Service Line"] in selected_lines]
    return cases

def build_table(rows, cols):
    header = "".join("<th>{}</th>".format(html_escape(col)) for col in cols)
    body = ""
    for row in rows:
        body += "<tr>"
        for col in cols:
            body += "<td>{}</td>".format(html_escape(row.get(col, "")))
        body += "</tr>"
    return '<table class="queue-table"><thead><tr>{}</tr></thead><tbody>{}</tbody></table>'.format(header, body)

def build_bar(label, value, max_value):
    width = 0 if max_value == 0 else (value / max_value) * 100
    return """
    <div class="bar-row">
        <div class="bar-label">{}</div>
        <div class="progress-track"><div class="progress-fill" style="width:{}%"></div></div>
        <div class="bar-number">{}</div>
    </div>
    """.format(html_escape(label), width, html_escape(value))

def build_brief(rows):
    total = len(rows)
    high = sum(1 for c in rows if c["Risk"] == "High")
    sla = sum(1 for c in rows if c["Days Open"] >= c["SLA Limit"])
    exposure = sum(c["Exposure"] for c in rows)
    avg_ready = round(sum(readiness_score(c) for c in rows) / total, 1) if total else 0
    control_loss = sum(1 for c in rows if workflow_loss_index(c) >= 51)
    owners = len(set(c["Owner"] for c in rows))
    return f"""Enterprise Revenue Operations Platform
Leadership Brief
Generated {date.today().isoformat()}

Synthetic Data Notice
This brief uses synthetic records only. It does not contain PHI and does not make payer, clinical, billing, coding, or patient specific decisions.

Active View
Total synthetic records: {total}
High risk records: {high}
SLA pressure signals: {sla}
Distinct owners: {owners}
Average readiness score: {avg_ready}
Workflow loss cases: {control_loss}
Simulated exposure: {money(exposure)}

Kori Pickle Workflow Loss Control Method
The active review queue should be interpreted through the question: where did the workflow first lose control?

Priority Actions
1. Stabilize records with missing documentation before payer submission.
2. Escalate records at or beyond SLA limit to the assigned operational owner.
3. Validate payer rule requirements before resubmission or appeal work begins.
4. Document every human review action in the audit log.
5. Use the readiness score and workflow loss label as prioritization signals only.

Human Review Boundary
This platform supports operational visibility and workflow intelligence. It does not automate medical necessity, payer approval, claim coding, billing determinations, or clinical judgment.
"""

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --orange: rgb(255, 130, 0);
    --black: rgb(0, 0, 0);
    --white: rgb(255, 255, 255);
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"] {
    background: var(--white) !important;
    color: var(--black) !important;
}

[data-testid="stDecoration"] { background: var(--orange) !important; }

.block-container {
    max-width: 1420px !important;
    padding-top: 2.2rem !important;
    padding-left: 3.2rem !important;
    padding-right: 3.2rem !important;
    padding-bottom: 5rem !important;
}

p, div, span, label, input, textarea, button, select {
    font-family: Inter, Arial, sans-serif !important;
    color: var(--black) !important;
}

h1, h2, h3 {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    color: var(--black) !important;
    font-weight: 300 !important;
    letter-spacing: -0.045em !important;
}

[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1.2px solid var(--black) !important;
}

[data-testid="stSidebar"] label {
    font-size: 0.64rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
textarea,
[data-testid="stTextArea"] textarea {
    background: var(--white) !important;
    border: 1px solid var(--black) !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    color: var(--black) !important;
}

span[data-baseweb="tag"], [data-baseweb="tag"] {
    background: var(--white) !important;
    color: var(--black) !important;
    border: 1px solid var(--orange) !important;
    border-radius: 0 !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.6rem;
    border-bottom: 1px solid var(--black);
    padding-bottom: 0.6rem;
    overflow-x: auto;
}

.stTabs [data-baseweb="tab"] {
    background: var(--white) !important;
    border: 1px solid var(--black) !important;
    border-radius: 0 !important;
    padding: 0.68rem 0.95rem !important;
    font-weight: 400 !important;
}

.stTabs [aria-selected="true"] {
    background: var(--orange) !important;
    border-color: var(--orange) !important;
}

button, .stDownloadButton button {
    background: var(--white) !important;
    color: var(--black) !important;
    border: 1px solid var(--black) !important;
    border-radius: 0 !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

.brand-shell {
    border-left: 1.2px solid var(--black);
    border-right: 1.2px solid var(--black);
    padding: 2rem 2.2rem 2.6rem 2.2rem;
    margin-bottom: 2rem;
    background: var(--white);
}

.brand-mark {
    display: grid;
    grid-template-columns: 1fr;
    gap: 0.35rem;
    max-width: 900px;
    margin-bottom: 1.4rem;
}

.brand-signature {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: clamp(3.1rem, 7vw, 6.3rem);
    font-style: italic;
    font-weight: 300 !important;
    letter-spacing: -0.06em;
    line-height: 0.86;
}

.brand-submark {
    font-size: clamp(0.68rem, 1.3vw, 0.88rem);
    letter-spacing: 0.42em;
    text-transform: uppercase;
    font-weight: 500;
}

.brand-intel {
    color: var(--orange) !important;
    letter-spacing: 0.48em;
}

.brand-rule {
    height: 4px;
    width: 100%;
    background: var(--orange);
    margin: 1.2rem 0 2.2rem 0;
}

.kicker {
    font-size: 0.68rem;
    letter-spacing: 0.34em;
    text-transform: uppercase;
    font-weight: 500;
    margin-bottom: 1.2rem;
}

.hero-grid {
    display: grid;
    grid-template-columns: minmax(0, 0.92fr) minmax(320px, 0.7fr);
    gap: 2rem;
    align-items: stretch;
}

.hero-title {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: clamp(3.9rem, 7vw, 7.3rem);
    line-height: 0.88;
    letter-spacing: -0.065em;
    font-weight: 300 !important;
    margin: 0;
}

.hero-title span {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-weight: 300 !important;
    color: var(--orange) !important;
}

.hero-copy {
    margin-top: 1.7rem;
    max-width: 840px;
    font-size: 1.03rem;
    line-height: 1.76;
    font-weight: 400;
}

.identity-panel {
    border: 1px solid var(--black);
    padding: 2rem;
    min-height: 420px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.identity-statement {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: clamp(2.35rem, 4.4vw, 4.2rem);
    line-height: 0.94;
    letter-spacing: -0.045em;
    font-weight: 300;
}

.thin-orange { width: 52%; height: 2px; background: var(--orange); margin: 1.4rem 0; }

.badge {
    display: inline-block;
    border: 1px solid var(--black);
    border-left: 6px solid var(--orange);
    padding: 0.62rem 0.9rem;
    margin: 0.28rem 0.28rem 0.28rem 0;
    font-size: 0.66rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    background: var(--white);
}

.metric-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1rem; margin: 1.4rem 0 2.2rem 0; }

.metric-card {
    border: 1px solid var(--black);
    border-left: 5px solid var(--orange);
    padding: 1.55rem;
    min-height: 162px;
    background: var(--white);
}

.metric-label {
    font-size: 0.64rem;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    font-weight: 500;
    margin-bottom: 1rem;
}

.metric-value {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: clamp(3.2rem, 5.3vw, 5.4rem);
    line-height: 0.88;
    letter-spacing: -0.055em;
    font-weight: 300 !important;
    color: var(--black);
}

.metric-note { font-size: 0.84rem; line-height: 1.5; margin-top: 1rem; }

.section-panel { border: 1px solid var(--black); padding: 2rem; margin: 1.2rem 0; }

.section-title {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: clamp(2.8rem, 5.4vw, 5.5rem);
    line-height: 0.94;
    letter-spacing: -0.055em;
    font-weight: 300 !important;
    margin: 1.3rem 0 0.9rem 0;
}

.editorial-note {
    border: 1px solid var(--black);
    border-left: 5px solid var(--orange);
    padding: 1.5rem;
    margin: 1rem 0;
}

.editorial-note h3 {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: clamp(2.2rem, 4.4vw, 3.7rem);
    line-height: 0.95;
    margin: 0 0 1rem 0;
    font-weight: 300 !important;
}

.queue-table {
    width: 100%;
    border-collapse: collapse;
    border: 1px solid var(--black);
    margin: 1rem 0;
    font-size: 0.86rem;
}

.queue-table th {
    background: var(--white);
    border: 1px solid var(--black);
    padding: 0.72rem;
    text-align: left;
    font-size: 0.62rem;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    font-weight: 500;
}

.queue-table td {
    border: 1px solid var(--black);
    padding: 0.72rem;
    vertical-align: top;
}

.score-wrap { border: 1px solid var(--black); padding: 2rem; margin: 1rem 0; }
.score-number {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: clamp(5rem, 10vw, 9rem);
    font-weight: 300 !important;
    line-height: 0.78;
    letter-spacing: -0.07em;
}
.progress-track { height: 12px; border: 1px solid var(--black); background: var(--white); margin: 0.8rem 0 1rem 0; }
.progress-fill { height: 100%; background: var(--orange); }
.bar-row { display: grid; grid-template-columns: 130px 1fr 44px; gap: 1rem; align-items: center; margin: 1rem 0; }
.bar-label, .bar-number { font-weight: 400; }
.footer-brand { border-top: 3px solid var(--orange); border-bottom: 3px solid var(--orange); text-align: center; padding: 2.2rem 1rem; margin-top: 3rem; }
.footer-signature { font-family: "Cormorant Garamond", Georgia, serif !important; font-size: 4rem; font-style: italic; font-weight: 300 !important; letter-spacing: -0.04em; line-height: 1; margin: 0.7rem 0 0.5rem 0; }
.link-button { display: inline-block; border: 1px solid var(--black); padding: 0.7rem 1.2rem; margin: 0.4rem; text-decoration: none !important; color: var(--black) !important; font-size: 0.72rem; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; }

@media (max-width: 900px) {
    .block-container { padding-left: 1.35rem !important; padding-right: 1.35rem !important; }
    .brand-shell { padding: 1.4rem; }
    .hero-grid, .metric-grid { grid-template-columns: 1fr; }
    .hero-title { font-size: clamp(4.2rem, 18vw, 6.2rem); }
    .identity-panel { min-height: auto; }
    .bar-row { grid-template-columns: 100px 1fr 32px; }
}
</style>
    """,
    unsafe_allow_html=True,
)

risk_options = sorted(set(c["Risk"] for c in synthetic_cases), key=["High", "Moderate", "Low"].index)
payer_options = sorted(set(c["Payer Group"] for c in synthetic_cases))
domain_options = sorted(set(c["Workflow Domain"] for c in synthetic_cases))
line_options = sorted(set(c["Service Line"] for c in synthetic_cases))

st.sidebar.markdown("### Command Filters")
st.sidebar.caption("Synthetic CSV upload only. Do not upload PHI.")
uploaded = st.sidebar.file_uploader("Synthetic CSV upload option", type=["csv"])
selected_risks = st.sidebar.multiselect("Filter by risk level", risk_options, default=risk_options)
selected_payers = st.sidebar.multiselect("Filter by payer group", payer_options, default=payer_options)
selected_domains = st.sidebar.multiselect("Filter by workflow area", domain_options, default=domain_options)
selected_lines = st.sidebar.multiselect("Filter by service line", line_options, default=line_options)

cases = filtered_cases()
if uploaded is not None:
    st.sidebar.warning("CSV upload received. For portfolio safety, this app continues to display the built in synthetic dataset unless the file has been confirmed to contain no PHI.")

total_cases = len(cases)
high_count = sum(1 for c in cases if c["Risk"] == "High")
sla_count = sum(1 for c in cases if c["Days Open"] >= c["SLA Limit"])
exposure_total = sum(c["Exposure"] for c in cases)
avg_ready = round(sum(readiness_score(c) for c in cases) / total_cases, 1) if total_cases else 0
avg_aging = round(sum(c["Days Open"] for c in cases) / total_cases, 1) if total_cases else 0
owners = len(set(c["Owner"] for c in cases))

st.markdown(
    """
<div class="brand-shell">
    <div class="brand-mark">
        <div class="brand-signature">Kori Pickle</div>
        <div class="brand-submark">Healthcare Operations</div>
        <div class="brand-submark brand-intel">Intelligence</div>
    </div>
    <div class="brand-rule"></div>
    <div class="hero-grid">
        <div>
            <div class="kicker">Kori Pickle • Healthcare Operations Intelligence</div>
            <h1 class="hero-title">Enterprise<br>Revenue<br><span>Operations</span><br>Platform</h1>
            <div class="hero-copy">
                A premium synthetic no PHI healthcare operations command center for patient access, eligibility verification,
                prior authorization pressure tracking, routing intelligence, documentation readiness, denial prevention,
                payer friction analysis, and responsible operational intelligence.
                <br><br>
                This build functions as an operational review workbench: filter synthetic cases, isolate ownership gaps,
                simulate stabilization impact, generate escalation language, and build a leadership brief from the active command view.
            </div>
            <div style="margin-top:1.6rem;">
                <span class="badge">No PHI</span>
                <span class="badge">Synthetic Data</span>
                <span class="badge">Human Review Required</span>
                <span class="badge">Built by Kori Pickle</span>
            </div>
        </div>
        <div class="identity-panel">
            <div>
                <div class="kicker">Operational Identity</div>
                <div class="identity-statement">Workflow visibility before revenue damage.</div>
                <div class="thin-orange"></div>
                <p>Designed around one question: where did the workflow first lose control?</p>
            </div>
            <div class="kicker">Patient Access • Authorization Control • Documentation Readiness • Denial Prevention</div>
        </div>
    </div>
</div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-label">High Risk Records</div>
        <div class="metric-value">""" + str(high_count) + """</div>
        <div class="metric-note">Prioritized operational review queue.</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">SLA Pressure</div>
        <div class="metric-value">""" + str(sla_count) + """</div>
        <div class="metric-note">Records aged at or above SLA limit.</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Synthetic Exposure</div>
        <div class="metric-value">""" + money(exposure_total) + """</div>
        <div class="metric-note">Portfolio simulation only.</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Readiness Average</div>
        <div class="metric-value">""" + str(avg_ready) + """</div>
        <div class="metric-note">Aggregate workflow readiness score.</div>
    </div>
</div>
    """,
    unsafe_allow_html=True,
)

tabs = st.tabs(
    [
        "Command Center",
        "Workflow Loss Method",
        "Readiness Engine",
        "Documentation Detector",
        "Payer Rule Lab",
        "SLA Countdown",
        "Work Queue",
        "Audit Log",
        "Stabilization Simulator",
        "2027 API Checklist",
        "About Kori",
        "Brief Builder",
    ]
)

with tabs[0]:
    st.markdown('<div class="section-title">Live Command Center</div>', unsafe_allow_html=True)
    st.write("Use the sidebar filters to isolate operational pressure across payer group, workflow domain, service line, and risk level.")
    table_rows = []
    for c in cases:
        row = {
            "Case ID": c["Case ID"],
            "Payer Group": c["Payer Group"],
            "Workflow Domain": c["Workflow Domain"],
            "Service Line": c["Service Line"],
            "Risk": c["Risk"],
            "Owner": c["Owner"],
            "Days Open": c["Days Open"],
            "Status": c["Status"],
        }
        table_rows.append(row)
    st.markdown(build_table(table_rows, ["Case ID", "Payer Group", "Workflow Domain", "Service Line", "Risk", "Owner", "Days Open", "Status"]), unsafe_allow_html=True)
    risk_counts = {risk: sum(1 for c in cases if c["Risk"] == risk) for risk in risk_options}
    max_risk = max(risk_counts.values()) if risk_counts else 1
    bars = "".join(build_bar(risk, risk_counts[risk], max_risk) for risk in risk_options)
    st.markdown('<div class="section-panel"><div class="kicker">Risk Queue Distribution</div>{}</div>'.format(bars), unsafe_allow_html=True)
    st.markdown(
        '<div class="editorial-note"><h3>Executive Interpretation</h3><p>The active view shows {} synthetic records, {} high risk records, {} SLA pressure signals, average aging of {} days, {} distinct owners, and {} in simulated exposure. These are prioritization signals for human review, not automated payer or clinical decisions.</p></div>'.format(
            total_cases, high_count, sla_count, avg_aging, owners, money(exposure_total)
        ),
        unsafe_allow_html=True,
    )

with tabs[1]:
    st.markdown('<div class="section-title">Kori Pickle Workflow Loss Control Method</div>', unsafe_allow_html=True)
    st.write("This is the proprietary operating method behind the platform. It identifies where the workflow first lost control before the issue becomes revenue damage, denial risk, staff burden, or patient access delay.")
    col_a, col_b = st.columns([0.9, 1.1])
    with col_a:
        method_case_id = st.selectbox("Select synthetic case for control review", [c["Case ID"] for c in cases] if cases else ["No active records"])
        selected_case = next((c for c in cases if c["Case ID"] == method_case_id), None)
    with col_b:
        if selected_case:
            score = workflow_loss_index(selected_case)
            st.markdown(
                '<div class="score-wrap"><div class="kicker">Workflow Loss Index</div><div class="score-number">{}</div><p>{}</p><div class="progress-track"><div class="progress-fill" style="width:{}%"></div></div></div>'.format(
                    score, loss_label(score), score
                ),
                unsafe_allow_html=True,
            )
    if selected_case:
        controls = [
            ("Patient Access Control", "Front end access, eligibility, financial clearance, and routing readiness."),
            ("Authorization Readiness Control", "Payer path, service line context, medical necessity support, and follow up ownership."),
            ("Documentation Control", "Evidence required for timely review, routing, and payer communication."),
            ("Ownership Control", "Clear operational owner for next action, escalation, and resolution pathway."),
            ("Time Control", "Aging, SLA exposure, and turnaround pressure."),
        ]
        st.markdown('<div class="section-panel"><div class="kicker">First Control Loss</div><div class="section-title">{}</div><p>{}</p></div>'.format(html_escape(selected_case["First Control Loss"]), html_escape(selected_case["Next Action"])), unsafe_allow_html=True)
        control_html = "".join('<div class="badge">{}</div>'.format(html_escape(item[0])) for item in controls)
        st.markdown('<div class="section-panel"><div class="kicker">Five Control Domains</div>{}</div>'.format(control_html), unsafe_allow_html=True)

with tabs[2]:
    st.markdown('<div class="section-title">Authorization Readiness Engine</div>', unsafe_allow_html=True)
    readiness_rows = []
    for c in cases:
        score = readiness_score(c)
        readiness_rows.append({
            "Case ID": c["Case ID"],
            "Readiness": score,
            "Workflow Loss": workflow_loss_index(c),
            "Label": loss_label(workflow_loss_index(c)),
            "Missing Items": ", ".join(missing_docs(c)) if missing_docs(c) else "None",
            "Next Action": c["Next Action"],
        })
    st.markdown(build_table(readiness_rows, ["Case ID", "Readiness", "Workflow Loss", "Label", "Missing Items", "Next Action"]), unsafe_allow_html=True)

with tabs[3]:
    st.markdown('<div class="section-title">Missing Documentation Detector</div>', unsafe_allow_html=True)
    detector_rows = []
    for c in cases:
        detector_rows.append({
            "Case ID": c["Case ID"],
            "Required Documentation": ", ".join(c["Required Docs"]),
            "Present Documentation": ", ".join(c["Present Docs"]),
            "Missing Documentation": ", ".join(missing_docs(c)) if missing_docs(c) else "None",
            "Readiness": readiness_score(c),
        })
    st.markdown(build_table(detector_rows, ["Case ID", "Required Documentation", "Present Documentation", "Missing Documentation", "Readiness"]), unsafe_allow_html=True)

with tabs[4]:
    st.markdown('<div class="section-title">Payer Rule Lab</div>', unsafe_allow_html=True)
    payer = st.selectbox("Choose payer group", payer_options)
    domain = st.selectbox("Choose workflow domain", domain_options)
    rule_text = {
        "Commercial": "Validate plan rules, benefit limitations, authorization pathway, clinical documentation requirements, and payer portal route before submission.",
        "Medicare Advantage": "Confirm medical necessity support, prior therapy evidence, site of service expectations, payer specific authorization window, and appeal pathway.",
        "Medicaid": "Confirm eligibility status, referral requirements, covered service rules, documentation completeness, and state specific timing expectations.",
        "Marketplace": "Verify active coverage, deductible and benefit status, network rules, authorization pathway, and clinical packet readiness.",
        "Self Pay": "Complete estimate review, financial counseling pathway, payment plan documentation, and patient communication record.",
    }
    st.markdown('<div class="editorial-note"><h3>{}</h3><p>{}</p><p><b>Applied domain:</b> {}</p></div>'.format(html_escape(payer), html_escape(rule_text[payer]), html_escape(domain)), unsafe_allow_html=True)

with tabs[5]:
    st.markdown('<div class="section-title">SLA Breach Countdown</div>', unsafe_allow_html=True)
    sla_rows = []
    for c in cases:
        remaining = c["SLA Limit"] - c["Days Open"]
        if remaining < 0:
            countdown = "{} days overdue".format(abs(remaining))
        elif remaining == 0:
            countdown = "Due today"
        else:
            countdown = "{} days remaining".format(remaining)
        sla_rows.append({
            "Case ID": c["Case ID"],
            "Owner": c["Owner"],
            "Days Open": c["Days Open"],
            "SLA Limit": c["SLA Limit"],
            "Countdown": countdown,
            "Status": c["Status"],
        })
    st.markdown(build_table(sla_rows, ["Case ID", "Owner", "Days Open", "SLA Limit", "Countdown", "Status"]), unsafe_allow_html=True)

with tabs[6]:
    st.markdown('<div class="section-title">Operational Work Queue</div>', unsafe_allow_html=True)
    queue = sorted(cases, key=lambda c: workflow_loss_index(c), reverse=True)
    work_rows = []
    for c in queue:
        work_rows.append({
            "Rank": len(work_rows) + 1,
            "Case ID": c["Case ID"],
            "Owner": c["Owner"],
            "Workflow Loss": workflow_loss_index(c),
            "Control Label": loss_label(workflow_loss_index(c)),
            "Next Action": c["Next Action"],
        })
    st.markdown(build_table(work_rows, ["Rank", "Case ID", "Owner", "Workflow Loss", "Control Label", "Next Action"]), unsafe_allow_html=True)

with tabs[7]:
    st.markdown('<div class="section-title">Audit Trail and Human Review Log</div>', unsafe_allow_html=True)
    audit_rows = []
    for c in cases:
        if workflow_loss_index(c) >= 51:
            audit_rows.append({
                "Date": date.today().isoformat(),
                "Case ID": c["Case ID"],
                "Reviewer Role": c["Owner"],
                "Review Type": "Human operational review",
                "Audit Note": "Reviewed synthetic case for workflow loss, missing documentation, SLA pressure, and ownership clarity.",
            })
    if audit_rows:
        st.markdown(build_table(audit_rows, ["Date", "Case ID", "Reviewer Role", "Review Type", "Audit Note"]), unsafe_allow_html=True)
    else:
        st.info("No control loss cases in the active synthetic view.")

with tabs[8]:
    st.markdown('<div class="section-title">Before and After Stabilization Simulator</div>', unsafe_allow_html=True)
    doc_capture = st.slider("Documentation completion improvement", 0, 40, 18)
    routing_gain = st.slider("Routing accuracy improvement", 0, 40, 12)
    follow_up_gain = st.slider("Payer follow up reliability improvement", 0, 40, 10)
    improvement_factor = min(0.65, (doc_capture + routing_gain + follow_up_gain) / 160)
    stabilized_exposure = exposure_total * improvement_factor
    new_pressure = max(0, int(round(sla_count * (1 - improvement_factor))))
    st.markdown(
        """
<div class="metric-grid">
    <div class="metric-card"><div class="metric-label">Current Simulated Exposure</div><div class="metric-value">""" + money(exposure_total) + """</div></div>
    <div class="metric-card"><div class="metric-label">Potential Stabilized Exposure</div><div class="metric-value">""" + money(stabilized_exposure) + """</div></div>
    <div class="metric-card"><div class="metric-label">Current SLA Signals</div><div class="metric-value">""" + str(sla_count) + """</div></div>
    <div class="metric-card"><div class="metric-label">Post Stabilization SLA Signals</div><div class="metric-value">""" + str(new_pressure) + """</div></div>
</div>
        """,
        unsafe_allow_html=True,
    )

with tabs[9]:
    st.markdown('<div class="section-title">2027 API Readiness Checklist</div>', unsafe_allow_html=True)
    checklist = [
        "Synthetic data separation is documented",
        "No PHI is uploaded or stored",
        "Human review boundary is visible",
        "Audit log captures reviewer role and action",
        "Payer rule logic is explainable",
        "Prior authorization readiness is separated from clinical judgment",
        "FHIR aligned fields are identified for future integration",
        "CSV import is restricted to synthetic portfolio data",
    ]
    completed = 0
    for item in checklist:
        if st.checkbox(item, value=True):
            completed += 1
    readiness = int((completed / len(checklist)) * 100)
    st.markdown('<div class="score-wrap"><div class="kicker">API Readiness Position</div><div class="score-number">{}%</div><p>{} of {} controls confirmed.</p></div>'.format(readiness, completed, len(checklist)), unsafe_allow_html=True)

with tabs[10]:
    st.markdown('<div class="section-title">About Kori</div>', unsafe_allow_html=True)
    st.markdown(
        """
<div class="section-panel">
    <div class="kicker">Healthcare Operations Intelligence</div>
    <p>Kori Pickle is a BSHA candidate at the University of Phoenix with a focus on healthcare operations, revenue cycle management, patient access, prior authorization, denial prevention, health informatics, and workflow intelligence.</p>
    <p>This platform reflects a patient to professional perspective: healthcare workflows should be clear, accountable, visible, and safe before they become access barriers, rework, or downstream revenue damage.</p>
    <div class="thin-orange"></div>
    <p><b>Academic standing:</b> 99 of 120 credits completed. GPA 3.6.</p>
    <p><b>Professional focus:</b> remote healthcare administration, revenue cycle operations, patient access operations, prior authorization workflows, and responsible operational intelligence.</p>
</div>
<div class="section-panel">
    <div class="kicker">Branded Resume Snapshot</div>
    <p><b>Core strengths:</b> revenue cycle management, prior authorization workflows, eligibility verification, workflow analysis, denial prevention, patient access operations, health informatics, quality improvement, and documentation readiness.</p>
    <p><b>Portfolio position:</b> building synthetic healthcare operations tools that demonstrate workflow logic, human review boundaries, and operational stabilization methods without using PHI.</p>
</div>
        """,
        unsafe_allow_html=True,
    )

with tabs[11]:
    st.markdown('<div class="section-title">Downloadable Executive Brief Builder</div>', unsafe_allow_html=True)
    brief = build_brief(cases)
    edited_brief = st.text_area("Leadership brief", brief, height=430)
    st.download_button(
        label="Download Executive Brief",
        data=edited_brief,
        file_name="kori_pickle_enterprise_revenue_operations_brief.txt",
        mime="text/plain",
    )
    csv_buffer = StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=["Case ID", "Payer Group", "Workflow Domain", "Service Line", "Risk", "Owner", "Days Open", "Status", "Exposure"])
    writer.writeheader()
    for c in cases:
        writer.writerow({key: c[key] for key in writer.fieldnames})
    st.download_button(
        label="Download Synthetic Work Queue CSV",
        data=csv_buffer.getvalue(),
        file_name="synthetic_work_queue.csv",
        mime="text/csv",
    )

st.markdown(
    """
<div class="footer-brand">
    <div class="brand-mark" style="margin:0 auto 1rem auto;">
        <div class="brand-signature" style="font-size:4.2rem;">Kori Pickle</div>
        <div class="brand-submark">Healthcare Operations</div>
        <div class="brand-submark brand-intel">Intelligence</div>
    </div>
    <div class="kicker">Created by Kori Pickle</div>
    <p>Healthcare Operations Intelligence • Revenue Cycle • Patient Access • Prior Authorization • Denial Prevention</p>
    <a class="link-button" href="https://www.linkedin.com/" target="_blank">LinkedIn</a>
    <a class="link-button" href="https://github.com/koripickle1101-TN" target="_blank">GitHub</a>
</div>
    """,
    unsafe_allow_html=True,
)
