import csv
from datetime import date
from io import StringIO
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Enterprise Revenue Operations Platform",
    page_icon="KP",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_b64(path):
    p = Path(path)
    if p.exists():
        return p.read_text().strip()
    return ""


BRAND_LOGO = load_b64("assets/brand_logo.b64")


def img_html(b64_data, alt, cls):
    if not b64_data:
        return f'<div class="{cls} missing-asset">Asset pending<br>{alt}</div>'
    return f'<img class="{cls}" alt="{alt}" src="data:image/jpeg;base64,{b64_data}">'


def money(value):
    return "${:,.0f}".format(value)


def today_iso():
    return date.today().isoformat()


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Inter:wght@300;400;500;600;700&display=swap');

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
    max-width: 1480px !important;
    padding-top: 2rem !important;
    padding-left: 4rem !important;
    padding-right: 4rem !important;
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
    letter-spacing: -0.035em !important;
}

[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1.5px solid var(--black) !important;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p { color: var(--black) !important; }

[data-testid="stSidebar"] label {
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
textarea,
[data-testid="stTextArea"] textarea {
    background: var(--white) !important;
    border: 1.4px solid var(--black) !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    color: var(--black) !important;
}

span[data-baseweb="tag"], [data-baseweb="tag"] {
    background: var(--white) !important;
    color: var(--black) !important;
    border: 1.3px solid var(--orange) !important;
    border-radius: 0 !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.55rem;
    border-bottom: 1.5px solid var(--black);
    padding-bottom: 0.55rem;
    overflow-x: auto;
}

.stTabs [data-baseweb="tab"] {
    background: var(--white) !important;
    border: 1.3px solid var(--black) !important;
    border-radius: 0 !important;
    padding: 0.68rem 0.95rem !important;
    font-weight: 500 !important;
}

.stTabs [aria-selected="true"] { background: var(--orange) !important; border-color: var(--orange) !important; }

button[kind="primary"], .stDownloadButton button {
    background: var(--white) !important;
    color: var(--black) !important;
    border: 1.4px solid var(--black) !important;
    border-radius: 0 !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

.brand-shell {
    border-left: 1.5px solid var(--black);
    border-right: 1.5px solid var(--black);
    padding: 2rem 2.2rem 2.6rem 2.2rem;
    margin-bottom: 2rem;
    background: var(--white);
}

.logo-img {
    width: min(760px, 100%);
    display: block;
    margin: 0 auto 1.4rem auto;
}

.profile-box {
    border: 1.4px solid var(--black);
    border-left: 7px solid var(--orange);
    padding: 1.4rem;
}

.missing-asset {
    border: 1.4px solid var(--orange);
    padding: 1rem;
    text-align: center;
    font-size: 0.78rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

.brand-rule {
    height: 7px;
    width: 100%;
    background: var(--orange);
    margin: 1rem 0 2rem 0;
}

.kicker {
    font-size: 0.7rem;
    letter-spacing: 0.34em;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 1.2rem;
}

.hero-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(320px, 0.72fr);
    gap: 2.2rem;
    align-items: stretch;
}

.hero-title {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: clamp(3.8rem, 7.2vw, 7.6rem);
    line-height: 0.86;
    letter-spacing: -0.065em;
    font-weight: 300;
    margin: 0;
}

.hero-title span {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-weight: 300;
    color: var(--orange) !important;
}

.hero-copy {
    margin-top: 1.7rem;
    max-width: 880px;
    font-size: 1.04rem;
    line-height: 1.78;
    font-weight: 400;
}

.identity-panel {
    border: 1.4px solid var(--black);
    padding: 2rem;
    min-height: 440px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.identity-statement {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: clamp(2.3rem, 4.4vw, 4.3rem);
    line-height: 0.94;
    letter-spacing: -0.045em;
    font-weight: 300;
}

.thin-orange { width: 52%; height: 2px; background: var(--orange); margin: 1.4rem 0; }

.badge {
    display: inline-block;
    border: 1.3px solid var(--black);
    border-left: 7px solid var(--orange);
    padding: 0.62rem 0.9rem;
    margin: 0.28rem 0.28rem 0.28rem 0;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    background: var(--white);
}

.metric-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1rem; margin: 1.4rem 0 2.2rem 0; }

.metric-card { border: 1.4px solid var(--black); border-left: 6px solid var(--orange); padding: 1.55rem; min-height: 162px; background: var(--white); }

.metric-label { font-size: 0.66rem; letter-spacing: 0.24em; text-transform: uppercase; font-weight: 600; margin-bottom: 0.9rem; }

.metric-value { font-family: "Cormorant Garamond", Georgia, serif !important; font-size: clamp(3.1rem, 5.1vw, 5.1rem); line-height: 0.88; letter-spacing: -0.045em; font-weight: 300; color: var(--black); }

.metric-value.orange { color: var(--orange); }

.metric-note { font-size: 0.86rem; line-height: 1.5; margin-top: 1rem; }

.section-panel { border: 1.4px solid var(--black); padding: 2rem; margin: 1.2rem 0; }

.section-title { font-family: "Cormorant Garamond", Georgia, serif !important; font-size: clamp(2.7rem, 5.4vw, 5.4rem); line-height: 0.94; letter-spacing: -0.055em; font-weight: 300; margin: 1.6rem 0 0.9rem 0; }

.editorial-note { border: 1.4px solid var(--black); border-left: 7px solid var(--orange); padding: 1.5rem; margin: 1rem 0; }

.editorial-note h3 { font-family: "Cormorant Garamond", Georgia, serif !important; font-size: 3rem; line-height: 0.95; margin: 0 0 1rem 0; font-weight: 300 !important; }

.queue-table { width: 100%; border-collapse: collapse; border: 1.4px solid var(--black); margin: 1rem 0; font-size: 0.88rem; }

.queue-table th { background: var(--white); border: 1.2px solid var(--black); padding: 0.72rem; text-align: left; font-size: 0.66rem; letter-spacing: 0.14em; text-transform: uppercase; }

.queue-table td { border: 1px solid var(--black); padding: 0.72rem; vertical-align: top; }

.score-wrap { border: 1.4px solid var(--black); padding: 2rem; margin: 1rem 0; }

.score-number { font-family: "Cormorant Garamond", Georgia, serif !important; font-size: clamp(5rem, 10vw, 9rem); font-weight: 300; line-height: 0.78; letter-spacing: -0.06em; }

.progress-track { height: 13px; border: 1.4px solid var(--black); background: var(--white); margin: 0.8rem 0 1rem 0; }
.progress-fill { height: 100%; background: var(--orange); }
.bar-row { display: grid; grid-template-columns: 140px 1fr 44px; gap: 1rem; align-items: center; margin: 1rem 0; }

.footer-brand { border-top: 3px solid var(--orange); border-bottom: 3px solid var(--orange); text-align: center; padding: 2.2rem 1rem; margin-top: 3rem; }
.footer-signature { font-family: "Cormorant Garamond", Georgia, serif !important; font-size: 4rem; font-style: italic; font-weight: 300; letter-spacing: -0.04em; line-height: 1; margin: 0.7rem 0 0.5rem 0; }
.link-button { display: inline-block; border: 1.3px solid var(--black); padding: 0.7rem 1.2rem; margin: 0.4rem; text-decoration: none !important; color: var(--black) !important; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; }

@media (max-width: 900px) {
    .block-container { padding-left: 1.35rem !important; padding-right: 1.35rem !important; }
    .brand-shell { padding: 1.4rem; }
    .hero-grid, .metric-grid { grid-template-columns: 1fr; }
    .hero-title { font-size: clamp(4.1rem, 19vw, 6.2rem); }
    .identity-panel { min-height: auto; }
    .bar-row { grid-template-columns: 105px 1fr 32px; }
}
</style>
    """,
    unsafe_allow_html=True,
)


synthetic_cases = [
    {"Case ID": "REV-0001", "Payer Group": "Commercial", "Workflow Domain": "Patient Access", "Service Line": "Orthopedics", "Risk": "High", "Owner": "Patient Access Lead", "Days Open": 7, "SLA Limit": 5, "Exposure": 18450, "Eligibility": "Verified", "Routing": "Correct", "Documentation": "Missing clinical note", "Human Review": "Required", "Status": "Needs Documentation"},
    {"Case ID": "REV-0002", "Payer Group": "Medicare Advantage", "Workflow Domain": "Authorization Control", "Service Line": "Neurology", "Risk": "High", "Owner": "Prior Authorization Lead", "Days Open": 9, "SLA Limit": 5, "Exposure": 28500, "Eligibility": "Verified", "Routing": "Unclear", "Documentation": "Missing medical necessity statement", "Human Review": "Required", "Status": "Escalate"},
    {"Case ID": "REV-0003", "Payer Group": "Medicaid", "Workflow Domain": "Documentation Readiness", "Service Line": "Rehabilitation", "Risk": "Moderate", "Owner": "Documentation Specialist", "Days Open": 4, "SLA Limit": 5, "Exposure": 9750, "Eligibility": "Pending", "Routing": "Correct", "Documentation": "Missing therapy duration", "Human Review": "Required", "Status": "Needs Eligibility Review"},
    {"Case ID": "REV-0004", "Payer Group": "Commercial", "Workflow Domain": "Routing Intelligence", "Service Line": "Cardiology", "Risk": "High", "Owner": "RCM Analyst", "Days Open": 8, "SLA Limit": 5, "Exposure": 22100, "Eligibility": "Verified", "Routing": "Incorrect portal", "Documentation": "Complete", "Human Review": "Required", "Status": "Routing Review"},
    {"Case ID": "REV-0005", "Payer Group": "Marketplace", "Workflow Domain": "Eligibility Verification", "Service Line": "Imaging", "Risk": "Moderate", "Owner": "Eligibility Specialist", "Days Open": 5, "SLA Limit": 5, "Exposure": 12600, "Eligibility": "Mismatch", "Routing": "Correct", "Documentation": "Complete", "Human Review": "Required", "Status": "Needs Eligibility Review"},
    {"Case ID": "REV-0006", "Payer Group": "Self Pay", "Workflow Domain": "Financial Clearance", "Service Line": "Surgery", "Risk": "Low", "Owner": "Financial Counselor", "Days Open": 2, "SLA Limit": 4, "Exposure": 6800, "Eligibility": "Not Applicable", "Routing": "Correct", "Documentation": "Complete", "Human Review": "Optional", "Status": "Financial Review"},
    {"Case ID": "REV-0007", "Payer Group": "Commercial", "Workflow Domain": "Denial Prevention", "Service Line": "Oncology", "Risk": "High", "Owner": "Denial Prevention Lead", "Days Open": 10, "SLA Limit": 5, "Exposure": 45200, "Eligibility": "Verified", "Routing": "Correct", "Documentation": "Missing lab evidence", "Human Review": "Required", "Status": "Pre-Denial Review"},
    {"Case ID": "REV-0008", "Payer Group": "Medicare Advantage", "Workflow Domain": "Authorization Control", "Service Line": "Imaging", "Risk": "High", "Owner": "Prior Authorization Lead", "Days Open": 6, "SLA Limit": 5, "Exposure": 14100, "Eligibility": "Verified", "Routing": "Correct", "Documentation": "Missing conservative therapy duration", "Human Review": "Required", "Status": "Needs Documentation"},
    {"Case ID": "REV-0009", "Payer Group": "Medicaid", "Workflow Domain": "Documentation Readiness", "Service Line": "Behavioral Health", "Risk": "Moderate", "Owner": "Clinical Documentation Liaison", "Days Open": 6, "SLA Limit": 5, "Exposure": 7900, "Eligibility": "Verified", "Routing": "Correct", "Documentation": "Incomplete plan of care", "Human Review": "Required", "Status": "Needs Documentation"},
    {"Case ID": "REV-0010", "Payer Group": "Commercial", "Workflow Domain": "Eligibility Verification", "Service Line": "Primary Care", "Risk": "Low", "Owner": "Patient Access Specialist", "Days Open": 1, "SLA Limit": 5, "Exposure": 3500, "Eligibility": "Verified", "Routing": "Correct", "Documentation": "Complete", "Human Review": "Optional", "Status": "Ready"},
    {"Case ID": "REV-0011", "Payer Group": "Medicare Advantage", "Workflow Domain": "Patient Access", "Service Line": "Rehabilitation", "Risk": "High", "Owner": "Access Operations Manager", "Days Open": 7, "SLA Limit": 5, "Exposure": 31800, "Eligibility": "Pending", "Routing": "Unclear", "Documentation": "Missing order signature", "Human Review": "Required", "Status": "Escalate"},
    {"Case ID": "REV-0012", "Payer Group": "Commercial", "Workflow Domain": "Routing Intelligence", "Service Line": "Neurology", "Risk": "Moderate", "Owner": "RCM Analyst", "Days Open": 5, "SLA Limit": 5, "Exposure": 11300, "Eligibility": "Verified", "Routing": "Secondary review needed", "Documentation": "Complete", "Human Review": "Required", "Status": "Routing Review"},
    {"Case ID": "REV-0013", "Payer Group": "Marketplace", "Workflow Domain": "Denial Prevention", "Service Line": "Cardiology", "Risk": "High", "Owner": "Revenue Integrity Analyst", "Days Open": 8, "SLA Limit": 5, "Exposure": 23400, "Eligibility": "Verified", "Routing": "Correct", "Documentation": "Missing prior treatment history", "Human Review": "Required", "Status": "Pre-Denial Review"},
    {"Case ID": "REV-0014", "Payer Group": "Commercial", "Workflow Domain": "Authorization Control", "Service Line": "Surgery", "Risk": "Moderate", "Owner": "Prior Authorization Coordinator", "Days Open": 3, "SLA Limit": 5, "Exposure": 12550, "Eligibility": "Verified", "Routing": "Correct", "Documentation": "Complete", "Human Review": "Required", "Status": "Ready for Submission"},
]


def load_uploaded_cases(upload):
    if upload is None:
        return synthetic_cases
    try:
        text = upload.getvalue().decode("utf-8")
        reader = csv.DictReader(StringIO(text))
        rows = []
        for row in reader:
            row["Days Open"] = int(row.get("Days Open", 0))
            row["SLA Limit"] = int(row.get("SLA Limit", 5))
            row["Exposure"] = float(row.get("Exposure", 0))
            rows.append(row)
        return rows if rows else synthetic_cases
    except Exception:
        st.warning("CSV could not be read. Returning to synthetic demo dataset.")
        return synthetic_cases


with st.sidebar:
    st.markdown("### Command Filters")
    uploaded = st.file_uploader("Synthetic CSV upload only", type=["csv"])
    cases = load_uploaded_cases(uploaded)

    risk_options = sorted({c["Risk"] for c in cases})
    payer_options = sorted({c["Payer Group"] for c in cases})
    domain_options = sorted({c["Workflow Domain"] for c in cases})
    service_options = sorted({c["Service Line"] for c in cases})

    selected_risks = st.multiselect("Filter by risk level", risk_options, default=risk_options)
    selected_payers = st.multiselect("Filter by payer group", payer_options, default=payer_options)
    selected_domains = st.multiselect("Filter by workflow area", domain_options, default=domain_options)
    selected_services = st.multiselect("Filter by service line", service_options, default=service_options)

filtered = [
    c for c in cases
    if c["Risk"] in selected_risks
    and c["Payer Group"] in selected_payers
    and c["Workflow Domain"] in selected_domains
    and c["Service Line"] in selected_services
]


def readiness_score(case):
    score = 100
    penalties = []
    if case["Eligibility"] not in ["Verified", "Not Applicable"]:
        score -= 22
        penalties.append("Eligibility requires validation")
    if case["Routing"] != "Correct":
        score -= 22
        penalties.append("Routing ownership or portal requires review")
    if case["Documentation"] != "Complete":
        score -= 26
        penalties.append(case["Documentation"])
    if int(case["Days Open"]) >= int(case["SLA Limit"]):
        score -= 15
        penalties.append("SLA pressure present")
    if case["Risk"] == "High":
        score -= 8
        penalties.append("High risk queue priority")
    return max(score, 0), penalties


def case_action(case):
    score, gaps = readiness_score(case)
    if score >= 85:
        status = "Ready with human review"
        action = "Proceed to authorization packet review before submission."
    elif score >= 65:
        status = "Conditionally ready"
        action = "Resolve listed gaps before payer submission or follow up."
    else:
        status = "Not ready"
        action = "Stabilize eligibility, routing, documentation, and escalation ownership first."
    return status, action, gaps


def filtered_stats(rows):
    total = len(rows)
    high = sum(1 for c in rows if c["Risk"] == "High")
    sla = sum(1 for c in rows if int(c["Days Open"]) >= int(c["SLA Limit"]))
    exposure = sum(float(c["Exposure"]) for c in rows)
    avg_age = sum(int(c["Days Open"]) for c in rows) / total if total else 0
    owners = len({c["Owner"] for c in rows})
    avg_score = sum(readiness_score(c)[0] for c in rows) / total if total else 0
    return total, high, sla, exposure, avg_age, owners, avg_score


total, high, sla, exposure, avg_age, owners, avg_score = filtered_stats(filtered)


def render_table(rows, columns):
    html = '<table class="queue-table"><thead><tr>'
    for col in columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"
    for row in rows:
        html += "<tr>"
        for col in columns:
            html += f"<td>{row.get(col, '')}</td>"
        html += "</tr>"
    html += "</tbody></table>"
    return html


def risk_bars(rows):
    counts = {"High": 0, "Moderate": 0, "Low": 0}
    for r in rows:
        counts[r["Risk"]] = counts.get(r["Risk"], 0) + 1
    max_val = max(counts.values()) if counts else 1
    html = '<div class="section-panel"><div class="kicker">Risk Queue Distribution</div>'
    for label in ["High", "Moderate", "Low"]:
        width = 100 * counts.get(label, 0) / max_val if max_val else 0
        html += f"""
        <div class="bar-row">
            <div>{label}</div>
            <div class="progress-track"><div class="progress-fill" style="width:{width}%"></div></div>
            <div>{counts.get(label, 0)}</div>
        </div>
        """
    html += "</div>"
    return html


def brief_text(rows):
    t, h, s, e, a, o, sc = filtered_stats(rows)
    top_domains = {}
    for r in rows:
        top_domains[r["Workflow Domain"]] = top_domains.get(r["Workflow Domain"], 0) + 1
    top_domain = max(top_domains, key=top_domains.get) if top_domains else "No active domain"
    return f"""Enterprise Revenue Operations Platform
Created by Kori Pickle

Synthetic data only. No PHI.

Active command view date: {today_iso()}
Filtered records: {t}
High risk records: {h}
SLA pressure signals: {s}
Average aging: {a:.1f} days
Simulated exposure: {money(e)}
Distinct owners: {o}
Average authorization readiness score: {sc:.0f}

Primary workflow pressure area: {top_domain}

Executive interpretation:
The active command view shows operational review signals, not automated payer or clinical decisions. The priority is to stabilize workflow ownership, missing documentation, routing accuracy, eligibility readiness, SLA pressure, and denial prevention risk before downstream revenue damage occurs.

Human review boundary:
This platform supports operational prioritization only. It does not make payer decisions, billing determinations, coding determinations, clinical decisions, or patient specific recommendations.
"""


st.markdown(
    f"""
<div class="brand-shell">
    {img_html(BRAND_LOGO, "Kori Pickle Healthcare Operations Intelligence Logo", "logo-img")}
    <div class="brand-rule"></div>
    <div class="hero-grid">
        <div>
            <div class="kicker">Kori Pickle • Healthcare Operations Intelligence</div>
            <div class="hero-title">
                Enterprise<br>
                Revenue<br>
                <span>Operations</span><br>
                Platform
            </div>
            <div class="hero-copy">
                A premium synthetic no PHI healthcare operations command center for patient access, eligibility verification,
                prior authorization pressure tracking, routing intelligence, documentation readiness, denial prevention,
                payer friction analysis, and responsible operational intelligence.
                <br><br>
                This build functions as an operational review workbench: filter synthetic cases, isolate ownership gaps,
                simulate stabilization impact, generate escalation language, and build a leadership brief from the active command view.
            </div>
            <div style="margin-top:1.1rem;">
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
            <div class="small-caps">Patient Access • Authorization Control • Documentation Readiness • Denial Prevention</div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-label">High Risk Records</div>
        <div class="metric-value orange">{high}</div>
        <div class="metric-note">Prioritized operational review queue.</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">SLA Pressure</div>
        <div class="metric-value">{sla}</div>
        <div class="metric-note">Records aged at or above SLA limit.</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Synthetic Exposure</div>
        <div class="metric-value">{money(exposure)}</div>
        <div class="metric-note">Portfolio simulation only.</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Readiness Average</div>
        <div class="metric-value">{avg_score:.0f}</div>
        <div class="metric-note">Aggregate workflow readiness score.</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

tabs = st.tabs([
    "Command Center",
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
])

with tabs[0]:
    st.markdown('<div class="section-title">Live Command Center</div>', unsafe_allow_html=True)
    st.write("Use the sidebar filters to isolate operational pressure across payer group, workflow domain, service line, and risk level.")
    st.markdown(render_table(filtered, ["Case ID", "Payer Group", "Workflow Domain", "Service Line", "Risk", "Owner", "Days Open", "Status"]), unsafe_allow_html=True)
    st.markdown(risk_bars(filtered), unsafe_allow_html=True)
    st.markdown(
        f"""
<div class="editorial-note">
    <h3>Executive Interpretation</h3>
    <p>The active view shows {total} synthetic records, {high} high risk records, {sla} SLA pressure signals,
    average aging of {avg_age:.1f} days, {owners} distinct owners, and {money(exposure)} in simulated exposure.
    These are prioritization signals for human review, not automated payer or clinical decisions.</p>
</div>
""",
        unsafe_allow_html=True,
    )

with tabs[1]:
    st.markdown('<div class="section-title">Authorization Readiness Engine</div>', unsafe_allow_html=True)
    if filtered:
        selected_case = st.selectbox("Select synthetic case for readiness review", [c["Case ID"] for c in filtered])
        c = next(row for row in filtered if row["Case ID"] == selected_case)
        score, gaps = readiness_score(c)
        status, action, gaps = case_action(c)
        st.markdown(
            f"""
<div class="score-wrap">
    <div class="kicker">Readiness Score</div>
    <div class="score-number">{score}</div>
    <div class="progress-track"><div class="progress-fill" style="width:{score}%"></div></div>
    <p><b>Status:</b> {status}</p>
    <p><b>Operational action:</b> {action}</p>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown(render_table([c], ["Case ID", "Eligibility", "Routing", "Documentation", "Human Review", "Owner"]), unsafe_allow_html=True)
        st.write("Readiness gaps:")
        for gap in gaps if gaps else ["No major readiness gaps detected. Final human review still required."]:
            st.write("• " + gap)
    else:
        st.write("No records match the active filters.")

with tabs[2]:
    st.markdown('<div class="section-title">Missing Documentation Detector</div>', unsafe_allow_html=True)
    docs = [c for c in filtered if c["Documentation"] != "Complete"]
    st.markdown(render_table(docs, ["Case ID", "Payer Group", "Service Line", "Documentation", "Owner", "Status"]), unsafe_allow_html=True)
    st.markdown("""<div class="editorial-note"><h3>Detector Logic</h3><p>The detector isolates records where the authorization packet is not submission ready. The goal is to prevent a weak packet from becoming a delay, denial, avoidable follow up, or patient access friction point.</p></div>""", unsafe_allow_html=True)

with tabs[3]:
    st.markdown('<div class="section-title">Payer Rule Lab</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        lab_payer = st.selectbox("Payer group", payer_options)
        lab_service = st.selectbox("Service line", service_options)
    with col2:
        eligibility_ready = st.selectbox("Eligibility status", ["Verified", "Pending", "Mismatch"])
        routing_ready = st.selectbox("Routing status", ["Correct", "Unclear", "Incorrect portal"])
    with col3:
        documentation_ready = st.selectbox("Documentation status", ["Complete", "Missing clinical note", "Missing medical necessity statement", "Missing therapy duration", "Missing prior treatment history"])
        days_pending = st.number_input("Days pending", min_value=0, max_value=30, value=5, step=1)

    lab_case = {"Case ID": "LAB-0001", "Payer Group": lab_payer, "Workflow Domain": "Payer Rule Lab", "Service Line": lab_service, "Risk": "High" if days_pending >= 6 or documentation_ready != "Complete" else "Moderate", "Owner": "Human Reviewer", "Days Open": int(days_pending), "SLA Limit": 5, "Exposure": 0, "Eligibility": eligibility_ready, "Routing": routing_ready, "Documentation": documentation_ready, "Human Review": "Required", "Status": "Simulation"}
    score, gaps = readiness_score(lab_case)
    status, action, gaps = case_action(lab_case)
    st.markdown(f"""<div class="editorial-note"><h3>{status}</h3><p><b>Simulated readiness score:</b> {score}</p><p><b>Recommended operational move:</b> {action}</p><p><b>Decision boundary:</b> This simulation does not approve, deny, code, bill, or clinically determine care. It supports workflow review only.</p></div>""", unsafe_allow_html=True)
    for gap in gaps:
        st.write("• " + gap)

with tabs[4]:
    st.markdown('<div class="section-title">SLA Breach Countdown</div>', unsafe_allow_html=True)
    countdown_rows = []
    for c in filtered:
        remaining = int(c["SLA Limit"]) - int(c["Days Open"])
        breach = "Breached" if remaining <= 0 else f"{remaining} days remaining"
        row = dict(c)
        row["SLA Countdown"] = breach
        countdown_rows.append(row)
    st.markdown(render_table(countdown_rows, ["Case ID", "Owner", "Days Open", "SLA Limit", "SLA Countdown", "Status"]), unsafe_allow_html=True)

with tabs[5]:
    st.markdown('<div class="section-title">Operational Work Queue</div>', unsafe_allow_html=True)
    st.write("This queue translates dashboard signals into operational work. It shows what needs attention, who owns it, what is missing, and what action should happen next.")
    queue_rows = []
    for c in filtered:
        status, action, gaps = case_action(c)
        row = dict(c)
        row["Next Action"] = action
        queue_rows.append(row)
    st.markdown(render_table(queue_rows, ["Case ID", "Risk", "Owner", "Status", "Next Action"]), unsafe_allow_html=True)

with tabs[6]:
    st.markdown('<div class="section-title">Audit Trail and Human Review Log</div>', unsafe_allow_html=True)
    audit_rows = []
    for c in filtered:
        status, action, gaps = case_action(c)
        audit_rows.append({"Timestamp": today_iso(), "Case ID": c["Case ID"], "Reviewer": c["Owner"], "Review Signal": status, "Reason": "; ".join(gaps[:2]) if gaps else "Final human review before submission", "Boundary": "No automated clinical or payer decision"})
    st.markdown(render_table(audit_rows, ["Timestamp", "Case ID", "Reviewer", "Review Signal", "Reason", "Boundary"]), unsafe_allow_html=True)

with tabs[7]:
    st.markdown('<div class="section-title">Before and After Stabilization Simulator</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        record_volume = st.number_input("Monthly front end records", min_value=100, max_value=100000, value=15000, step=500)
    with col2:
        current_friction = st.slider("Current workflow friction rate", min_value=1, max_value=30, value=12, step=1)
    with col3:
        stabilization_capture = st.slider("Stabilization capture rate", min_value=10, max_value=95, value=72, step=1)

    current_pressure = record_volume * current_friction / 100
    stabilized = current_pressure * stabilization_capture / 100
    remaining = current_pressure - stabilized
    st.markdown(f"""<div class="metric-grid"><div class="metric-card"><div class="metric-label">Current Pressure</div><div class="metric-value">{current_pressure:.0f}</div><div class="metric-note">Monthly records with workflow friction.</div></div><div class="metric-card"><div class="metric-label">Stabilized Records</div><div class="metric-value orange">{stabilized:.0f}</div><div class="metric-note">Estimated records improved through workflow controls.</div></div><div class="metric-card"><div class="metric-label">Remaining Friction</div><div class="metric-value">{remaining:.0f}</div><div class="metric-note">Residual pressure requiring human review.</div></div><div class="metric-card"><div class="metric-label">Capture Rate</div><div class="metric-value">{stabilization_capture}</div><div class="metric-note">Synthetic operational assumption.</div></div></div>""", unsafe_allow_html=True)

with tabs[8]:
    st.markdown('<div class="section-title">2027 API Readiness Checklist</div>', unsafe_allow_html=True)
    checklist = ["Prior authorization status visibility is available to operational users", "Documentation requirements are structured before submission", "Routing ownership is clearly assigned", "Payer follow up is tracked by SLA threshold", "Human review is separated from automation support", "No PHI is stored in this public portfolio environment", "Leadership brief can be generated from the active work queue", "Synthetic CSV upload can simulate operational datasets"]
    completed = 0
    for item in checklist:
        if st.checkbox(item, value=True):
            completed += 1
    score = int(completed / len(checklist) * 100)
    st.markdown(f"""<div class="score-wrap"><div class="kicker">Operational API Readiness Posture</div><div class="score-number">{score}</div><div class="progress-track"><div class="progress-fill" style="width:{score}%"></div></div><p>This checklist demonstrates operational readiness thinking. It does not represent live payer connectivity or production API certification.</p></div>""", unsafe_allow_html=True)

with tabs[9]:
    st.markdown('<div class="section-title">About Kori Pickle</div>', unsafe_allow_html=True)
    st.markdown("""<div class="profile-box"><div class="kicker">Patient to Professional Healthcare Operations Perspective</div><p>Kori Pickle is a University of Phoenix BSHA candidate focused on healthcare operations, revenue cycle management, patient access, prior authorization, denial prevention, workflow intelligence, and health informatics.</p><p>Her work focuses on turning lived patient experience and healthcare administration coursework into practical, remote-ready operational tools that show visibility, workflow discipline, documentation readiness, and responsible human review.</p><span class="badge">99 of 120 Credits</span><span class="badge">GPA 3.6</span><span class="badge">Healthcare Operations</span><span class="badge">Revenue Cycle</span></div>""", unsafe_allow_html=True)
    resume_download = """Kori Pickle
Healthcare Operations | Revenue Cycle Management | Patient Access | Prior Authorization | Health Informatics

Professional Summary
BSHA candidate with a patient to professional perspective and a focused interest in healthcare operations, revenue cycle workflow, denial prevention, prior authorization readiness, patient access operations, health informatics, workflow visibility, and responsible operational intelligence.

Education
Bachelor of Science in Healthcare Administration Candidate
University of Phoenix
99 of 120 credits completed
GPA 3.6

Core Competencies
Revenue Cycle Management
Patient Access Operations
Prior Authorization Workflow
Eligibility Verification
Documentation Readiness
Denial Prevention
Workflow Intelligence
Health Informatics
Operational Reporting
Quality Improvement
Human Review Governance

Portfolio Focus
Synthetic no PHI healthcare operations tools that demonstrate workflow visibility, authorization readiness, payer friction analysis, operational escalation, leadership briefing, and responsible decision support boundaries.
"""
    st.download_button("Download resume text", resume_download, file_name="Kori_Pickle_Healthcare_Operations_Resume.txt")

with tabs[10]:
    st.markdown('<div class="section-title">Downloadable Leadership Brief</div>', unsafe_allow_html=True)
    brief = brief_text(filtered)
    st.text_area("Executive brief generated from active command view", brief, height=330)
    st.download_button("Download executive brief", brief, file_name="kori_pickle_enterprise_rev_ops_brief.txt")
    st.markdown("""<div class="editorial-note"><h3>Synthetic Data Boundary</h3><p>This platform demonstrates healthcare operations logic using synthetic data only. It is designed for workflow intelligence, revenue cycle visibility, prior authorization readiness, and responsible human-review processes. It does not use, request, store, process, or display real PHI.</p></div>""", unsafe_allow_html=True)

st.markdown(
    f"""
<div class="footer-brand">
    {img_html(BRAND_LOGO, "Kori Pickle Healthcare Operations Intelligence Logo", "logo-img")}
    <div class="kicker">Created by Kori Pickle</div>
    <div class="footer-signature">Kori Pickle</div>
    <p>Healthcare Operations Intelligence • Revenue Cycle • Patient Access • Prior Authorization • Denial Prevention</p>
    <a class="link-button" href="https://www.linkedin.com/" target="_blank">LinkedIn</a>
    <a class="link-button" href="https://github.com/koripickle1101-TN" target="_blank">GitHub</a>
</div>
""",
    unsafe_allow_html=True,
)
