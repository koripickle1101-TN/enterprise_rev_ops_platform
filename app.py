import csv
from datetime import date
from io import StringIO
import streamlit as st

st.set_page_config(
    page_title="Enterprise Revenue Operations Platform",
    page_icon="KP",
    layout="wide",
    initial_sidebar_state="expanded"
)

cases = [
    {"Case ID":"REV-0001","Payer Group":"Commercial","Workflow Domain":"Patient Access","Service Line":"Orthopedics","Risk":"High","Owner":"Patient Access Lead","Days Open":7,"SLA Limit":5,"Exposure":18450,"Status":"Needs Documentation","Required Docs":["order","insurance card","clinical note","medical necessity note"],"Present Docs":["order","insurance card"],"First Control Loss":"Documentation Control","Next Action":"Validate documentation packet and assign same day authorization follow up."},
    {"Case ID":"REV-0002","Payer Group":"Medicare Advantage","Workflow Domain":"Authorization Control","Service Line":"Neurology","Risk":"High","Owner":"Prior Authorization Lead","Days Open":9,"SLA Limit":5,"Exposure":32700,"Status":"Escalate","Required Docs":["order","neuro exam","failed conservative therapy","imaging rationale"],"Present Docs":["order","neuro exam"],"First Control Loss":"Authorization Readiness Control","Next Action":"Escalate payer follow up and request missing medical necessity support."},
    {"Case ID":"REV-0003","Payer Group":"Medicaid","Workflow Domain":"Documentation Readiness","Service Line":"Rehabilitation","Risk":"Moderate","Owner":"Documentation Specialist","Days Open":4,"SLA Limit":5,"Exposure":12600,"Status":"Needs Eligibility Review","Required Docs":["plan of care","therapy evaluation","frequency order"],"Present Docs":["plan of care","therapy evaluation"],"First Control Loss":"Documentation Control","Next Action":"Confirm therapy frequency order before submission."},
    {"Case ID":"REV-0004","Payer Group":"Commercial","Workflow Domain":"Routing Intelligence","Service Line":"Cardiology","Risk":"High","Owner":"RCM Analyst","Days Open":8,"SLA Limit":4,"Exposure":28600,"Status":"Routing Review","Required Docs":["referral","cardiology note","payer route","procedure code"],"Present Docs":["referral","cardiology note","procedure code"],"First Control Loss":"Ownership Control","Next Action":"Correct payer route and document escalation owner."},
    {"Case ID":"REV-0005","Payer Group":"Marketplace","Workflow Domain":"Eligibility Verification","Service Line":"Imaging","Risk":"Moderate","Owner":"Eligibility Specialist","Days Open":5,"SLA Limit":5,"Exposure":11250,"Status":"Needs Eligibility Review","Required Docs":["eligibility response","benefit check","order"],"Present Docs":["order"],"First Control Loss":"Patient Access Control","Next Action":"Complete eligibility response and benefit confirmation."},
    {"Case ID":"REV-0006","Payer Group":"Self Pay","Workflow Domain":"Financial Clearance","Service Line":"Surgery","Risk":"Low","Owner":"Financial Counselor","Days Open":2,"SLA Limit":5,"Exposure":7200,"Status":"Financial Review","Required Docs":["estimate","payment plan review"],"Present Docs":["estimate"],"First Control Loss":"Patient Access Control","Next Action":"Complete patient financial pathway review."},
    {"Case ID":"REV-0007","Payer Group":"Commercial","Workflow Domain":"Denial Prevention","Service Line":"Oncology","Risk":"High","Owner":"Denial Prevention Lead","Days Open":10,"SLA Limit":5,"Exposure":44200,"Status":"Pre Denial Review","Required Docs":["treatment plan","medical necessity note","prior therapy history","payer policy match"],"Present Docs":["treatment plan","medical necessity note"],"First Control Loss":"Time Control","Next Action":"Run pre denial review and attach policy matched documentation."},
    {"Case ID":"REV-0008","Payer Group":"Medicare Advantage","Workflow Domain":"Authorization Control","Service Line":"Imaging","Risk":"High","Owner":"Prior Authorization Lead","Days Open":6,"SLA Limit":5,"Exposure":19600,"Status":"Needs Documentation","Required Docs":["order","clinical note","failed therapy evidence","imaging rationale"],"Present Docs":["order","clinical note"],"First Control Loss":"Authorization Readiness Control","Next Action":"Request therapy evidence and attach imaging rationale."},
    {"Case ID":"REV-0009","Payer Group":"Medicaid","Workflow Domain":"Documentation Readiness","Service Line":"Behavioral Health","Risk":"Moderate","Owner":"Clinical Documentation Liaison","Days Open":6,"SLA Limit":5,"Exposure":9800,"Status":"Needs Documentation","Required Docs":["assessment","treatment plan","provider attestation"],"Present Docs":["assessment"],"First Control Loss":"Documentation Control","Next Action":"Secure treatment plan and attestation before routing."},
    {"Case ID":"REV-0010","Payer Group":"Commercial","Workflow Domain":"Eligibility Verification","Service Line":"Primary Care","Risk":"Low","Owner":"Patient Access Specialist","Days Open":1,"SLA Limit":5,"Exposure":2600,"Status":"Ready","Required Docs":["eligibility response","benefit check"],"Present Docs":["eligibility response","benefit check"],"First Control Loss":"None","Next Action":"Proceed with standard review."},
    {"Case ID":"REV-0011","Payer Group":"Medicare Advantage","Workflow Domain":"Patient Access","Service Line":"Rehabilitation","Risk":"High","Owner":"Access Operations Manager","Days Open":7,"SLA Limit":5,"Exposure":22300,"Status":"Escalate","Required Docs":["order","eligibility response","plan of care","authorization pathway"],"Present Docs":["order","plan of care"],"First Control Loss":"Patient Access Control","Next Action":"Escalate access pathway and complete eligibility validation."},
    {"Case ID":"REV-0012","Payer Group":"Commercial","Workflow Domain":"Routing Intelligence","Service Line":"Neurology","Risk":"Moderate","Owner":"RCM Analyst","Days Open":5,"SLA Limit":5,"Exposure":14100,"Status":"Routing Review","Required Docs":["payer route","order","clinical note"],"Present Docs":["order","clinical note"],"First Control Loss":"Ownership Control","Next Action":"Confirm payer route and prevent duplicate submission."},
    {"Case ID":"REV-0013","Payer Group":"Marketplace","Workflow Domain":"Denial Prevention","Service Line":"Cardiology","Risk":"High","Owner":"Revenue Integrity Analyst","Days Open":8,"SLA Limit":5,"Exposure":24250,"Status":"Pre Denial Review","Required Docs":["cardiology note","medical necessity note","payer policy match","procedure code"],"Present Docs":["cardiology note","procedure code"],"First Control Loss":"Documentation Control","Next Action":"Attach payer policy match and medical necessity support."},
    {"Case ID":"REV-0014","Payer Group":"Commercial","Workflow Domain":"Authorization Control","Service Line":"Surgery","Risk":"Moderate","Owner":"Prior Authorization Coordinator","Days Open":3,"SLA Limit":5,"Exposure":17300,"Status":"Ready for Submission","Required Docs":["order","surgical note","procedure code","site of service"],"Present Docs":["order","surgical note","procedure code","site of service"],"First Control Loss":"None","Next Action":"Submit and monitor payer response window."}
]

def money(value):
    return "${:,.0f}".format(value)

def safe(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def missing_docs(case):
    return [doc for doc in case["Required Docs"] if doc not in case["Present Docs"]]

def readiness_score(case):
    doc_penalty = len(missing_docs(case)) * 13
    aging_penalty = max(0, case["Days Open"] - case["SLA Limit"]) * 8
    risk_penalty = {"Low":0,"Moderate":7,"High":17}.get(case["Risk"],0)
    return max(0, min(100, 100 - doc_penalty - aging_penalty - risk_penalty))

def workflow_loss_index(case):
    base = {"Low":10,"Moderate":30,"High":50}.get(case["Risk"],20)
    score = base + len(missing_docs(case)) * 9 + max(0, case["Days Open"] - case["SLA Limit"]) * 8
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

def table_html(rows, columns):
    head = "".join(["<th>{}</th>".format(safe(c)) for c in columns])
    body = ""
    for row in rows:
        body += "<tr>" + "".join(["<td>{}</td>".format(safe(row.get(c, ""))) for c in columns]) + "</tr>"
    return '<div class="table-scroll"><table class="queue-table"><thead><tr>{}</tr></thead><tbody>{}</tbody></table></div>'.format(head, body)

def bar_html(label, value, max_value):
    width = 0 if max_value == 0 else (value / max_value) * 100
    return '<div class="bar-row"><div class="bar-label">{}</div><div class="track"><div class="fill" style="width:{}%"></div></div><div class="bar-value">{}</div></div>'.format(safe(label), width, value)

def brief_text(rows):
    total = len(rows)
    high = sum(1 for c in rows if c["Risk"] == "High")
    sla = sum(1 for c in rows if c["Days Open"] >= c["SLA Limit"])
    exposure = sum(c["Exposure"] for c in rows)
    owners = len(set(c["Owner"] for c in rows))
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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500&family=Inter:wght@300;400;500;600&family=Great+Vibes&display=swap');

:root { --orange: rgb(255, 130, 0); --black: rgb(0, 0, 0); --white: rgb(255, 255, 255); }

[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="collapsedControl"], header, footer {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}

html, body, [data-testid="stAppViewContainer"] { background: var(--white) !important; color: var(--black) !important; }
.block-container { max-width: 1380px !important; padding-top: 0.75rem !important; padding-left: 3rem !important; padding-right: 3rem !important; padding-bottom: 5rem !important; }

p, div, span, label, input, textarea, button, select { font-family: Inter, Arial, sans-serif !important; color: var(--black) !important; }
h1, h2, h3 { font-family: "Playfair Display", Georgia, serif !important; font-weight: 400 !important; letter-spacing: -0.035em !important; color: var(--black) !important; }

[data-testid="stSidebar"] { background: var(--white) !important; border-right: 2px solid var(--orange) !important; }
[data-testid="stSidebar"] label { font-size: 0.66rem !important; letter-spacing: 0.18em !important; text-transform: uppercase !important; }
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, textarea { background: var(--white) !important; border: 1px solid var(--black) !important; border-radius: 0 !important; box-shadow: inset 5px 0 0 var(--orange) !important; }
span[data-baseweb="tag"], [data-baseweb="tag"] { background: var(--white) !important; color: var(--black) !important; border: 1px solid var(--orange) !important; border-radius: 999px !important; }

.brand-shell { border-left: 1px solid var(--black); border-right: 1px solid var(--black); border-top: 7px solid var(--orange); padding: 2rem 2.2rem 2.7rem 2.2rem; background: var(--white); }
.signature-header { margin-bottom: 1.7rem; }
.signature-name { font-family: "Great Vibes", cursive !important; font-weight: 400 !important; font-size: clamp(4.3rem, 8vw, 8rem); line-height: 0.82; letter-spacing: 0; color: var(--black) !important; }
.signature-subline { margin-top: 0.9rem; font-size: 0.8rem; letter-spacing: 0.47em; text-transform: uppercase; font-weight: 500; }
.signature-intelligence { margin-top: 0.42rem; font-size: 0.82rem; letter-spacing: 0.56em; text-transform: uppercase; color: var(--orange) !important; font-weight: 500; }
.signature-rule { height: 5px; background: var(--orange); margin: 1.5rem 0 2.1rem 0; }

.kicker { font-size: 0.68rem; letter-spacing: 0.34em; text-transform: uppercase; font-weight: 500; margin-bottom: 1rem; }
.hero-grid { display: grid; grid-template-columns: 0.9fr 0.75fr; gap: 2rem; align-items: stretch; }
.hero-title { font-family: "Playfair Display", Georgia, serif !important; font-size: clamp(4rem, 7vw, 7.4rem); line-height: 0.92; letter-spacing: -0.05em; font-weight: 400 !important; margin: 0; }
.hero-title span { color: var(--orange) !important; font-family: "Playfair Display", Georgia, serif !important; font-weight: 400 !important; }
.hero-copy { margin-top: 1.6rem; max-width: 850px; font-size: 1.04rem; line-height: 1.82; font-weight: 400; }
.identity-panel { border: 1px solid var(--black); border-top: 7px solid var(--orange); padding: 2rem; min-height: 420px; display: flex; flex-direction: column; justify-content: space-between; }
.identity-statement { font-family: "Playfair Display", Georgia, serif !important; font-size: clamp(2.35rem, 4.1vw, 4rem); line-height: 1.02; letter-spacing: -0.035em; font-weight: 400; }
.orange-line { height: 4px; width: 60%; background: var(--orange); margin: 1.4rem 0; }
.badge { display: inline-block; border: 1px solid var(--black); border-left: 8px solid var(--orange); padding: 0.64rem 0.9rem; margin: 0.28rem; font-size: 0.67rem; font-weight: 500; letter-spacing: 0.13em; text-transform: uppercase; background: var(--white); }

.metric-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1rem; margin: 1.5rem 0 2rem 0; }
.metric-card { border: 1px solid var(--black); border-left: 8px solid var(--orange); border-top: 4px solid var(--orange); padding: 1.55rem; min-height: 162px; background: var(--white); position: relative; }
.metric-card:after { content: ""; position: absolute; right: 1rem; bottom: 1rem; width: 38px; height: 2px; background: var(--orange); }
.metric-label { font-size: 0.64rem; letter-spacing: 0.25em; text-transform: uppercase; font-weight: 500; margin-bottom: 1rem; }
.metric-value { font-family: "Playfair Display", Georgia, serif !important; font-size: clamp(3rem, 4.7vw, 4.8rem); line-height: 1.02; letter-spacing: -0.035em; font-weight: 400 !important; color: var(--black) !important; font-variant-numeric: lining-nums proportional-nums !important; }
.metric-note { font-size: 0.84rem; line-height: 1.5; margin-top: 0.95rem; }

.stTabs [data-baseweb="tab-list"] { gap: 0.6rem; border-bottom: 2px solid var(--orange); padding-bottom: 0.6rem; overflow-x: auto; }
.stTabs [data-baseweb="tab"] { background: var(--white) !important; border: 1px solid var(--black) !important; border-radius: 0 !important; padding: 0.7rem 1rem !important; font-weight: 400 !important; }
.stTabs [aria-selected="true"] { background: var(--orange) !important; border-color: var(--orange) !important; }

.section-title { font-family: "Playfair Display", Georgia, serif !important; font-size: clamp(2.8rem, 5vw, 5.1rem); line-height: 1; letter-spacing: -0.04em; font-weight: 400 !important; margin: 1.3rem 0 1rem 0; }
.section-panel { border: 1px solid var(--black); border-top: 5px solid var(--orange); padding: 2rem; margin: 1.2rem 0; }
.editorial-note { border: 1px solid var(--black); border-left: 8px solid var(--orange); padding: 1.6rem; margin: 1.2rem 0; }
.editorial-note h3 { font-family: "Playfair Display", Georgia, serif !important; font-size: clamp(2.2rem, 4vw, 3.6rem); line-height: 1; margin: 0 0 1rem 0; font-weight: 400 !important; }

.table-scroll { overflow-x: auto; border: 1px solid var(--black); border-top: 5px solid var(--orange); margin: 1rem 0; }
.queue-table { width: 100%; border-collapse: collapse; font-size: 0.86rem; }
.queue-table th { background: var(--orange); color: var(--black) !important; border: 1px solid var(--black); padding: 0.72rem; text-align: left; font-size: 0.62rem; letter-spacing: 0.14em; text-transform: uppercase; font-weight: 600; }
.queue-table td { border: 1px solid var(--black); padding: 0.72rem; vertical-align: top; }
.score-wrap { border: 1px solid var(--black); border-left: 8px solid var(--orange); border-top: 5px solid var(--orange); padding: 2rem; margin: 1rem 0; }
.score-number { font-family: "Playfair Display", Georgia, serif !important; font-size: clamp(4.2rem, 7.5vw, 7rem); font-weight: 400 !important; line-height: 1; letter-spacing: -0.035em; font-variant-numeric: lining-nums proportional-nums !important; }
.track { height: 13px; border: 1px solid var(--black); background: var(--white); }
.fill { height: 100%; background: var(--orange); }
.bar-row { display: grid; grid-template-columns: 130px 1fr 44px; gap: 1rem; align-items: center; margin: 1rem 0; }
.bar-value { font-family: "Playfair Display", Georgia, serif !important; font-size: 1.45rem; font-weight: 400 !important; color: var(--orange) !important; }
.footer-brand { border-top: 5px solid var(--orange); border-bottom: 5px solid var(--orange); text-align: center; padding: 2.4rem 1rem; margin-top: 3rem; }
.footer-signature { font-family: "Great Vibes", cursive !important; font-size: 5.3rem; font-weight: 400 !important; letter-spacing: 0; line-height: 1; margin: 0.7rem 0 0.5rem 0; }
.link-button { display: inline-block; border: 1px solid var(--black); border-left: 6px solid var(--orange); padding: 0.72rem 1.2rem; margin: 0.4rem; text-decoration: none !important; color: var(--black) !important; font-size: 0.72rem; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; }
button, .stDownloadButton button { background: var(--white) !important; border: 1px solid var(--black) !important; border-left: 6px solid var(--orange) !important; border-radius: 0 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; }

@media (max-width: 900px) {
    .block-container { padding-left: 1.05rem !important; padding-right: 1.05rem !important; }
    .brand-shell { padding: 1.35rem; }
    .hero-grid, .metric-grid { grid-template-columns: 1fr; }
    .hero-title { font-size: clamp(3.25rem, 13vw, 5.25rem); }
    .signature-name { font-size: clamp(4rem, 16vw, 6rem); }
    .metric-value { font-size: clamp(3rem, 14vw, 4.5rem); }
    .bar-row { grid-template-columns: 95px 1fr 30px; }
}
</style>
""", unsafe_allow_html=True)

risk_order = ["High", "Moderate", "Low"]
risk_options = [risk for risk in risk_order if risk in set(c["Risk"] for c in cases)]
payer_options = sorted(set(c["Payer Group"] for c in cases))
domain_options = sorted(set(c["Workflow Domain"] for c in cases))
line_options = sorted(set(c["Service Line"] for c in cases))

st.sidebar.markdown("### Command Filters")
st.sidebar.caption("Synthetic CSV upload only. Do not upload PHI.")
uploaded = st.sidebar.file_uploader("Synthetic CSV Upload Option", type=["csv"])
selected_risks = st.sidebar.multiselect("Filter by risk level", risk_options, default=risk_options)
selected_payers = st.sidebar.multiselect("Filter by payer group", payer_options, default=payer_options)
selected_domains = st.sidebar.multiselect("Filter by workflow area", domain_options, default=domain_options)
selected_lines = st.sidebar.multiselect("Filter by service line", line_options, default=line_options)

filtered = [c for c in cases if c["Risk"] in selected_risks and c["Payer Group"] in selected_payers and c["Workflow Domain"] in selected_domains and c["Service Line"] in selected_lines]
if uploaded is not None:
    st.sidebar.warning("Upload detected. For portfolio safety, the app continues using built in synthetic records unless the file is confirmed to contain no PHI.")

total = len(filtered)
high = sum(1 for c in filtered if c["Risk"] == "High")
sla = sum(1 for c in filtered if c["Days Open"] >= c["SLA Limit"])
exposure = sum(c["Exposure"] for c in filtered)
avg_ready = round(sum(readiness_score(c) for c in filtered) / total, 1) if total else 0
avg_days = round(sum(c["Days Open"] for c in filtered) / total, 1) if total else 0
owners = len(set(c["Owner"] for c in filtered))

st.markdown("""
<div class="brand-shell">
    <div class="signature-header">
        <div class="signature-name">Kori Pickle</div>
        <div class="signature-subline">Healthcare Operations</div>
        <div class="signature-intelligence">Intelligence</div>
        <div class="signature-rule"></div>
    </div>
    <div class="hero-grid">
        <div>
            <div class="kicker">Kori Pickle • Healthcare Operations Intelligence</div>
            <h1 class="hero-title">Enterprise<br>Revenue<br><span>Operations</span><br>Platform</h1>
            <div class="hero-copy">
                A premium synthetic no PHI healthcare operations command center for patient access, eligibility verification, prior authorization pressure tracking, routing intelligence, documentation readiness, denial prevention, payer friction analysis, and responsible operational intelligence.
                <br><br>
                This build functions as an operational review workbench: filter synthetic cases, isolate ownership gaps, simulate stabilization impact, generate escalation language, and build a leadership brief from the active command view.
            </div>
            <div style="margin-top:1.6rem;">
                <span class="badge">No PHI</span><span class="badge">Synthetic Data</span><span class="badge">Human Review Required</span><span class="badge">Built by Kori Pickle</span>
            </div>
        </div>
        <div class="identity-panel">
            <div>
                <div class="kicker">Operational Identity</div>
                <div class="identity-statement">Workflow visibility before revenue damage.</div>
                <div class="orange-line"></div>
                <p>Designed around one question: where did the workflow first lose control?</p>
            </div>
            <div class="kicker">Patient Access • Authorization Control • Documentation Readiness • Denial Prevention</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="metric-grid">
    <div class="metric-card"><div class="metric-label">High Risk Records</div><div class="metric-value">{}</div><div class="metric-note">Prioritized operational review queue.</div></div>
    <div class="metric-card"><div class="metric-label">SLA Pressure</div><div class="metric-value">{}</div><div class="metric-note">Records aged at or above SLA limit.</div></div>
    <div class="metric-card"><div class="metric-label">Synthetic Exposure</div><div class="metric-value">{}</div><div class="metric-note">Portfolio simulation only.</div></div>
    <div class="metric-card"><div class="metric-label">Readiness Average</div><div class="metric-value">{}</div><div class="metric-note">Aggregate workflow readiness score.</div></div>
</div>
""".format(high, sla, money(exposure), avg_ready), unsafe_allow_html=True)

tabs = st.tabs(["Command Center", "Workflow Loss Method", "Readiness Engine", "Documentation Detector", "Payer Rule Lab", "SLA Countdown", "Work Queue", "Audit Log", "Stabilization Simulator", "2027 API Checklist", "About Kori", "Brief Builder"])

with tabs[0]:
    st.markdown('<div class="section-title">Live Command Center</div>', unsafe_allow_html=True)
    st.write("Use the sidebar filters to isolate operational pressure across payer group, workflow domain, service line, and risk level.")
    rows = [{"Case ID":c["Case ID"], "Payer Group":c["Payer Group"], "Workflow Domain":c["Workflow Domain"], "Service Line":c["Service Line"], "Risk":c["Risk"], "Owner":c["Owner"], "Days Open":c["Days Open"], "Status":c["Status"]} for c in filtered]
    st.markdown(table_html(rows, ["Case ID", "Payer Group", "Workflow Domain", "Service Line", "Risk", "Owner", "Days Open", "Status"]), unsafe_allow_html=True)
    risk_counts = {r: sum(1 for c in filtered if c["Risk"] == r) for r in risk_options}
    max_count = max(risk_counts.values()) if risk_counts else 1
    st.markdown('<div class="section-panel"><div class="kicker">Risk Queue Distribution</div>{}</div>'.format("".join(bar_html(r, risk_counts[r], max_count) for r in risk_options)), unsafe_allow_html=True)
    st.markdown('<div class="editorial-note"><h3>Executive Interpretation</h3><p>The active view shows {} synthetic records, {} high risk records, {} SLA pressure signals, average aging of {} days, {} distinct owners, and {} in simulated exposure. These are prioritization signals for human review, not automated payer or clinical decisions.</p></div>'.format(total, high, sla, avg_days, owners, money(exposure)), unsafe_allow_html=True)

with tabs[1]:
    st.markdown('<div class="section-title">Kori Pickle Workflow Loss Control Method</div>', unsafe_allow_html=True)
    st.write("This proprietary method identifies where the workflow first lost control before the issue becomes revenue damage, denial risk, staff burden, or patient access delay.")
    selected_id = st.selectbox("Select synthetic case for control review", [c["Case ID"] for c in filtered] if filtered else ["No active records"])
    case = next((c for c in filtered if c["Case ID"] == selected_id), None)
    if case:
        score = workflow_loss_index(case)
        st.markdown('<div class="score-wrap"><div class="kicker">Workflow Loss Index</div><div class="score-number">{}</div><p>{}</p><div class="track"><div class="fill" style="width:{}%"></div></div></div>'.format(score, loss_label(score), score), unsafe_allow_html=True)
        st.markdown('<div class="section-panel"><div class="kicker">First Control Loss</div><div class="section-title">{}</div><p>{}</p></div>'.format(safe(case["First Control Loss"]), safe(case["Next Action"])), unsafe_allow_html=True)
        domains = ["Patient Access Control", "Authorization Readiness Control", "Documentation Control", "Ownership Control", "Time Control"]
        st.markdown('<div class="section-panel"><div class="kicker">Five Control Domains</div>{}</div>'.format("".join('<span class="badge">{}</span>'.format(d) for d in domains)), unsafe_allow_html=True)

with tabs[2]:
    st.markdown('<div class="section-title">Authorization Readiness Engine</div>', unsafe_allow_html=True)
    rows = [{"Case ID":c["Case ID"], "Readiness":readiness_score(c), "Workflow Loss":workflow_loss_index(c), "Label":loss_label(workflow_loss_index(c)), "Missing Items":", ".join(missing_docs(c)) if missing_docs(c) else "None", "Next Action":c["Next Action"]} for c in filtered]
    st.markdown(table_html(rows, ["Case ID", "Readiness", "Workflow Loss", "Label", "Missing Items", "Next Action"]), unsafe_allow_html=True)

with tabs[3]:
    st.markdown('<div class="section-title">Missing Documentation Detector</div>', unsafe_allow_html=True)
    rows = [{"Case ID":c["Case ID"], "Required Documentation":", ".join(c["Required Docs"]), "Present Documentation":", ".join(c["Present Docs"]), "Missing Documentation":", ".join(missing_docs(c)) if missing_docs(c) else "None", "Readiness":readiness_score(c)} for c in filtered]
    st.markdown(table_html(rows, ["Case ID", "Required Documentation", "Present Documentation", "Missing Documentation", "Readiness"]), unsafe_allow_html=True)

with tabs[4]:
    st.markdown('<div class="section-title">Payer Rule Lab</div>', unsafe_allow_html=True)
    payer = st.selectbox("Choose payer group", payer_options)
    domain = st.selectbox("Choose workflow domain", domain_options)
    rule = {"Commercial":"Validate plan rules, benefit limitations, authorization pathway, clinical documentation requirements, and payer portal route before submission.", "Medicare Advantage":"Confirm medical necessity support, prior therapy evidence, site of service expectations, payer specific authorization window, and appeal pathway.", "Medicaid":"Confirm eligibility status, referral requirements, covered service rules, documentation completeness, and state specific timing expectations.", "Marketplace":"Verify active coverage, deductible and benefit status, network rules, authorization pathway, and clinical packet readiness.", "Self Pay":"Complete estimate review, financial counseling pathway, payment plan documentation, and patient communication record."}
    st.markdown('<div class="editorial-note"><h3>{}</h3><p>{}</p><p>Applied domain: {}</p></div>'.format(payer, rule[payer], domain), unsafe_allow_html=True)

with tabs[5]:
    st.markdown('<div class="section-title">SLA Breach Countdown</div>', unsafe_allow_html=True)
    rows = []
    for c in filtered:
        remaining = c["SLA Limit"] - c["Days Open"]
        countdown = "Due today" if remaining == 0 else ("{} days overdue".format(abs(remaining)) if remaining < 0 else "{} days remaining".format(remaining))
        rows.append({"Case ID":c["Case ID"], "Owner":c["Owner"], "Days Open":c["Days Open"], "SLA Limit":c["SLA Limit"], "Countdown":countdown, "Status":c["Status"]})
    st.markdown(table_html(rows, ["Case ID", "Owner", "Days Open", "SLA Limit", "Countdown", "Status"]), unsafe_allow_html=True)

with tabs[6]:
    st.markdown('<div class="section-title">Operational Work Queue</div>', unsafe_allow_html=True)
    queue = sorted(filtered, key=lambda c: workflow_loss_index(c), reverse=True)
    rows = [{"Rank":i+1, "Case ID":c["Case ID"], "Owner":c["Owner"], "Workflow Loss":workflow_loss_index(c), "Control Label":loss_label(workflow_loss_index(c)), "Next Action":c["Next Action"]} for i, c in enumerate(queue)]
    st.markdown(table_html(rows, ["Rank", "Case ID", "Owner", "Workflow Loss", "Control Label", "Next Action"]), unsafe_allow_html=True)

with tabs[7]:
    st.markdown('<div class="section-title">Audit Trail and Human Review Log</div>', unsafe_allow_html=True)
    rows = [{"Date":date.today().isoformat(), "Case ID":c["Case ID"], "Reviewer Role":c["Owner"], "Review Type":"Human operational review", "Audit Note":"Reviewed synthetic case for workflow loss, missing documentation, SLA pressure, and ownership clarity."} for c in filtered if workflow_loss_index(c) >= 51]
    st.markdown(table_html(rows, ["Date", "Case ID", "Reviewer Role", "Review Type", "Audit Note"]), unsafe_allow_html=True) if rows else st.info("No control loss cases in the active synthetic view.")

with tabs[8]:
    st.markdown('<div class="section-title">Before and After Stabilization Simulator</div>', unsafe_allow_html=True)
    doc_capture = st.slider("Documentation completion improvement", 0, 40, 18)
    routing_gain = st.slider("Routing accuracy improvement", 0, 40, 12)
    follow_up_gain = st.slider("Payer follow up reliability improvement", 0, 40, 10)
    improvement = min(0.65, (doc_capture + routing_gain + follow_up_gain) / 160)
    st.markdown('<div class="metric-grid"><div class="metric-card"><div class="metric-label">Current Exposure</div><div class="metric-value">{}</div></div><div class="metric-card"><div class="metric-label">Potential Stabilized Exposure</div><div class="metric-value">{}</div></div><div class="metric-card"><div class="metric-label">Current SLA Signals</div><div class="metric-value">{}</div></div><div class="metric-card"><div class="metric-label">Post Stabilization SLA Signals</div><div class="metric-value">{}</div></div></div>'.format(money(exposure), money(exposure * improvement), sla, max(0, int(round(sla * (1 - improvement))))), unsafe_allow_html=True)

with tabs[9]:
    st.markdown('<div class="section-title">2027 API Readiness Checklist</div>', unsafe_allow_html=True)
    checklist = ["Synthetic data separation is documented", "No PHI is uploaded or stored", "Human review boundary is visible", "Audit log captures reviewer role and action", "Payer rule logic is explainable", "Prior authorization readiness is separated from clinical judgment", "FHIR aligned fields are identified for future integration", "CSV import is restricted to synthetic portfolio data"]
    complete = sum(1 for item in checklist if st.checkbox(item, value=True))
    readiness = int((complete / len(checklist)) * 100)
    st.markdown('<div class="score-wrap"><div class="kicker">API Readiness Position</div><div class="score-number">{}%</div><p>{} of {} controls confirmed.</p></div>'.format(readiness, complete, len(checklist)), unsafe_allow_html=True)

with tabs[10]:
    st.markdown('<div class="section-title">About Kori</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-panel"><div class="kicker">Healthcare Operations Intelligence</div><p>Kori Pickle is a BSHA candidate at the University of Phoenix with a focus on healthcare operations, revenue cycle management, patient access, prior authorization, denial prevention, health informatics, and workflow intelligence.</p><p>This platform reflects a patient to professional perspective: healthcare workflows should be clear, accountable, visible, and safe before they become access barriers, rework, or downstream revenue damage.</p><div class="orange-line"></div><p>Academic standing: 99 of 120 credits completed. GPA 3.6.</p><p>Professional focus: remote healthcare administration, revenue cycle operations, patient access operations, prior authorization workflows, and responsible operational intelligence.</p></div><div class="section-panel"><div class="kicker">Branded Resume Snapshot</div><p>Core strengths: revenue cycle management, prior authorization workflows, eligibility verification, workflow analysis, denial prevention, patient access operations, health informatics, quality improvement, and documentation readiness.</p><p>Portfolio position: building synthetic healthcare operations tools that demonstrate workflow logic, human review boundaries, and operational stabilization methods without using PHI.</p></div>', unsafe_allow_html=True)

with tabs[11]:
    st.markdown('<div class="section-title">Downloadable Executive Brief Builder</div>', unsafe_allow_html=True)
    brief = st.text_area("Leadership brief", brief_text(filtered), height=430)
    st.download_button("Download Executive Brief", brief, file_name="kori_pickle_enterprise_revenue_operations_brief.txt", mime="text/plain")
    csv_buffer = StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=["Case ID", "Payer Group", "Workflow Domain", "Service Line", "Risk", "Owner", "Days Open", "Status", "Exposure"])
    writer.writeheader()
    for c in filtered:
        writer.writerow({k: c[k] for k in writer.fieldnames})
    st.download_button("Download Synthetic Work Queue CSV", csv_buffer.getvalue(), file_name="synthetic_work_queue.csv", mime="text/csv")

st.markdown("""
<div class="footer-brand">
    <div class="footer-signature">Kori Pickle</div>
    <div class="signature-subline">Healthcare Operations</div>
    <div class="signature-intelligence">Intelligence</div>
    <div class="kicker" style="margin-top:1.4rem;">Created by Kori Pickle</div>
    <p>Healthcare Operations Intelligence • Revenue Cycle • Patient Access • Prior Authorization • Denial Prevention</p>
    <a class="link-button" href="https://www.linkedin.com/" target="_blank">LinkedIn</a>
    <a class="link-button" href="https://github.com/koripickle1101-TN" target="_blank">GitHub</a>
</div>
""", unsafe_allow_html=True)
