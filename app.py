import csv
import html
from datetime import date
from io import StringIO
from collections import Counter
import streamlit as st

st.set_page_config(
    page_title="Kori Pickle Healthcare Operations Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed"
)

TENNESSEE_ORANGE = "#FF8200"
BLACK = "#000000"
WHITE = "#FFFFFF"
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
    "Case ID":"id", "Payer Group":"payer", "Workflow Domain":"domain", "Service Line":"line", "Risk":"risk", "Owner":"owner",
    "Days Open":"days", "SLA Limit":"sla", "Exposure":"exposure", "Status":"status", "Required Docs":"required", "Present Docs":"present",
    "First Control Loss":"loss", "Payer Rule":"rule", "Next Action":"action"
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
    return round(max(0, min(100, 100 - missing * 13 - overdue * 8 - risk_penalty)), 1)

def wlcm_scores(case):
    scores = {domain: 86 for domain in CONTROL_DOMAINS}
    loss = case.get("loss", "None")
    if loss in scores:
        scores[loss] -= 32
    if case.get("domain") in ["Patient Access", "Eligibility Verification", "Financial Clearance"]:
        scores["Access Control"] -= 12
    scores["Documentation Control"] -= len(missing_docs(case)) * 9
    if case.get("domain") == "Authorization Control":
        scores["Authorization Control"] -= 16
    if case.get("domain") == "Routing Intelligence":
        scores["Routing Control"] -= 18
    overdue = max(0, int(case.get("days", 0)) - int(case.get("sla", 5)))
    scores["Follow-Up Control"] -= overdue * 10
    return {key: max(0, min(100, round(value, 1))) for key, value in scores.items()}

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
    present = split_items(case.get("present", ""))
    factors = {
        "Eligibility verified": any(x in present for x in ["Eligibility Response", "Benefit Check"]),
        "Benefit checked": "Benefit Check" in present,
        "Service requirement reviewed": any(x in present for x in ["Procedure Code", "Site of Service"]),
        "Clinical note present": any(x in present for x in ["Clinical Note", "Cardiology Note", "Neuro Exam", "Surgical Note", "Assessment"]),
        "Medical necessity support present": "Medical Necessity Note" in present,
        "Prior therapy history present when required": any(x in present for x in ["Prior Therapy History", "Failed Conservative Therapy", "Failed Therapy Evidence"]) or "Therapy" not in case.get("required", ""),
        "Payer route confirmed": "Payer Route" in present or case.get("domain") != "Routing Intelligence",
        "Submission owner assigned": bool(case.get("owner", "")),
        "Follow-up window documented": int(case.get("days", 0)) <= int(case.get("sla", 5))
    }
    met = sum(1 for value in factors.values() if value)
    score = round(met / len(factors) * 100, 1)
    status = "Ready" if score >= 85 else "Needs Review" if score >= 65 else "Escalate" if case.get("risk") == "High" else "Not Ready"
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
        return DEFAULT_DATA, "Default synthetic data active."
    try:
        raw = uploaded.getvalue().decode("utf-8")
        reader = csv.DictReader(StringIO(raw))
        rows = []
        for row in reader:
            item = {internal: row.get(external, row.get(internal, "")) for external, internal in REQUIRED_COLUMNS.items()}
            for key in ["days", "sla", "exposure"]:
                try:
                    item[key] = int(float(item[key]))
                except Exception:
                    item[key] = 0
            if item.get("id"):
                rows.append(item)
        return (rows, "Synthetic CSV loaded. Validation passed.") if rows else (DEFAULT_DATA, "CSV did not include valid synthetic case rows. Default synthetic data active.")
    except Exception:
        return DEFAULT_DATA, "CSV could not be read. Default synthetic data active."

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
    return Counter(values).most_common(1)[0][0] if values else "None"

def common_missing(rows):
    docs = []
    for row in rows:
        docs.extend(missing_docs(row))
    return Counter(docs).most_common(1)[0][0] if docs else "None detected"

def executive_brief(rows):
    total, high, sla, exposure, owners, avg_ready = summary(rows)
    return f"""Kori Pickle Healthcare Operations Intelligence
Enterprise Revenue Operations Platform
Generated {date.today().isoformat()}

Synthetic Data Standard
This platform uses synthetic records only. It does not process PHI, make payer decisions, make billing determinations, make coding decisions, or provide clinical recommendations.

Current Command View
Total synthetic records reviewed: {total}
High risk records: {high}
SLA pressure signals: {sla}
Average readiness score: {avg_ready}
Simulated exposure: {money(exposure)}
Distinct operational owners: {owners}
Top workflow failure domain: {most_common(rows, 'loss')}
Most common missing documentation item: {common_missing(rows)}
Highest pressure payer group: {most_common(rows, 'payer')}

Leadership Action
Prioritize cases where documentation readiness, authorization control, routing control, and follow-up control are unstable. Assign a human owner, confirm missing items, document the next action, and escalate records that are at or past the SLA threshold.

Signature Method
Workflow Loss Control Method asks: Where did the workflow first lose control?
"""

def render_html(markup):
    st.html(str(markup).strip())

def chip(text):
    return f'<span class="chip">{esc(text)}</span>'

def metric_card(label, value, note):
    return f'<div class="metric-card"><div class="eyebrow">{esc(label)}</div><div class="metric-number">{esc(value)}</div><div class="metric-note">{esc(note)}</div></div>'

def case_card(case):
    miss_text = ", ".join(missing_docs(case)) if missing_docs(case) else "None detected"
    return f'<div class="case-card"><div class="case-title">{esc(case["id"])}</div><div class="case-meta">{esc(case["risk"])} • {esc(case["payer"])} • {esc(case["domain"])} • {esc(case["line"])}</div><div class="case-row"><strong>Owner:</strong> {esc(case["owner"])}</div><div class="case-row"><strong>Missing:</strong> {esc(miss_text)}</div><div class="case-row"><strong>Control Status:</strong> {esc(stability_status(case))}</div><div class="case-row"><strong>Next:</strong> {esc(case["action"])}</div></div>'

def progress_row(label, value, max_value):
    pct = 0 if max_value == 0 else round(value / max_value * 100, 1)
    return f'<div class="bar-row"><div class="bar-label">{esc(label)}</div><div class="track"><div class="fill" style="width:{pct}%"></div></div><div class="bar-number">{esc(value)}</div></div>'

def record_table(rows):
    body = ""
    for row in rows:
        _, sla_label, _ = sla_status(row)
        body += f'<tr><td>{esc(row["id"])}</td><td>{esc(row["payer"])}</td><td>{esc(row["domain"])}</td><td>{esc(row["line"])}</td><td>{esc(row["risk"])}</td><td>{esc(row["owner"])}</td><td>{esc(sla_label)}</td><td>{readiness_score(row)}</td></tr>'
    return '<div class="table-scroll"><table class="ops-table"><tr><th>Case ID</th><th>Payer Group</th><th>Workflow Domain</th><th>Service Line</th><th>Risk</th><th>Owner</th><th>SLA</th><th>Readiness</th></tr>' + body + '</table></div>'

render_html(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Allura&family=Cormorant+Garamond:wght@300;400&family=Inter:wght@300;400;500;600;700&display=swap');
:root{{--orange:{TENNESSEE_ORANGE};--black:{BLACK};--white:{WHITE};}}
html,body,[data-testid="stAppViewContainer"],[data-testid="stHeader"]{{background:var(--white)!important;color:var(--black)!important;overflow-x:hidden!important;}}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"],#MainMenu,footer,button[title="View fullscreen"],button[title="Exit fullscreen"],[data-testid="collapsedControl"]{{visibility:hidden!important;height:0!important;display:none!important;}}
*{{box-sizing:border-box!important;}}
.block-container{{max-width:1040px!important;padding:2rem 2.4rem 5rem!important;overflow-x:hidden!important;}}
[data-testid="stVerticalBlock"], .element-container{{max-width:100%!important;}}
p,li,div,label,span{{font-family:'Inter',sans-serif;color:var(--black);}}
h1,h2,h3{{font-family:'Cormorant Garamond',Georgia,serif!important;font-weight:300!important;color:var(--black)!important;}}
.main-frame{{border-left:2px solid var(--black);border-right:2px solid var(--black);padding:2.2rem 2.6rem 4rem;background:var(--white);overflow:hidden;}}
.signature-lockup{{border-top:12px solid var(--orange);border-bottom:7px solid var(--orange);padding:2.4rem 0;margin:0 0 4rem;overflow:hidden;}}
.signature-name{{font-family:'Allura',cursive;font-size:clamp(5.2rem,13vw,10rem);line-height:.72;color:var(--black);letter-spacing:-.035em;white-space:normal;overflow-wrap:normal;}}
.signature-sub{{font-size:clamp(.9rem,1.9vw,1.15rem);letter-spacing:.56em;text-transform:uppercase;margin-top:1.5rem;font-weight:400;}}
.signature-intel{{color:var(--orange);letter-spacing:.7em;text-transform:uppercase;margin-top:1rem;font-size:clamp(.85rem,1.8vw,1.05rem);}}
.eyebrow{{font-size:.82rem;text-transform:uppercase;letter-spacing:.42em;font-weight:700;margin-bottom:1.05rem;line-height:1.8;}}
.hero-title{{font-family:'Cormorant Garamond',Georgia,serif;font-weight:300;font-size:clamp(5rem,11vw,9rem);line-height:.82;letter-spacing:-.065em;margin:2.3rem 0;max-width:900px;overflow-wrap:normal;}}
.orange{{color:var(--orange);}}
.lead{{font-size:clamp(1.16rem,2vw,1.55rem);line-height:1.72;font-weight:300;max-width:880px;margin:1.8rem 0;}}
.chip-wrap{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin:2.5rem 0 4rem;max-width:760px;}}
.chip{{display:flex;align-items:center;border:1.5px solid var(--black);border-left:15px solid var(--orange);min-height:56px;padding:0 1.2rem;font-size:.82rem;letter-spacing:.28em;text-transform:uppercase;font-weight:700;background:var(--white);overflow:hidden;}}
.identity-card,.section-card{{border:1.5px solid var(--black);border-top:10px solid var(--orange);padding:clamp(2rem,4.5vw,4rem);margin:3.2rem 0;background:var(--white);overflow:hidden;}}
.identity-head{{font-family:'Cormorant Garamond',Georgia,serif;font-size:clamp(3.1rem,7vw,6rem);line-height:.9;letter-spacing:-.06em;font-weight:300;margin:1rem 0 2rem;}}
.orange-rule{{width:min(420px,72%);height:6px;background:var(--orange);margin:2rem 0;}}
.identity-copy{{font-size:clamp(1.18rem,2.2vw,1.5rem);line-height:1.65;font-weight:300;}}
.domain-line{{font-size:.94rem;letter-spacing:.32em;text-transform:uppercase;font-weight:700;line-height:2;margin-top:2rem;}}
.metric-grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1rem;align-items:stretch;margin:3rem 0 3.5rem;}}
.metric-card{{border:1.5px solid var(--black);border-left:15px solid var(--orange);padding:1.8rem 1.35rem;min-height:220px;height:220px;background:var(--white);overflow:hidden;display:flex;flex-direction:column;justify-content:center;}}
.metric-number{{font-family:'Cormorant Garamond',Georgia,serif;color:var(--orange);font-weight:300;letter-spacing:-.055em;font-size:clamp(3.6rem,6.8vw,5.8rem);line-height:.9;margin:.5rem 0 .9rem;white-space:nowrap;}}
.metric-note{{font-size:1rem;line-height:1.42;font-weight:300;}}
.module-title{{font-family:'Cormorant Garamond',Georgia,serif;font-size:clamp(3.8rem,8vw,7rem);line-height:.9;letter-spacing:-.065em;font-weight:300;margin:3rem 0 1.6rem;}}
.case-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin:2rem 0;align-items:stretch;}}
.case-card{{border:1.5px solid var(--black);border-left:14px solid var(--orange);padding:1.55rem;min-height:310px;height:310px;background:var(--white);overflow:hidden;}}
.case-title{{font-family:'Cormorant Garamond',Georgia,serif;font-size:clamp(3rem,5.5vw,4.8rem);line-height:.9;letter-spacing:-.055em;font-weight:300;margin-bottom:.9rem;white-space:nowrap;}}
.case-meta{{font-size:.74rem;letter-spacing:.24em;text-transform:uppercase;font-weight:700;margin-bottom:.85rem;line-height:1.6;white-space:normal;overflow:hidden;}}
.case-row{{font-size:.96rem;line-height:1.5;margin:.55rem 0;overflow:hidden;}}
.table-scroll{{overflow-x:auto;border:1.5px solid var(--black);margin:2rem 0 3rem;width:100%;background:var(--white);}}
.ops-table{{width:100%;min-width:920px;border-collapse:collapse;table-layout:fixed;}}
.ops-table th{{background:var(--orange);color:var(--black);text-align:left;font-size:.75rem;letter-spacing:.22em;text-transform:uppercase;padding:1rem;border:1px solid var(--black);}}
.ops-table td{{padding:1rem;border:1px solid var(--black);font-size:.93rem;line-height:1.35;vertical-align:top;overflow-wrap:anywhere;}}
.bar-box{{border:1.5px solid var(--black);border-top:10px solid var(--orange);padding:2rem;margin:2.4rem 0;background:var(--white);overflow:hidden;}}
.bar-row{{display:grid;grid-template-columns:130px 1fr 58px;gap:1rem;align-items:center;margin:1.2rem 0;}}
.bar-label{{font-size:1.15rem;font-weight:300;}}
.track{{border:1.5px solid var(--black);height:26px;background:var(--white);}}
.fill{{height:100%;background:var(--orange);}}
.bar-number{{font-family:'Cormorant Garamond',Georgia,serif;font-size:2.8rem;color:var(--orange);font-weight:300;line-height:1;}}
.footer-lockup{{text-align:center;border-top:8px solid var(--orange);border-bottom:8px solid var(--orange);padding:3rem 0;margin-top:5rem;overflow:hidden;}}
.footer-signature{{font-family:'Allura',cursive;font-size:clamp(3.8rem,10vw,7rem);line-height:.8;letter-spacing:-.035em;}}
.footer-text{{font-size:1.05rem;line-height:1.65;max-width:720px;margin:1rem auto;}}
.footer-links{{display:flex;justify-content:center;gap:1rem;flex-wrap:wrap;margin-top:2rem;}}
.footer-link{{border:1.5px solid var(--black);border-left:14px solid var(--orange);padding:1rem 1.6rem;text-decoration:none!important;color:var(--black)!important;letter-spacing:.25em;text-transform:uppercase;font-weight:700;}}
pre,code{{background:var(--white)!important;color:var(--black)!important;border:1.5px solid var(--orange)!important;}}
.stButton>button,.stDownloadButton>button{{background:var(--white)!important;color:var(--black)!important;border:1.5px solid var(--black)!important;border-left:14px solid var(--orange)!important;border-radius:0!important;font-weight:700!important;letter-spacing:.12em!important;text-transform:uppercase!important;}}
.stSelectbox div[data-baseweb="select"],.stMultiSelect div[data-baseweb="select"],.stTextArea textarea,.stTextInput input,.stNumberInput input{{border-radius:0!important;border:1.5px solid var(--black)!important;background:var(--white)!important;color:var(--black)!important;}}
@media(max-width:900px){{
.block-container{{padding:1rem .82rem 3rem!important;}}
.main-frame{{padding:1.05rem .9rem 2.5rem;border-left:1.5px solid var(--black);border-right:1.5px solid var(--black);}}
.signature-lockup{{padding:2rem 0;margin-bottom:3rem;}}
.signature-name{{font-size:clamp(4.1rem,16vw,5.8rem);line-height:.78;}}
.signature-sub,.signature-intel{{letter-spacing:.34em;font-size:.78rem;}}
.eyebrow{{font-size:.7rem;letter-spacing:.3em;}}
.hero-title{{font-size:clamp(4.0rem,15vw,5.7rem);line-height:.86;}}
.lead{{font-size:1.05rem;line-height:1.7;}}
.chip-wrap{{grid-template-columns:1fr;gap:.75rem;margin-bottom:3rem;}}
.chip{{min-height:48px;font-size:.66rem;letter-spacing:.24em;padding:0 .9rem;}}
.identity-card,.section-card{{padding:1.7rem 1.15rem;margin:2.4rem 0;}}
.identity-head{{font-size:clamp(3rem,12vw,4.6rem);}}
.domain-line{{font-size:.76rem;letter-spacing:.24em;}}
.metric-grid{{grid-template-columns:1fr;gap:1rem;}}
.metric-card{{height:188px;min-height:188px;padding:1.45rem 1.25rem;}}
.metric-number{{font-size:4.1rem;}}
.module-title{{font-size:clamp(3.4rem,13vw,5rem);line-height:.92;}}
.case-grid{{grid-template-columns:1fr;gap:1rem;}}
.case-card{{height:300px;min-height:300px;padding:1.35rem 1.15rem;}}
.case-title{{font-size:3.45rem;}}
.case-meta{{font-size:.66rem;letter-spacing:.2em;}}
.case-row{{font-size:.92rem;}}
.bar-row{{grid-template-columns:82px 1fr 42px;gap:.7rem;}}
.track{{height:22px;}}
.bar-number{{font-size:2.15rem;}}
.footer-signature{{font-size:4.1rem;}}
}}
</style>
""")

render_html('<div class="main-frame"><div class="signature-lockup"><div class="signature-name">Kori Pickle</div><div class="signature-sub">Healthcare Operations</div><div class="signature-intel">Intelligence</div></div><div class="eyebrow">Kori Pickle • Healthcare Operations Intelligence</div><div class="hero-title">Enterprise<br>Revenue<br><span class="orange">Operations</span><br>Platform</div><div class="lead">A premium synthetic no PHI healthcare operations command center for patient access, eligibility verification, prior authorization pressure tracking, routing intelligence, documentation readiness, denial prevention, payer friction analysis, and responsible operational intelligence.</div><div class="lead">This build functions as an operational review workbench: filter synthetic cases, isolate ownership gaps, simulate stabilization impact, generate escalation language, and build a leadership brief from the active command view.</div><div class="chip-wrap"><span class="chip">No PHI</span><span class="chip">Synthetic Data</span><span class="chip">Human Review Required</span><span class="chip">Built by Kori Pickle</span></div><div class="identity-card"><div class="eyebrow">Operational Identity</div><div class="identity-head">Workflow visibility before revenue damage.</div><div class="orange-rule"></div><div class="identity-copy">Designed around one question: where did the workflow first lose control?</div><div class="domain-line">Patient Access • Authorization Control • Documentation Readiness • Denial Prevention</div></div></div>')

uploaded = st.file_uploader("Synthetic CSV upload only", type=["csv"], label_visibility="collapsed")
rows, upload_message = parse_csv(uploaded)
st.caption(upload_message)

all_risks = sorted({row["risk"] for row in rows})
all_payers = sorted({row["payer"] for row in rows})
all_domains = sorted({row["domain"] for row in rows})
all_lines = sorted({row["line"] for row in rows})

with st.expander("Command Filters", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        selected_risks = st.multiselect("Filter by risk level", all_risks, default=all_risks)
        selected_domains = st.multiselect("Filter by workflow area", all_domains, default=all_domains)
    with c2:
        selected_payers = st.multiselect("Filter by payer group", all_payers, default=all_payers)
        selected_lines = st.multiselect("Filter by service line", all_lines, default=all_lines)

filtered_rows = [row for row in rows if row["risk"] in selected_risks and row["payer"] in selected_payers and row["domain"] in selected_domains and row["line"] in selected_lines]
if not filtered_rows:
    filtered_rows = rows

total, high, sla, exposure, owners, avg_ready = summary(filtered_rows)
render_html('<div class="main-frame"><div class="metric-grid">' + metric_card("High Risk Records", high, "Prioritized operational review queue.") + metric_card("SLA Pressure", sla, "Records aged at or above SLA limit.") + metric_card("Synthetic Exposure", money(exposure), "Portfolio simulation only.") + metric_card("Readiness Average", avg_ready, "Aggregate workflow readiness score.") + '</div></div>')

modules = ["Command Center", "Case Review Workbench", "Workflow Loss Control Method", "Authorization Readiness Engine", "Missing Documentation Detector", "SLA Countdown", "Human Review Log", "Executive Brief Builder", "About Kori", "Stabilization Simulator", "2027 API Checklist"]
module = st.selectbox("Select module", modules, index=0)
case_ids = [row["id"] for row in filtered_rows]
selected_id = st.selectbox("Select synthetic case for review", case_ids, index=0)
selected_case = next(row for row in filtered_rows if row["id"] == selected_id)

render_html('<div class="main-frame">')

if module == "Command Center":
    render_html('<div class="module-title">Live Command Center</div><div class="lead">Use the filters above to isolate operational pressure across payer group, workflow domain, service line, and risk level.</div>')
    render_html('<div class="case-grid">' + ''.join(case_card(row) for row in filtered_rows) + '</div>')
    render_html(record_table(filtered_rows))
    risk_counts = Counter(row["risk"] for row in filtered_rows)
    max_risk = max(risk_counts.values()) if risk_counts else 1
    render_html('<div class="bar-box"><div class="eyebrow">Risk Queue Distribution</div>' + ''.join(progress_row(label, risk_counts.get(label, 0), max_risk) for label in ["High", "Moderate", "Low"]) + '</div>')
    render_html(f'<div class="section-card"><div class="module-title" style="margin-top:0;">Executive Interpretation</div><div class="identity-copy">The active view shows {total} synthetic records, {high} high risk records, {sla} SLA pressure signals, {owners} distinct owners, average readiness of {avg_ready}, and {money(exposure)} in simulated exposure. These are prioritization signals for human review, not automated payer or clinical decisions.</div></div>')

elif module == "Case Review Workbench":
    remaining, sla_label, timing = sla_status(selected_case)
    render_html('<div class="module-title">Case Review Workbench</div>' + case_card(selected_case) + f'<div class="section-card"><div class="eyebrow">Selected Case Operating Pathway</div><div class="case-row"><strong>What failed:</strong> {esc(first_failed_domain(selected_case))}</div><div class="case-row"><strong>Where it failed:</strong> {esc(selected_case["domain"])}</div><div class="case-row"><strong>Why it matters:</strong> {esc(selected_case["rule"])}</div><div class="case-row"><strong>Who owns it:</strong> {esc(selected_case["owner"])}</div><div class="case-row"><strong>SLA status:</strong> {esc(sla_label)} • {abs(remaining)} day(s) {"past SLA" if remaining < 0 else "remaining"}</div><div class="case-row"><strong>Escalation timing:</strong> {esc(timing)}</div><div class="case-row"><strong>Leadership should know:</strong> This record needs human review because workflow control is unstable before downstream revenue or access impact occurs.</div></div>')
    note = st.text_area("Human review note", placeholder="Document reviewer observation, action taken, escalation status, and follow-up date.")
    if note:
        st.success("Human review note captured for this session. Do not enter PHI.")

elif module == "Workflow Loss Control Method":
    scores = wlcm_scores(selected_case)
    render_html('<div class="module-title">Workflow Loss Control Method™</div><div class="lead">Kori Pickle’s original method identifies where front-end revenue cycle control was first lost before the issue becomes a denial, access delay, rework burden, or payer escalation.</div><div class="bar-box"><div class="eyebrow">Five Control Domains</div>' + ''.join(progress_row(domain, int(score), 100) for domain, score in scores.items()) + f'</div><div class="section-card"><div class="case-row"><strong>First failed control domain:</strong> {esc(first_failed_domain(selected_case))}</div><div class="case-row"><strong>Stability status:</strong> {esc(stability_status(selected_case))}</div><div class="case-row"><strong>Required action:</strong> {esc(selected_case["action"])}</div></div>')

elif module == "Authorization Readiness Engine":
    factors, score, status = auth_readiness(selected_case)
    rows_html = ''.join(f'<div class="case-row"><strong>{esc(name)}:</strong> {"Met" if value else "Gap"}</div>' for name, value in factors.items())
    render_html('<div class="module-title">Authorization Readiness Engine</div>' + metric_card("Authorization Readiness", f"{score}%", status) + f'<div class="section-card"><div class="eyebrow">Readiness Factors</div>{rows_html}</div>')

elif module == "Missing Documentation Detector":
    missing = missing_docs(selected_case)
    render_html('<div class="module-title">Missing Documentation Detector</div>')
    if missing:
        render_html('<div class="section-card"><div class="eyebrow">Detected Documentation Gaps</div><div class="chip-wrap">' + ''.join(chip(item) for item in missing) + f'</div><div class="lead">Operational impact: {esc(selected_case["rule"])}</div><div class="case-row"><strong>Next action:</strong> {esc(selected_case["action"])}</div><div class="case-row"><strong>Owner:</strong> {esc(selected_case["owner"])}</div></div>')
    else:
        render_html('<div class="section-card"><div class="identity-copy">No missing documentation detected for this synthetic case.</div></div>')

elif module == "SLA Countdown":
    remaining, sla_label, timing = sla_status(selected_case)
    render_html('<div class="module-title">SLA Breach Countdown</div><div class="metric-grid">' + metric_card("Days Open", selected_case["days"], "Current aging") + metric_card("SLA Limit", selected_case["sla"], "Operational threshold") + metric_card("SLA Status", sla_label, timing) + metric_card("Days Delta", abs(remaining), "Past SLA" if remaining < 0 else "Remaining") + '</div>')

elif module == "Human Review Log":
    render_html('<div class="module-title">Human Review Log</div>')
    reviewer = st.text_input("Reviewer name", value="Kori Pickle")
    action_taken = st.selectbox("Action taken", ["Documentation request", "Eligibility follow-up", "Payer route correction", "Authorization escalation", "Ready for submission", "Leadership escalation"])
    decision_status = st.selectbox("Decision status", ["Open", "In Review", "Escalated", "Completed"])
    notes = st.text_area("Review notes", placeholder="Use synthetic details only. Do not enter PHI.")
    follow_date = st.date_input("Follow-up date")
    st.download_button("Download Human Review Log Entry", f"Reviewer: {reviewer}\nDate: {date.today()}\nCase: {selected_case['id']}\nAction: {action_taken}\nStatus: {decision_status}\nNotes: {notes}\nFollow up: {follow_date}\n", file_name="human_review_log_entry.txt")

elif module == "Executive Brief Builder":
    brief = executive_brief(filtered_rows)
    render_html('<div class="module-title">Executive Brief Builder</div>')
    st.text_area("Leadership brief generated from the active command view", brief, height=420)
    st.download_button("Download Executive Brief", brief, file_name="kori_pickle_executive_brief.txt")

elif module == "About Kori":
    render_html('<div class="module-title">About Kori</div><div class="section-card"><div class="eyebrow">Professional Portfolio Positioning</div><div class="identity-copy">Kori Pickle is a BSHA candidate focused on healthcare operations, revenue cycle workflow analysis, patient access, prior authorization readiness, denial prevention, documentation readiness, health informatics, and workflow visibility. Her work is shaped by a patient-to-professional perspective and a practical interest in how upstream operational breakdowns become downstream delays, rework, denials, and patient access friction.</div><div class="orange-rule"></div><div class="case-row"><strong>Current academic standing:</strong> 99 of 120 credits completed • GPA 3.6</div><div class="case-row"><strong>Core focus:</strong> healthcare operations intelligence, front-end revenue cycle control, authorization readiness, workflow stabilization, responsible human review</div><div class="case-row"><strong>Portfolio statement:</strong> This public platform demonstrates synthetic operational logic only. It does not process PHI or replace payer, billing, coding, or clinical judgment.</div></div>')

elif module == "Stabilization Simulator":
    closure_gain = st.slider("Documentation gap closure target", 0, 100, 45)
    follow_gain = st.slider("Follow-up reliability improvement", 0, 100, 35)
    new_score = min(100, round(avg_ready + closure_gain * 0.28 + follow_gain * 0.18, 1))
    avoided = int(exposure * (new_score - avg_ready) / 100)
    render_html('<div class="module-title">Before-and-After Stabilization Simulator</div><div class="metric-grid">' + metric_card("Current Readiness", avg_ready, "Active filtered view") + metric_card("Projected Readiness", new_score, "After stabilization") + metric_card("Exposure Stabilized", money(max(0, avoided)), "Synthetic estimate") + metric_card("Leadership Focus", common_missing(filtered_rows), "Most common gap") + '</div>')

elif module == "2027 API Checklist":
    render_html('<div class="module-title">2027 API Readiness Checklist</div>')
    items = ["Synthetic data governance", "No PHI public deployment", "Human review workflow", "Audit log structure", "Payer route field", "Authorization status field", "Documentation gap field", "SLA timestamp field", "Owner assignment field", "Exportable leadership brief"]
    checked = [item for item in items if st.checkbox(item, value=True)]
    render_html(metric_card("API Readiness", f"{len(checked)} / {len(items)}", "Portfolio maturity checklist"))

render_html(f'<div class="footer-lockup"><div class="eyebrow">Created by Kori Pickle</div><div class="footer-signature">Kori Pickle</div><div class="footer-text">Healthcare Operations Intelligence • Revenue Cycle • Patient Access • Prior Authorization • Denial Prevention</div><div class="footer-links"><a class="footer-link" href="{LINKEDIN_URL}" target="_blank">LinkedIn</a><a class="footer-link" href="{GITHUB_URL}" target="_blank">GitHub</a></div></div></div>')
