import csv
import html
from datetime import date
from io import StringIO
from collections import Counter
import streamlit as st

st.set_page_config(
    page_title="Kori Pickle Healthcare Operations Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

LINKEDIN_URL = "https://www.linkedin.com/in/kori-p-865jct"
GITHUB_URL = "https://github.com/koripickle1101-TN"

DEFAULT_DATA = [
    {"id":"REV-0001","payer":"Commercial","domain":"Patient Access","line":"Orthopedics","risk":"High","owner":"Patient Access Lead","days":7,"sla":5,"exposure":18450,"status":"Needs Documentation","required":"Order;Insurance Card;Clinical Note;Medical Necessity Note;Eligibility Response;Benefit Check","present":"Order;Insurance Card","loss":"Documentation Control","rule":"Medical necessity narrative required before authorization submission.","action":"Validate documentation packet and assign same day authorization follow up."},
    {"id":"REV-0002","payer":"Medicare Advantage","domain":"Authorization Control","line":"Neurology","risk":"High","owner":"Prior Authorization Lead","days":9,"sla":5,"exposure":32700,"status":"Escalate","required":"Order;Neuro Exam;Failed Conservative Therapy;Imaging Rationale;Payer Policy Match","present":"Order;Neuro Exam","loss":"Authorization Control","rule":"Conservative therapy evidence and imaging rationale required.","action":"Escalate payer follow up and request missing medical necessity support."},
    {"id":"REV-0003","payer":"Medicaid","domain":"Documentation Readiness","line":"Rehabilitation","risk":"Moderate","owner":"Documentation Specialist","days":4,"sla":5,"exposure":12600,"status":"Needs Eligibility Review","required":"Plan of Care;Therapy Evaluation;Frequency Order;Provider Attestation","present":"Plan of Care;Therapy Evaluation","loss":"Documentation Control","rule":"Therapy frequency order must match requested treatment period.","action":"Confirm therapy frequency order before submission."},
    {"id":"REV-0004","payer":"Commercial","domain":"Routing Intelligence","line":"Cardiology","risk":"High","owner":"RCM Analyst","days":8,"sla":4,"exposure":28600,"status":"Routing Review","required":"Referral;Cardiology Note;Payer Route;Procedure Code","present":"Referral;Cardiology Note;Procedure Code","loss":"Routing Control","rule":"Correct payer route must be established before submission.","action":"Correct payer route and document escalation owner."},
    {"id":"REV-0005","payer":"Marketplace","domain":"Eligibility Verification","line":"Imaging","risk":"Moderate","owner":"Eligibility Specialist","days":5,"sla":5,"exposure":11250,"status":"Needs Eligibility Review","required":"Eligibility Response;Benefit Check;Order","present":"Order","loss":"Access Control","rule":"Eligibility response and benefit confirmation required before scheduling clearance.","action":"Complete eligibility response and benefit confirmation."},
    {"id":"REV-0006","payer":"Self Pay","domain":"Financial Clearance","line":"Surgery","risk":"Low","owner":"Financial Counselor","days":2,"sla":5,"exposure":7200,"status":"Financial Review","required":"Estimate;Payment Plan Review","present":"Estimate","loss":"Access Control","rule":"Financial pathway review required before scheduled procedure date.","action":"Complete patient financial pathway review."},
    {"id":"REV-0007","payer":"Commercial","domain":"Denial Prevention","line":"Oncology","risk":"High","owner":"Denial Prevention Lead","days":10,"sla":5,"exposure":44200,"status":"Pre Denial Review","required":"Treatment Plan;Medical Necessity Note;Prior Therapy History;Payer Policy Match","present":"Treatment Plan;Medical Necessity Note","loss":"Follow-Up Control","rule":"Policy matched documentation required for high cost treatment authorization.","action":"Run pre denial review and attach policy matched documentation."},
    {"id":"REV-0008","payer":"Medicare Advantage","domain":"Authorization Control","line":"Imaging","risk":"High","owner":"Prior Authorization Lead","days":6,"sla":5,"exposure":19600,"status":"Needs Documentation","required":"Order;Clinical Note;Failed Therapy Evidence;Imaging Rationale","present":"Order;Clinical Note","loss":"Authorization Control","rule":"Failed therapy evidence must be documented for advanced imaging authorization.","action":"Request therapy evidence and attach imaging rationale."},
    {"id":"REV-0009","payer":"Medicaid","domain":"Documentation Readiness","line":"Behavioral Health","risk":"Moderate","owner":"Clinical Documentation Liaison","days":6,"sla":5,"exposure":9800,"status":"Needs Documentation","required":"Assessment;Treatment Plan;Provider Attestation","present":"Assessment","loss":"Documentation Control","rule":"Provider attestation and treatment plan must be present before routing.","action":"Secure treatment plan and attestation before routing."},
    {"id":"REV-0010","payer":"Commercial","domain":"Eligibility Verification","line":"Primary Care","risk":"Low","owner":"Patient Access Specialist","days":1,"sla":5,"exposure":2600,"status":"Ready","required":"Eligibility Response;Benefit Check","present":"Eligibility Response;Benefit Check","loss":"None","rule":"Standard eligibility confirmation complete.","action":"Proceed with standard review."},
    {"id":"REV-0011","payer":"Medicare Advantage","domain":"Patient Access","line":"Rehabilitation","risk":"High","owner":"Access Operations Manager","days":7,"sla":5,"exposure":22300,"status":"Escalate","required":"Order;Eligibility Response;Plan of Care;Authorization Pathway","present":"Order;Plan of Care","loss":"Access Control","rule":"Eligibility pathway and authorization route must be confirmed before start of care.","action":"Escalate access pathway and complete eligibility validation."},
    {"id":"REV-0012","payer":"Commercial","domain":"Routing Intelligence","line":"Neurology","risk":"Moderate","owner":"RCM Analyst","days":5,"sla":5,"exposure":14100,"status":"Routing Review","required":"Payer Route;Order;Clinical Note","present":"Order;Clinical Note","loss":"Routing Control","rule":"Correct payer route required to prevent duplicate submission.","action":"Confirm payer route and prevent duplicate submission."},
    {"id":"REV-0013","payer":"Marketplace","domain":"Denial Prevention","line":"Cardiology","risk":"High","owner":"Revenue Integrity Analyst","days":8,"sla":5,"exposure":24250,"status":"Pre Denial Review","required":"Cardiology Note;Medical Necessity Note;Payer Policy Match;Procedure Code","present":"Cardiology Note;Procedure Code","loss":"Documentation Control","rule":"Payer policy match and medical necessity support required before submission.","action":"Attach payer policy match and medical necessity support."},
    {"id":"REV-0014","payer":"Commercial","domain":"Authorization Control","line":"Surgery","risk":"Moderate","owner":"Prior Authorization Coordinator","days":3,"sla":5,"exposure":17300,"status":"Ready for Submission","required":"Order;Surgical Note;Procedure Code;Site of Service","present":"Order;Surgical Note;Procedure Code;Site of Service","loss":"None","rule":"Required surgical authorization packet complete.","action":"Submit and monitor payer response window."}
]

REQUIRED_COLUMNS = {
    "Case ID": "id",
    "Payer Group": "payer",
    "Workflow Domain": "domain",
    "Service Line": "line",
    "Risk": "risk",
    "Owner": "owner",
    "Days Open": "days",
    "SLA Limit": "sla",
    "Exposure": "exposure",
    "Status": "status",
    "Required Docs": "required",
    "Present Docs": "present",
    "First Control Loss": "loss",
    "Payer Rule": "rule",
    "Next Action": "action"
}

CONTROL_DOMAINS = ["Access Control", "Documentation Control", "Authorization Control", "Routing Control", "Follow-Up Control"]

def esc(value):
    return html.escape(str(value))

def money(value):
    return "${:,.0f}".format(float(value or 0))

def split_items(value):
    return [item.strip() for item in str(value or "").split(";") if item.strip()]

def missing_docs(case):
    present = set(split_items(case.get("present", "")))
    return [item for item in split_items(case.get("required", "")) if item not in present]

def readiness_score(case):
    missing = len(missing_docs(case))
    overdue = max(0, int(case.get("days", 0)) - int(case.get("sla", 5)))
    risk_penalty = {"Low": 0, "Moderate": 7, "High": 16}.get(case.get("risk", ""), 5)
    score = 100 - missing * 13 - overdue * 8 - risk_penalty
    return round(max(0, min(100, score)), 1)

def wlcm_scores(case):
    misses = len(missing_docs(case))
    overdue = max(0, int(case.get("days", 0)) - int(case.get("sla", 5)))
    base = {
        "Access Control": 86,
        "Documentation Control": 86,
        "Authorization Control": 86,
        "Routing Control": 86,
        "Follow-Up Control": 86
    }
    loss = case.get("loss", "None")
    if loss in base:
        base[loss] -= 32
    if case.get("domain") in ["Patient Access", "Eligibility Verification", "Financial Clearance"]:
        base["Access Control"] -= 12
    if misses:
        base["Documentation Control"] -= misses * 9
    if case.get("domain") == "Authorization Control":
        base["Authorization Control"] -= 16
    if case.get("domain") == "Routing Intelligence":
        base["Routing Control"] -= 18
    if overdue:
        base["Follow-Up Control"] -= overdue * 10
    return {key: max(0, min(100, round(value, 1))) for key, value in base.items()}

def first_failed_domain(case):
    scores = wlcm_scores(case)
    return min(scores, key=scores.get)

def stability_status(case):
    score = readiness_score(case)
    overdue = max(0, int(case.get("days", 0)) - int(case.get("sla", 5)))
    if case.get("risk") == "High" and overdue >= 2:
        return "Escalation Required"
    if score < 55:
        return "Control Loss"
    if score < 78:
        return "Watch"
    return "Stable"

def auth_readiness(case):
    factors = {
        "Eligibility verified": any(x in split_items(case.get("present", "")) for x in ["Eligibility Response", "Benefit Check"]),
        "Benefit checked": "Benefit Check" in split_items(case.get("present", "")),
        "CPT or service requirement reviewed": any(x in split_items(case.get("present", "")) for x in ["Procedure Code", "Site of Service"]),
        "Clinical note present": any(x in split_items(case.get("present", "")) for x in ["Clinical Note", "Cardiology Note", "Neuro Exam", "Surgical Note", "Assessment"]),
        "Medical necessity support present": "Medical Necessity Note" in split_items(case.get("present", "")),
        "Prior therapy history present when required": any(x in split_items(case.get("present", "")) for x in ["Prior Therapy History", "Failed Conservative Therapy", "Failed Therapy Evidence"]) or "Therapy" not in case.get("required", ""),
        "Payer route confirmed": "Payer Route" in split_items(case.get("present", "")) or case.get("domain") != "Routing Intelligence",
        "Submission owner assigned": bool(case.get("owner", "")),
        "Follow-up date documented": int(case.get("days", 0)) <= int(case.get("sla", 5))
    }
    met = sum(1 for value in factors.values() if value)
    score = round(met / len(factors) * 100, 1)
    if score >= 85:
        status = "Ready"
    elif score >= 65:
        status = "Needs Review"
    elif case.get("risk") == "High":
        status = "Escalate"
    else:
        status = "Not Ready"
    return factors, score, status

def sla_status(case):
    days = int(case.get("days", 0))
    sla = int(case.get("sla", 5))
    remaining = sla - days
    if remaining < 0:
        return remaining, "Breached", "Escalate today"
    if remaining == 0:
        return remaining, "Due Today", "Complete review today"
    if remaining <= 2:
        return remaining, "Breach Risk", "Assign owner and follow-up window"
    return remaining, "Within Window", "Monitor"

def parse_csv(uploaded):
    if uploaded is None:
        return DEFAULT_DATA, ""
    try:
        raw = uploaded.getvalue().decode("utf-8")
        reader = csv.DictReader(StringIO(raw))
        rows = []
        for row in reader:
            item = {}
            for external, internal in REQUIRED_COLUMNS.items():
                item[internal] = row.get(external, row.get(internal, ""))
            for number_key in ["days", "sla", "exposure"]:
                try:
                    item[number_key] = int(float(item[number_key]))
                except Exception:
                    item[number_key] = 0
            if item.get("id"):
                rows.append(item)
        if rows:
            return rows, "Synthetic CSV loaded. Validation passed."
        return DEFAULT_DATA, "CSV did not include valid case rows. Default synthetic data is active."
    except Exception:
        return DEFAULT_DATA, "CSV could not be read. Default synthetic data is active."

def summary(rows):
    total = len(rows)
    high = sum(1 for row in rows if row.get("risk") == "High")
    sla = sum(1 for row in rows if int(row.get("days", 0)) >= int(row.get("sla", 5)))
    exposure = sum(int(row.get("exposure", 0)) for row in rows)
    owners = len(set(row.get("owner", "") for row in rows if row.get("owner", "")))
    avg_ready = round(sum(readiness_score(row) for row in rows) / total, 1) if total else 0
    return total, high, sla, exposure, owners, avg_ready

def most_common(rows, key):
    values = [row.get(key, "") for row in rows if row.get(key, "")]
    if not values:
        return "None"
    return Counter(values).most_common(1)[0][0]

def common_missing(rows):
    docs = []
    for row in rows:
        docs.extend(missing_docs(row))
    if not docs:
        return "None detected"
    return Counter(docs).most_common(1)[0][0]

def executive_brief(rows):
    total, high, sla, exposure, owners, avg_ready = summary(rows)
    return f"""Enterprise Revenue Operations Platform
Created by Kori Pickle
Generated {date.today().isoformat()}

Synthetic Data Standard
This platform uses synthetic records only. It does not process PHI, make payer decisions, make billing determinations, make coding decisions, or provide clinical recommendations.

Active Command View
Total synthetic records reviewed: {total}
High risk count: {high}
SLA pressure count: {sla}
Average readiness score: {avg_ready}
Simulated exposure: {money(exposure)}
Distinct owners: {owners}
Top workflow failure domain: {most_common(rows, "loss")}
Most common missing documentation item: {common_missing(rows)}
Highest pressure payer group: {most_common([r for r in rows if r.get("risk") == "High"], "payer")}

Recommended Leadership Action
Prioritize human review for records with missing documentation, breached SLA windows, payer routing uncertainty, and authorization readiness gaps. Use the Workflow Loss Control Method to identify where control was lost before the issue becomes downstream denial activity, rework burden, patient access delay, or revenue leakage.
"""

def metric_html(label, value, note):
    return f"""
        <div class="metric-card">
            <div class="eyebrow">{esc(label)}</div>
            <div class="metric-number">{esc(value)}</div>
            <div class="metric-note">{esc(note)}</div>
        </div>
    """

def case_card_html(case):
    docs = missing_docs(case)
    miss = ", ".join(docs) if docs else "None detected"
    status = stability_status(case)
    return f"""
        <div class="case-card">
            <div class="case-title">{esc(case.get("id"))}</div>
            <div class="case-meta">{esc(case.get("risk"))} • {esc(case.get("payer"))} • {esc(case.get("domain"))} • {esc(case.get("line"))}</div>
            <div class="case-row"><b>Owner:</b> {esc(case.get("owner"))}</div>
            <div class="case-row"><b>Missing:</b> {esc(miss)}</div>
            <div class="case-row"><b>Control Status:</b> {esc(status)}</div>
            <div class="case-row"><b>Next:</b> {esc(case.get("action"))}</div>
        </div>
    """

def bar_html(label, value, max_value):
    width = 0 if max_value == 0 else round(value / max_value * 100, 1)
    return f"""
        <div class="bar-row">
            <div>{esc(label)}</div>
            <div class="track"><div class="fill" style="width:{width}%"></div></div>
            <div class="bar-number">{esc(value)}</div>
        </div>
    """

def render_table(rows):
    header = ["Case ID", "Payer Group", "Workflow Domain", "Service Line", "Risk", "Owner", "Days Open", "SLA Status", "Readiness"]
    html_rows = ""
    for row in rows:
        _, sla_label, _ = sla_status(row)
        html_rows += f"""
        <tr>
            <td>{esc(row.get("id"))}</td>
            <td>{esc(row.get("payer"))}</td>
            <td>{esc(row.get("domain"))}</td>
            <td>{esc(row.get("line"))}</td>
            <td>{esc(row.get("risk"))}</td>
            <td>{esc(row.get("owner"))}</td>
            <td>{esc(row.get("days"))}</td>
            <td>{esc(sla_label)}</td>
            <td>{esc(readiness_score(row))}</td>
        </tr>
        """
    heads = "".join(f"<th>{h}</th>" for h in header)
    st.markdown(f'<div class="table-wrap"><table><thead><tr>{heads}</tr></thead><tbody>{html_rows}</tbody></table></div>', unsafe_allow_html=True)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;500&display=swap');
    :root { --orange: #FF8200; --black: #000000; --white: #FFFFFF; }
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], header, footer { display: none !important; visibility: hidden !important; height: 0 !important; }
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] { background: var(--white) !important; color: var(--black) !important; }
    .block-container { max-width: 1280px !important; padding: 2rem 3rem 5rem !important; }
    [data-testid="stSidebar"] { background: var(--white) !important; border-right: 6px solid var(--orange) !important; }
    p, div, span, label, input, textarea, select, button { font-family: Inter, Arial, sans-serif !important; color: var(--black) !important; }
    h1, h2, h3 { font-family: "Playfair Display", Georgia, serif !important; font-weight: 400 !important; color: var(--black) !important; letter-spacing: -0.04em !important; }
    .shell { border-left: 2px solid var(--black); border-right: 2px solid var(--black); background: var(--white); padding: 3rem 4rem; }
    .brand-signature { font-family: "Great Vibes", cursive !important; font-size: clamp(4.8rem, 12vw, 9rem); line-height: 0.72; margin: 0 0 1.5rem; color: var(--black) !important; }
    .brand-sub { letter-spacing: 0.42em; text-transform: uppercase; font-size: 0.92rem; line-height: 2.4; }
    .orange-rule { height: 12px; background: var(--orange); margin: 2.5rem 0 4rem; }
    .eyebrow { letter-spacing: 0.34em; text-transform: uppercase; font-size: 0.76rem; font-weight: 600; line-height: 2; }
    .hero-title { font-family: "Playfair Display", Georgia, serif !important; font-size: clamp(4.2rem, 12vw, 10rem); line-height: 0.88; letter-spacing: -0.06em; font-weight: 400 !important; margin: 3rem 0 2rem; }
    .hero-title span { font-family: "Playfair Display", Georgia, serif !important; color: var(--orange) !important; font-weight: 400 !important; }
    .body-copy { font-size: clamp(1.1rem, 2vw, 1.45rem); line-height: 1.9; font-weight: 300; max-width: 980px; }
    .badges { display: flex; flex-wrap: wrap; gap: 1rem; margin: 3rem 0; }
    .badge { border: 1px solid var(--black); border-left: 12px solid var(--orange); padding: 0.95rem 1.25rem; letter-spacing: 0.2em; text-transform: uppercase; font-weight: 600; font-size: 0.78rem; background: var(--white); }
    .identity-panel, .section-panel { border: 1px solid var(--black); border-top: 10px solid var(--orange); padding: 3rem; margin: 3rem 0; background: var(--white); }
    .identity-title, .section-title { font-family: "Playfair Display", Georgia, serif !important; font-weight: 400 !important; letter-spacing: -0.05em; line-height: 0.94; }
    .identity-title { font-size: clamp(2.8rem, 7vw, 5.6rem); margin: 2rem 0; }
    .section-title { font-size: clamp(3rem, 8vw, 6rem); margin: 1rem 0 1.5rem; }
    .metrics-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1.2rem; margin: 3rem 0; }
    .metric-card { border: 1px solid var(--black); border-left: 12px solid var(--orange); padding: 2rem; min-height: 210px; background: var(--white); }
    .metric-number { font-family: "Playfair Display", Georgia, serif !important; font-weight: 400 !important; color: var(--orange) !important; font-size: clamp(3rem, 6vw, 5.4rem); line-height: 1; margin: 1.5rem 0 1rem; letter-spacing: -0.06em; }
    .metric-note { font-size: 1rem; line-height: 1.5; }
    .case-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1.2rem; margin: 2rem 0; }
    .case-card { border: 1px solid var(--black); border-left: 10px solid var(--orange); padding: 1.5rem; background: var(--white); }
    .case-title { font-family: "Playfair Display", Georgia, serif !important; font-size: 2.3rem; letter-spacing: -0.05em; line-height: 1; }
    .case-meta { letter-spacing: 0.14em; text-transform: uppercase; font-size: 0.75rem; line-height: 1.7; margin: 1rem 0; }
    .case-row { line-height: 1.6; margin: 0.55rem 0; }
    .table-wrap { overflow-x: auto; border: 1px solid var(--black); margin: 2rem 0; background: var(--white); }
    table { border-collapse: collapse; min-width: 1120px; width: 100%; background: var(--white); }
    th { background: var(--orange); color: var(--black); letter-spacing: 0.16em; text-transform: uppercase; font-size: 0.72rem; }
    th, td { border: 1px solid var(--black); padding: 1rem; text-align: left; vertical-align: top; }
    .bar-row { display: grid; grid-template-columns: 140px 1fr 56px; gap: 1rem; align-items: center; margin: 1.25rem 0; font-size: 1.1rem; }
    .track { height: 24px; border: 1px solid var(--black); background: var(--white); }
    .fill { height: 100%; background: var(--orange); }
    .bar-number { font-family: "Playfair Display", Georgia, serif !important; color: var(--orange) !important; font-size: 2.2rem; line-height: 1; }
    .brief-box { white-space: pre-wrap; border: 1px solid var(--black); border-left: 12px solid var(--orange); padding: 2rem; line-height: 1.7; background: var(--white); }
    .small-list { line-height: 1.9; font-size: 1.05rem; }
    .footer-brand { text-align: center; margin-top: 5rem; padding: 4rem 0; border-top: 10px solid var(--orange); border-bottom: 10px solid var(--orange); }
    .footer-signature { font-family: "Great Vibes", cursive !important; font-size: clamp(4.2rem, 10vw, 8rem); line-height: 0.82; color: var(--black) !important; }
    .footer-links a { display: inline-block; border: 1px solid var(--black); border-left: 10px solid var(--orange); padding: 1rem 1.8rem; margin: 1rem 0.5rem; text-decoration: none !important; letter-spacing: 0.18em; text-transform: uppercase; font-weight: 600; color: var(--black) !important; }
    .stButton button, .stDownloadButton button { border: 1px solid var(--black) !important; border-left: 10px solid var(--orange) !important; background: var(--white) !important; border-radius: 0 !important; letter-spacing: 0.14em !important; text-transform: uppercase !important; }
    div[data-baseweb="select"] > div, [data-testid="stFileUploader"] section, textarea { border: 1px solid var(--black) !important; background: var(--white) !important; border-radius: 0 !important; }
    div[data-baseweb="tag"] { background: var(--orange) !important; border: 1px solid var(--black) !important; border-radius: 0 !important; }
    [role="radiogroup"] { gap: 0.7rem; }
    @media (max-width: 900px) {
        .block-container { padding: 1rem 1.25rem 4rem !important; }
        .shell { padding: 2rem 1.6rem; }
        .brand-signature { font-size: 5.2rem; }
        .brand-sub { letter-spacing: 0.28em; font-size: 0.72rem; }
        .metrics-grid, .case-grid { grid-template-columns: 1fr; }
        .identity-panel, .section-panel { padding: 2rem 1.3rem; }
        .body-copy { font-size: 1.07rem; line-height: 1.8; }
        .bar-row { grid-template-columns: 92px 1fr 42px; gap: 0.7rem; }
        .footer-signature { font-size: 5rem; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

uploaded = st.sidebar.file_uploader("Synthetic CSV upload only", type=["csv"])
records, upload_message = parse_csv(uploaded)

risks = sorted(set(row["risk"] for row in records))
payers = sorted(set(row["payer"] for row in records))
domains = sorted(set(row["domain"] for row in records))
lines = sorted(set(row["line"] for row in records))

risk_filter = st.sidebar.multiselect("Filter by risk level", risks, default=risks)
payer_filter = st.sidebar.multiselect("Filter by payer group", payers, default=payers)
domain_filter = st.sidebar.multiselect("Filter by workflow area", domains, default=domains)
line_filter = st.sidebar.multiselect("Filter by service line", lines, default=lines)

filtered = [
    row for row in records
    if row["risk"] in risk_filter
    and row["payer"] in payer_filter
    and row["domain"] in domain_filter
    and row["line"] in line_filter
]

total, high, sla_count, exposure, owner_count, avg_ready = summary(filtered)

st.markdown('<div class="shell">', unsafe_allow_html=True)

st.markdown(
    """
    <div class="brand-signature">Kori Pickle</div>
    <div class="brand-sub">Healthcare Operations<br>Intelligence</div>
    <div class="orange-rule"></div>
    <div class="eyebrow">Kori Pickle • Healthcare Operations Intelligence</div>
    <div class="hero-title">Enterprise<br>Revenue<br><span>Operations</span><br>Platform</div>
    <div class="body-copy">
        A premium synthetic no PHI healthcare operations command center for patient access, eligibility verification, prior authorization pressure tracking, routing intelligence, documentation readiness, denial prevention, payer friction analysis, and responsible operational intelligence.
        <br><br>
        This build functions as an operational review workbench: filter synthetic cases, isolate ownership gaps, simulate stabilization impact, generate escalation language, and build a leadership brief from the active command view.
    </div>
    <div class="badges">
        <div class="badge">No PHI</div>
        <div class="badge">Synthetic Data</div>
        <div class="badge">Human Review Required</div>
        <div class="badge">Built by Kori Pickle</div>
    </div>
    <div class="identity-panel">
        <div class="eyebrow">Operational Identity</div>
        <div class="identity-title">Workflow visibility before revenue damage.</div>
        <div class="body-copy">Designed around one question: where did the workflow first lose control?</div>
        <div class="eyebrow" style="margin-top:2rem">Patient Access • Authorization Control • Documentation Readiness • Denial Prevention</div>
    </div>
    """,
    unsafe_allow_html=True
)

metric_block = (
    metric_html("High Risk Records", high, "Prioritized operational review queue.")
    + metric_html("SLA Pressure", sla_count, "Records aged at or above SLA limit.")
    + metric_html("Synthetic Exposure", money(exposure), "Portfolio simulation only.")
    + metric_html("Readiness Average", avg_ready, "Aggregate workflow readiness score.")
)
st.markdown(f'<div class="metrics-grid">{metric_block}</div>', unsafe_allow_html=True)

nav = st.radio(
    "Platform module",
    [
        "Command Center",
        "Case Review Workbench",
        "Workflow Loss Control Method",
        "Authorization Readiness Engine",
        "Missing Documentation Detector",
        "SLA Countdown",
        "Human Review Log",
        "Executive Brief Builder",
        "About Kori",
        "Stabilization Simulator",
        "2027 API Checklist"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

case_options = [row["id"] for row in filtered] or [row["id"] for row in records]
selected_id = st.selectbox("Select synthetic case for review", case_options)
active_case = next((row for row in records if row["id"] == selected_id), records[0])

if upload_message:
    st.markdown(f'<div class="badge">{esc(upload_message)}</div>', unsafe_allow_html=True)

if nav == "Command Center":
    st.markdown('<div class="section-title">Live Command Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="body-copy">Use the sidebar filters to isolate operational pressure across payer group, workflow domain, service line, and risk level.</div>', unsafe_allow_html=True)
    st.markdown('<div class="case-grid">' + "".join(case_card_html(row) for row in filtered) + '</div>', unsafe_allow_html=True)
    render_table(filtered)
    st.markdown('<div class="section-panel"><div class="eyebrow">Risk Queue Distribution</div>', unsafe_allow_html=True)
    counts = Counter(row["risk"] for row in filtered)
    max_count = max(counts.values()) if counts else 1
    bar_block = "".join(bar_html(label, counts.get(label, 0), max_count) for label in ["High", "Moderate", "Low"])
    st.markdown(bar_block + '</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="section-panel">
            <div class="section-title">Executive Interpretation</div>
            <div class="body-copy">The active view shows {total} synthetic records, {high} high risk records, {sla_count} SLA pressure signals, {owner_count} distinct owners, average readiness of {avg_ready}, and {money(exposure)} in simulated exposure. These are prioritization signals for human review, not automated payer or clinical decisions.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

elif nav == "Case Review Workbench":
    docs = missing_docs(active_case)
    miss = ", ".join(docs) if docs else "None detected"
    remaining, sla_label, timing = sla_status(active_case)
    factors, ar_score, ar_status = auth_readiness(active_case)
    st.markdown('<div class="section-title">Case Review Workbench</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="section-panel">
            <div class="eyebrow">{esc(active_case["id"])} • {esc(active_case["risk"])} Risk</div>
            <div class="identity-title">{esc(active_case["domain"])}</div>
            <div class="small-list">
                <b>Payer Group:</b> {esc(active_case["payer"])}<br>
                <b>Service Line:</b> {esc(active_case["line"])}<br>
                <b>Assigned Owner:</b> {esc(active_case["owner"])}<br>
                <b>Days Open:</b> {esc(active_case["days"])}<br>
                <b>SLA Status:</b> {esc(sla_label)}<br>
                <b>Missing Documentation:</b> {esc(miss)}<br>
                <b>Readiness Score:</b> {esc(readiness_score(active_case))}<br>
                <b>Control Loss Domain:</b> {esc(first_failed_domain(active_case))}<br>
                <b>Recommended Next Action:</b> {esc(active_case["action"])}<br>
                <b>Escalation Language:</b> Please review {esc(active_case["id"])} because the case is showing {esc(sla_label.lower())} status, {esc(active_case["risk"].lower())} risk, and documentation or routing gaps requiring human review before further workflow movement.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    note = st.text_area("Human review note", value=f"Reviewed {active_case['id']}. Next action assigned to {active_case['owner']}.")
    st.download_button("Download case review note", note, file_name=f"{active_case['id']}_human_review_note.txt")

elif nav == "Workflow Loss Control Method":
    scores = wlcm_scores(active_case)
    st.markdown('<div class="section-title">Workflow Loss Control Method™</div>', unsafe_allow_html=True)
    st.markdown('<div class="body-copy">This method identifies where the workflow first lost control before the issue becomes denial activity, access delay, rework burden, or revenue leakage.</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-panel"><div class="eyebrow">Five Control Domains</div>', unsafe_allow_html=True)
    st.markdown("".join(bar_html(domain, int(scores[domain]), 100) for domain in CONTROL_DOMAINS) + '</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="section-panel">
            <div class="eyebrow">Selected Case Output</div>
            <div class="small-list">
                <b>First Failed Control Domain:</b> {esc(first_failed_domain(active_case))}<br>
                <b>Current Operational Risk:</b> {esc(active_case["risk"])}<br>
                <b>Next Owner:</b> {esc(active_case["owner"])}<br>
                <b>Required Action:</b> {esc(active_case["action"])}<br>
                <b>Stability Status:</b> {esc(stability_status(active_case))}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

elif nav == "Authorization Readiness Engine":
    factors, ar_score, ar_status = auth_readiness(active_case)
    st.markdown('<div class="section-title">Authorization Readiness Engine</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-panel"><div class="eyebrow">Readiness Output</div><div class="metric-number">{ar_score}</div><div class="body-copy">Status: {esc(ar_status)}</div></div>', unsafe_allow_html=True)
    factor_cards = "".join(
        f'<div class="case-card"><div class="eyebrow">{esc(factor)}</div><div class="case-row">{"Complete" if result else "Needs Review"}</div></div>'
        for factor, result in factors.items()
    )
    st.markdown('<div class="case-grid">' + factor_cards + '</div>', unsafe_allow_html=True)

elif nav == "Missing Documentation Detector":
    st.markdown('<div class="section-title">Missing Documentation Detector</div>', unsafe_allow_html=True)
    docs = missing_docs(active_case)
    impact = "Authorization readiness is reduced because required documentation is missing from the operational packet." if docs else "No missing documentation detected in this synthetic case."
    st.markdown(
        f"""
        <div class="section-panel">
            <div class="eyebrow">{esc(active_case["id"])}</div>
            <div class="small-list">
                <b>Missing:</b> {esc(", ".join(docs) if docs else "None detected")}<br>
                <b>Documentation Gap Summary:</b> {esc(active_case["rule"])}<br>
                <b>Operational Impact:</b> {esc(impact)}<br>
                <b>Next Action:</b> {esc(active_case["action"])}<br>
                <b>Owner:</b> {esc(active_case["owner"])}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

elif nav == "SLA Countdown":
    remaining, sla_label, timing = sla_status(active_case)
    days = int(active_case["days"])
    sla = int(active_case["sla"])
    past = max(0, days - sla)
    st.markdown('<div class="section-title">SLA Breach Countdown</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="section-panel">
            <div class="eyebrow">{esc(active_case["id"])}</div>
            <div class="small-list">
                <b>SLA Status:</b> {esc(sla_label)}<br>
                <b>Days Open:</b> {esc(days)}<br>
                <b>SLA Limit:</b> {esc(sla)}<br>
                <b>Days Remaining:</b> {esc(remaining)}<br>
                <b>Days Past SLA:</b> {esc(past)}<br>
                <b>Escalation Timing:</b> {esc(timing)}<br>
                <b>Action:</b> {esc(active_case["action"])}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

elif nav == "Human Review Log":
    st.markdown('<div class="section-title">Human Review Log</div>', unsafe_allow_html=True)
    reviewer = st.text_input("Reviewer name", value="Kori Pickle")
    action_taken = st.selectbox("Action taken", ["Documentation request", "Eligibility review", "Payer follow up", "Routing correction", "Escalation", "Monitor"])
    decision_status = st.selectbox("Decision status", ["Open", "In Review", "Escalated", "Stabilized", "Closed"])
    escalation = st.selectbox("Escalation required", ["Yes", "No"])
    follow_up = st.date_input("Follow-up date")
    notes = st.text_area("Notes", value=f"{active_case['id']} reviewed. Assigned owner: {active_case['owner']}. Next action: {active_case['action']}")
    log_text = f"""Human Review Log
Reviewer: {reviewer}
Review Date: {date.today().isoformat()}
Case ID: {active_case["id"]}
Action Taken: {action_taken}
Decision Status: {decision_status}
Notes: {notes}
Escalation Required: {escalation}
Follow-up Date: {follow_up}
"""
    st.markdown(f'<div class="brief-box">{esc(log_text)}</div>', unsafe_allow_html=True)
    st.download_button("Download human review log", log_text, file_name=f"{active_case['id']}_human_review_log.txt")

elif nav == "Executive Brief Builder":
    st.markdown('<div class="section-title">Executive Brief Builder</div>', unsafe_allow_html=True)
    brief_text = executive_brief(filtered)
    st.markdown(f'<div class="brief-box">{esc(brief_text)}</div>', unsafe_allow_html=True)
    st.download_button("Download executive brief", brief_text, file_name="enterprise_revenue_operations_brief.txt")

elif nav == "About Kori":
    st.markdown('<div class="section-title">About Kori</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-panel">
            <div class="eyebrow">Professional Portfolio Statement</div>
            <div class="body-copy">
                Kori Pickle is a BSHA candidate focused on healthcare operations, revenue cycle workflow analysis, patient access, prior authorization, denial prevention, documentation readiness, and operational visibility.
                <br><br>
                Her work is shaped by a patient-to-professional perspective and a practical interest in how healthcare systems can identify workflow breakdowns earlier, assign ownership more clearly, and reduce avoidable rework before it becomes patient access friction or downstream revenue cycle damage.
                <br><br>
                This portfolio platform demonstrates healthcare administration thinking through synthetic operational data, workflow review logic, responsible human oversight, and leadership-ready reporting.
            </div>
        </div>
        <div class="section-panel">
            <div class="eyebrow">Why This Tool Exists</div>
            <div class="body-copy">
                Most revenue cycle issues appear downstream, but many begin upstream in patient access, eligibility verification, authorization readiness, documentation completeness, payer routing, and ownership gaps.
                <br><br>
                This platform demonstrates how synthetic operational data can be used to identify where workflow control was lost before the issue becomes a denial, delay, rework burden, or patient access problem.
            </div>
        </div>
        <div class="section-panel">
            <div class="eyebrow">Portfolio Use Statement</div>
            <div class="body-copy">
                This platform is a synthetic portfolio demonstration. It does not process PHI, make payer decisions, make billing determinations, make coding decisions, or provide clinical recommendations.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

elif nav == "Stabilization Simulator":
    st.markdown('<div class="section-title">Before-and-After Stabilization Simulator</div>', unsafe_allow_html=True)
    doc_gain = st.slider("Documentation completion improvement", 0, 50, 20)
    sla_gain = st.slider("SLA follow-up improvement", 0, 50, 15)
    routing_gain = st.slider("Routing accuracy improvement", 0, 50, 10)
    current_risk = high + sla_count
    projected_risk = max(0, round(current_risk * (1 - (doc_gain + sla_gain + routing_gain) / 220)))
    projected_exposure = max(0, round(exposure * (1 - (doc_gain + sla_gain + routing_gain) / 250)))
    sim_metrics = (
        metric_html("Current Pressure", current_risk, "Current combined risk and SLA signals.")
        + metric_html("Projected Pressure", projected_risk, "After stabilization inputs.")
        + metric_html("Current Exposure", money(exposure), "Synthetic simulation only.")
        + metric_html("Projected Exposure", money(projected_exposure), "Estimated stabilized exposure.")
    )
    st.markdown(f'<div class="metrics-grid">{sim_metrics}</div>', unsafe_allow_html=True)

elif nav == "2027 API Checklist":
    st.markdown('<div class="section-title">2027 API Readiness Checklist</div>', unsafe_allow_html=True)
    items = [
        "Synthetic data standard documented",
        "No PHI processing in public portfolio environment",
        "Human review requirement displayed",
        "Case ownership field available",
        "SLA field available",
        "Missing documentation field available",
        "Payer rule field available",
        "CSV import validation available",
        "Executive brief export available",
        "Workflow Loss Control Method available",
        "Clear disclaimer against clinical, payer, billing, or coding decisions"
    ]
    checklist_cards = "".join(
        f'<div class="case-card"><div class="eyebrow">Ready Signal</div><div class="case-row">{esc(item)}</div></div>'
        for item in items
    )
    st.markdown('<div class="case-grid">' + checklist_cards + '</div>', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="footer-brand">
        <div class="eyebrow">Created by Kori Pickle</div>
        <div class="footer-signature">Kori Pickle</div>
        <div class="body-copy" style="margin:auto">Healthcare Operations Intelligence • Revenue Cycle • Patient Access • Prior Authorization • Denial Prevention</div>
        <div class="footer-links">
            <a href="{LINKEDIN_URL}" target="_blank">LinkedIn</a>
            <a href="{GITHUB_URL}" target="_blank">GitHub</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)
