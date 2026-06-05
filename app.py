import csv, html
from datetime import date
from io import StringIO
import streamlit as st

st.set_page_config(page_title="Enterprise Revenue Operations Platform", layout="wide", initial_sidebar_state="expanded")

LINKEDIN_URL="https://www.linkedin.com/in/kori-p-865jct"
GITHUB_URL="https://github.com/koripickle1101-TN"

DATA=[
{"id":"REV-0001","payer":"Commercial","domain":"Patient Access","line":"Orthopedics","risk":"High","owner":"Patient Access Lead","days":7,"sla":5,"exposure":18450,"status":"Needs Documentation","required":"Order;Insurance Card;Clinical Note;Medical Necessity Note","present":"Order;Insurance Card","loss":"Documentation Control","rule":"Medical necessity narrative required before authorization submission.","action":"Validate documentation packet and assign same day authorization follow up."},
{"id":"REV-0002","payer":"Medicare Advantage","domain":"Authorization Control","line":"Neurology","risk":"High","owner":"Prior Authorization Lead","days":9,"sla":5,"exposure":32700,"status":"Escalate","required":"Order;Neuro Exam;Failed Conservative Therapy;Imaging Rationale","present":"Order;Neuro Exam","loss":"Authorization Readiness Control","rule":"Conservative therapy evidence and imaging rationale required.","action":"Escalate payer follow up and request missing medical necessity support."},
{"id":"REV-0003","payer":"Medicaid","domain":"Documentation Readiness","line":"Rehabilitation","risk":"Moderate","owner":"Documentation Specialist","days":4,"sla":5,"exposure":12600,"status":"Needs Eligibility Review","required":"Plan of Care;Therapy Evaluation;Frequency Order","present":"Plan of Care;Therapy Evaluation","loss":"Documentation Control","rule":"Therapy frequency order must match requested treatment period.","action":"Confirm therapy frequency order before submission."},
{"id":"REV-0004","payer":"Commercial","domain":"Routing Intelligence","line":"Cardiology","risk":"High","owner":"RCM Analyst","days":8,"sla":4,"exposure":28600,"status":"Routing Review","required":"Referral;Cardiology Note;Payer Route;Procedure Code","present":"Referral;Cardiology Note;Procedure Code","loss":"Ownership Control","rule":"Correct payer route must be established before submission.","action":"Correct payer route and document escalation owner."},
{"id":"REV-0005","payer":"Marketplace","domain":"Eligibility Verification","line":"Imaging","risk":"Moderate","owner":"Eligibility Specialist","days":5,"sla":5,"exposure":11250,"status":"Needs Eligibility Review","required":"Eligibility Response;Benefit Check;Order","present":"Order","loss":"Patient Access Control","rule":"Eligibility response and benefit confirmation required before scheduling clearance.","action":"Complete eligibility response and benefit confirmation."},
{"id":"REV-0006","payer":"Self Pay","domain":"Financial Clearance","line":"Surgery","risk":"Low","owner":"Financial Counselor","days":2,"sla":5,"exposure":7200,"status":"Financial Review","required":"Estimate;Payment Plan Review","present":"Estimate","loss":"Patient Access Control","rule":"Financial pathway review required before scheduled procedure date.","action":"Complete patient financial pathway review."},
{"id":"REV-0007","payer":"Commercial","domain":"Denial Prevention","line":"Oncology","risk":"High","owner":"Denial Prevention Lead","days":10,"sla":5,"exposure":44200,"status":"Pre Denial Review","required":"Treatment Plan;Medical Necessity Note;Prior Therapy History;Payer Policy Match","present":"Treatment Plan;Medical Necessity Note","loss":"Time Control","rule":"Policy matched documentation required for high cost treatment authorization.","action":"Run pre denial review and attach policy matched documentation."},
{"id":"REV-0008","payer":"Medicare Advantage","domain":"Authorization Control","line":"Imaging","risk":"High","owner":"Prior Authorization Lead","days":6,"sla":5,"exposure":19600,"status":"Needs Documentation","required":"Order;Clinical Note;Failed Therapy Evidence;Imaging Rationale","present":"Order;Clinical Note","loss":"Authorization Readiness Control","rule":"Failed therapy evidence must be documented for advanced imaging authorization.","action":"Request therapy evidence and attach imaging rationale."},
{"id":"REV-0009","payer":"Medicaid","domain":"Documentation Readiness","line":"Behavioral Health","risk":"Moderate","owner":"Clinical Documentation Liaison","days":6,"sla":5,"exposure":9800,"status":"Needs Documentation","required":"Assessment;Treatment Plan;Provider Attestation","present":"Assessment","loss":"Documentation Control","rule":"Provider attestation and treatment plan must be present before routing.","action":"Secure treatment plan and attestation before routing."},
{"id":"REV-0010","payer":"Commercial","domain":"Eligibility Verification","line":"Primary Care","risk":"Low","owner":"Patient Access Specialist","days":1,"sla":5,"exposure":2600,"status":"Ready","required":"Eligibility Response;Benefit Check","present":"Eligibility Response;Benefit Check","loss":"None","rule":"Standard eligibility confirmation complete.","action":"Proceed with standard review."},
{"id":"REV-0011","payer":"Medicare Advantage","domain":"Patient Access","line":"Rehabilitation","risk":"High","owner":"Access Operations Manager","days":7,"sla":5,"exposure":22300,"status":"Escalate","required":"Order;Eligibility Response;Plan of Care;Authorization Pathway","present":"Order;Plan of Care","loss":"Patient Access Control","rule":"Eligibility pathway and authorization route must be confirmed before start of care.","action":"Escalate access pathway and complete eligibility validation."},
{"id":"REV-0012","payer":"Commercial","domain":"Routing Intelligence","line":"Neurology","risk":"Moderate","owner":"RCM Analyst","days":5,"sla":5,"exposure":14100,"status":"Routing Review","required":"Payer Route;Order;Clinical Note","present":"Order;Clinical Note","loss":"Ownership Control","rule":"Correct payer route required to prevent duplicate submission.","action":"Confirm payer route and prevent duplicate submission."},
{"id":"REV-0013","payer":"Marketplace","domain":"Denial Prevention","line":"Cardiology","risk":"High","owner":"Revenue Integrity Analyst","days":8,"sla":5,"exposure":24250,"status":"Pre Denial Review","required":"Cardiology Note;Medical Necessity Note;Payer Policy Match;Procedure Code","present":"Cardiology Note;Procedure Code","loss":"Documentation Control","rule":"Payer policy match and medical necessity support required before submission.","action":"Attach payer policy match and medical necessity support."},
{"id":"REV-0014","payer":"Commercial","domain":"Authorization Control","line":"Surgery","risk":"Moderate","owner":"Prior Authorization Coordinator","days":3,"sla":5,"exposure":17300,"status":"Ready for Submission","required":"Order;Surgical Note;Procedure Code;Site of Service","present":"Order;Surgical Note;Procedure Code;Site of Service","loss":"None","rule":"Required surgical authorization packet complete.","action":"Submit and monitor payer response window."}
]

def esc(x): return html.escape(str(x))
def money(x): return "${:,.0f}".format(float(x))
def parts(x): return [p.strip() for p in str(x).split(";") if p.strip()]
def missing(r): return [d for d in parts(r["required"]) if d not in set(parts(r["present"]))]
def ready(r):
    return max(0,min(100,100-len(missing(r))*13-max(0,r["days"]-r["sla"])*8-{"Low":0,"Moderate":7,"High":17}.get(r["risk"],0)))
def loss_score(r):
    s={"Low":10,"Moderate":30,"High":50}.get(r["risk"],20)+len(missing(r))*9+max(0,r["days"]-r["sla"])*8
    if r["loss"]=="Ownership Control": s+=10
    if r["status"] in ["Escalate","Pre Denial Review"]: s+=8
    return max(0,min(100,s))
def loss_label(s):
    return "Escalation Required" if s>=76 else "Control Loss" if s>=51 else "Watch" if s>=26 else "Stable"

def load_csv(f):
    if not f: return DATA
    keymap={"Case ID":"id","Payer Group":"payer","Workflow Domain":"domain","Service Line":"line","Risk":"risk","Owner":"owner","Days Open":"days","SLA Limit":"sla","Exposure":"exposure","Status":"status","Required Docs":"required","Present Docs":"present","First Control Loss":"loss","Payer Rule":"rule","Next Action":"action"}
    out=[]
    try:
        rows=csv.DictReader(StringIO(f.getvalue().decode("utf-8")))
        for row in rows:
            item={}
            for old,new in keymap.items():
                item[new]=row.get(old,row.get(new,""))
            for n in ["days","sla","exposure"]:
                try: item[n]=int(float(item[n]))
                except Exception: item[n]=0
            out.append(item)
    except Exception:
        return DATA
    return out or DATA

def metric(label,value,note):
    return f'<div class="metric"><div class="kicker">{esc(label)}</div><div class="number">{esc(value)}</div><p>{esc(note)}</p></div>'

def brief(rows):
    total=len(rows); high=sum(1 for r in rows if r["risk"]=="High"); sla=sum(1 for r in rows if r["days"]>=r["sla"])
    exposure=sum(r["exposure"] for r in rows); owners=len(set(r["owner"] for r in rows))
    avg=round(sum(ready(r) for r in rows)/total,1) if total else 0
    return f"""Enterprise Revenue Operations Platform
Created by Kori Pickle
Generated {date.today().isoformat()}

Synthetic Data Standard
Synthetic records only. No PHI. Human review required.

Active Command View
Total records: {total}
High risk records: {high}
SLA pressure signals: {sla}
Distinct owners: {owners}
Average readiness: {avg}
Simulated exposure: {money(exposure)}

Workflow Loss Control Method
Core question: where did the workflow first lose control?

Recommended next steps
1. Stabilize missing documentation.
2. Escalate records at or beyond SLA.
3. Confirm payer rule requirements.
4. Document human review activity.
5. Use scoring as a prioritization signal only.
"""

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;500&display=swap');
:root{--o:#FF8200;--b:#000000;--w:#FFFFFF}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],header,footer{display:none!important;visibility:hidden!important;height:0!important}
html,body,[data-testid="stAppViewContainer"]{background:var(--w)!important;color:var(--b)!important}.block-container{max-width:1380px!important;padding:0 3rem 5rem!important}p,div,span,label,input,textarea,button,select{font-family:Inter,Arial,sans-serif!important;color:var(--b)!important}h1,h2,h3{font-family:"Playfair Display",Georgia,serif!important;font-weight:400!important}[data-testid="stSidebar"]{background:var(--w)!important;border-right:4px solid var(--o)!important}div[data-baseweb="select"]>div,[data-testid="stFileUploader"] section{border:1px solid var(--b)!important;background:var(--w)!important;border-radius:0!important}div[data-baseweb="tag"]{background:var(--o)!important;border:1px solid var(--b)!important;border-radius:0!important}.stButton button,.stDownloadButton button{border:1px solid var(--b)!important;background:var(--w)!important;border-radius:0!important;letter-spacing:.16em!important;text-transform:uppercase!important}
.shell{border-left:2px solid var(--b);border-right:2px solid var(--b);padding:3rem 4rem;background:var(--w)}.sig{font-family:"Great Vibes",cursive!important;font-size:clamp(4.5rem,11vw,9rem)!important;line-height:.76;margin:0 0 1rem}.sub{letter-spacing:.42em;text-transform:uppercase;font-size:.9rem;line-height:2.5}.rule{height:12px;background:var(--o);margin:2rem 0 3.5rem}.kicker{letter-spacing:.34em;text-transform:uppercase;font-size:.76rem;font-weight:600;line-height:2}.hero{font-family:"Playfair Display",Georgia,serif!important;font-size:clamp(4.8rem,13vw,10.5rem);line-height:.84;letter-spacing:-.055em;margin:4rem 0 2rem}.orange{color:var(--o)!important}.copy{font-size:clamp(1.1rem,2.2vw,1.55rem);line-height:1.9;font-weight:300;max-width:980px}.badges{display:flex;flex-wrap:wrap;gap:1rem;margin:3rem 0}.badge{border:1px solid var(--b);border-left:12px solid var(--o);padding:1rem 1.3rem;letter-spacing:.2em;text-transform:uppercase;font-weight:600;font-size:.78rem}.panel,.identity,.metric,.card,.loss{border:1px solid var(--b);background:var(--w)}.identity,.panel{border-top:10px solid var(--o);padding:3rem;margin:3rem 0}.identity-title,.section{font-family:"Playfair Display",Georgia,serif!important;font-weight:400;letter-spacing:-.05em;line-height:.9}.identity-title{font-size:clamp(2.8rem,7vw,6rem);margin:2rem 0}.section{font-size:clamp(3rem,8vw,6.6rem);margin:3rem 0 1.5rem}.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:1.3rem;margin:3rem 0}.metric{border-left:12px solid var(--o);padding:2rem;min-height:215px}.number{font-family:"Playfair Display",Georgia,serif!important;font-weight:400;color:var(--o)!important;font-size:clamp(3rem,6vw,5.7rem);line-height:1;margin:1.8rem 0 1rem;letter-spacing:-.04em}.cards,.lossgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:1.2rem;margin:2rem 0}.card{border-left:10px solid var(--o);padding:1.5rem}.loss{border-top:8px solid var(--o);padding:1.7rem}.caseid{font-family:"Playfair Display",Georgia,serif!important;font-size:2.2rem;letter-spacing:-.04em}.meta{letter-spacing:.16em;text-transform:uppercase;font-size:.82rem;line-height:1.8;margin:1rem 0}.tablewrap{overflow-x:auto;border:1px solid var(--b);margin:2rem 0}table{border-collapse:collapse;min-width:1100px;width:100%}th{background:var(--o);letter-spacing:.16em;text-transform:uppercase;font-size:.72rem}th,td{border:1px solid var(--b);padding:1rem;text-align:left;vertical-align:top}.bar{display:grid;grid-template-columns:130px 1fr 52px;gap:1rem;align-items:center;margin:1.2rem 0}.track{height:22px;border:1px solid var(--b)}.fill{height:100%;background:var(--o)}.brief{white-space:pre-wrap;border:1px solid var(--b);border-left:12px solid var(--o);padding:2rem;line-height:1.7}.footer{text-align:center;margin-top:5rem;padding:4rem 0;border-top:10px solid var(--o);border-bottom:10px solid var(--o)}.footsig{font-family:"Great Vibes",cursive!important;font-size:clamp(4rem,10vw,8rem);line-height:.8}.footer a{display:inline-block;border:1px solid var(--b);border-left:10px solid var(--o);padding:1rem 1.5rem;margin:1rem .5rem;text-decoration:none;letter-spacing:.2em;text-transform:uppercase}@media(max-width:900px){.block-container{padding:0 1rem 4rem!important}.shell{padding:2rem 1.4rem;border-left:1px solid var(--b);border-right:1px solid var(--b)}.sig{font-size:5rem!important}.sub{letter-spacing:.32em;font-size:.72rem}.hero{font-size:4.7rem}.metrics,.cards,.lossgrid{grid-template-columns:1fr}.metric{min-height:165px}.copy{font-size:1.05rem}.section{font-size:4rem}th,td{font-size:.88rem;padding:.85rem}}
</style>
""",unsafe_allow_html=True)

uploaded=st.sidebar.file_uploader("Synthetic CSV upload only",type=["csv"])
all_cases=load_csv(uploaded)
risk=st.sidebar.multiselect("Filter by risk level",sorted(set(x["risk"] for x in all_cases)),default=sorted(set(x["risk"] for x in all_cases)))
payer=st.sidebar.multiselect("Filter by payer group",sorted(set(x["payer"] for x in all_cases)),default=sorted(set(x["payer"] for x in all_cases)))
domain=st.sidebar.multiselect("Filter by workflow area",sorted(set(x["domain"] for x in all_cases)),default=sorted(set(x["domain"] for x in all_cases)))
line=st.sidebar.multiselect("Filter by service line",sorted(set(x["line"] for x in all_cases)),default=sorted(set(x["line"] for x in all_cases)))
rows=[r for r in all_cases if r["risk"] in risk and r["payer"] in payer and r["domain"] in domain and r["line"] in line]

total=len(rows); high=sum(1 for r in rows if r["risk"]=="High"); sla=sum(1 for r in rows if r["days"]>=r["sla"]); exposure=sum(r["exposure"] for r in rows); avg=round(sum(ready(r) for r in rows)/total,1) if total else 0; owners=len(set(r["owner"] for r in rows)) if rows else 0

st.markdown(f"""
<div class="shell"><div class="sig">Kori Pickle</div><div class="sub">Healthcare Operations</div><div class="sub orange">Intelligence</div><div class="rule"></div><div class="kicker">Kori Pickle • Healthcare Operations Intelligence</div><div class="hero">Enterprise<br>Revenue<br><span class="orange">Operations</span><br>Platform</div><div class="copy">A premium synthetic no PHI healthcare operations command center for patient access, eligibility verification, prior authorization pressure tracking, routing intelligence, documentation readiness, denial prevention, payer friction analysis, and responsible operational intelligence.<br><br>This build functions as an operational review workbench: filter synthetic cases, isolate ownership gaps, simulate stabilization impact, generate escalation language, and build a leadership brief from the active command view.</div><div class="badges"><div class="badge">No PHI</div><div class="badge">Synthetic Data</div><div class="badge">Human Review Required</div><div class="badge">Built by Kori Pickle</div></div><div class="identity"><div class="kicker">Operational Identity</div><div class="identity-title">Workflow visibility before revenue damage.</div><div class="rule" style="width:55%;height:6px;margin:2rem 0"></div><div class="copy">Designed around one question: where did the workflow first lose control?</div><div class="kicker" style="margin-top:2rem">Patient Access • Authorization Control • Documentation Readiness • Denial Prevention</div></div><div class="metrics">{metric("High Risk Records",high,"Prioritized operational review queue.")}{metric("SLA Pressure",sla,"Records aged at or above SLA limit.")}{metric("Synthetic Exposure",money(exposure),"Portfolio simulation only.")}{metric("Readiness Average",avg,"Aggregate workflow readiness score.")}</div>
""",unsafe_allow_html=True)

module=st.radio("Operational modules",["Command Center","Workflow Loss Control Method","Authorization Readiness Engine","Missing Documentation Detector","SLA Countdown","Human Review Log","Executive Brief Builder","About Kori","Stabilization Simulator","2027 API Checklist"],horizontal=True,label_visibility="collapsed")

if module=="Command Center":
    st.markdown('<div class="section">Live Command Center</div><div class="copy">Use the sidebar filters to isolate operational pressure across payer group, workflow domain, service line, and risk level.</div>',unsafe_allow_html=True)
    cards=""
    for r in rows:
        miss=", ".join(missing(r)) or "None detected"
        cards+=f'<div class="card"><div class="caseid">{esc(r["id"])}</div><div class="meta">{esc(r["risk"])} • {esc(r["payer"])} • {esc(r["domain"])}</div><p><b>Owner:</b> {esc(r["owner"])}<br><b>Missing:</b> {esc(miss)}<br><b>Next:</b> {esc(r["action"])}</p></div>'
    st.markdown(f'<div class="cards">{cards}</div>',unsafe_allow_html=True)
    cols=["id","payer","domain","line","risk","owner","days","status"]; labels=["Case ID","Payer Group","Workflow Domain","Service Line","Risk","Owner","Days Open","Status"]
    head="".join(f"<th>{x}</th>" for x in labels); body="".join("<tr>"+"".join(f"<td>{esc(r[c])}</td>" for c in cols)+"</tr>" for r in rows)
    st.markdown(f'<div class="tablewrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>',unsafe_allow_html=True)
    counts={k:sum(1 for r in rows if r["risk"]==k) for k in ["High","Moderate","Low"]}; mx=max(counts.values()) if counts else 1
    bars="".join(f'<div class="bar"><div>{k}</div><div class="track"><div class="fill" style="width:{0 if mx==0 else v/mx*100}%"></div></div><div class="number" style="font-size:2rem">{v}</div></div>' for k,v in counts.items())
    st.markdown(f'<div class="panel"><div class="kicker">Risk Queue Distribution</div>{bars}</div><div class="panel"><div class="section" style="margin-top:0">Executive Interpretation</div><div class="copy">The active view shows {total} synthetic records, {high} high risk records, {sla} SLA pressure signals, {owners} distinct owners, average readiness of {avg}, and {money(exposure)} in simulated exposure. These are prioritization signals for human review.</div></div>',unsafe_allow_html=True)
elif module=="Workflow Loss Control Method":
    st.markdown('<div class="section">Workflow Loss Control Method™</div><div class="copy">A Kori Pickle operating method for identifying where the workflow first lost control before revenue damage appears downstream.</div>',unsafe_allow_html=True)
    domains=[("Patient Access Control","Eligibility, benefits, scheduling pathway, and financial clearance stability."),("Authorization Readiness Control","Required evidence, payer rule alignment, and submission readiness."),("Documentation Control","Packet completeness, medical necessity support, and attestation status."),("Ownership Control","Human owner, route clarity, escalation pathway, and handoff accountability."),("Time Control","Aging, SLA pressure, stalled work, and delay prevention.")]
    st.markdown('<div class="lossgrid">'+"".join(f'<div class="loss"><div class="kicker">{a}</div><p>{b}</p></div>' for a,b in domains)+'</div>',unsafe_allow_html=True)
    st.markdown('<div class="lossgrid">'+"".join(f'<div class="loss"><div class="kicker">{esc(r["id"])} • {loss_label(loss_score(r))}</div><div class="number">{loss_score(r)}</div><p><b>First failed domain:</b> {esc(r["loss"])}</p><p><b>Why:</b> {esc(r["rule"])}</p><p><b>Owner:</b> {esc(r["owner"])}</p><p><b>Next:</b> {esc(r["action"])}</p></div>' for r in rows)+'</div>',unsafe_allow_html=True)
elif module=="Authorization Readiness Engine":
    st.markdown('<div class="section">Authorization Readiness Engine</div><div class="copy">Readiness scoring for human review before payer submission.</div>',unsafe_allow_html=True)
    st.markdown('<div class="lossgrid">'+"".join(f'<div class="loss"><div class="kicker">{esc(r["id"])} • {esc(r["domain"])}</div><div class="number">{ready(r)}</div><p><b>Status:</b> {"Ready for review" if ready(r)>=80 else "Needs stabilization"}</p><p><b>Payer logic:</b> {esc(r["rule"])}</p><p><b>Missing documentation count:</b> {len(missing(r))}</p></div>' for r in rows)+'</div>',unsafe_allow_html=True)
elif module=="Missing Documentation Detector":
    st.markdown('<div class="section">Missing Documentation Detector</div><div class="copy">Compares required documentation to present documentation and creates a human review queue.</div>',unsafe_allow_html=True)
    st.markdown('<div class="cards">'+"".join(f'<div class="card"><div class="caseid">{esc(r["id"])}</div><div class="meta">{esc(r["owner"])}</div><p><b>Missing:</b> {esc(", ".join(missing(r)) or "None detected")}</p><p>{esc(r["action"])}</p></div>' for r in rows)+'</div>',unsafe_allow_html=True)
elif module=="SLA Countdown":
    st.markdown('<div class="section">SLA Breach Countdown</div><div class="copy">Identifies whether synthetic cases are before SLA, at SLA, or beyond SLA.</div>',unsafe_allow_html=True)
    st.markdown('<div class="lossgrid">'+"".join(f'<div class="loss"><div class="kicker">{esc(r["id"])}</div><div class="number">{r["sla"]-r["days"]}</div><p><b>Owner:</b> {esc(r["owner"])}</p><p>{esc(r["action"])}</p></div>' for r in rows)+'</div>',unsafe_allow_html=True)
elif module=="Human Review Log":
    st.markdown('<div class="section">Human Review Log</div><div class="copy">Session based review notes for synthetic cases only.</div>',unsafe_allow_html=True)
    if "audit" not in st.session_state: st.session_state.audit=[]
    cid=st.selectbox("Synthetic case",[r["id"] for r in rows] or ["No active case"]); note=st.text_area("Human review note","Reviewed missing documentation and confirmed next owner.")
    if st.button("Add review note"): st.session_state.audit.append((date.today().isoformat(),cid,note))
    st.markdown('<div class="panel">'+"".join(f'<div style="border-bottom:1px solid #000;padding:1rem 0"><b>{esc(d)} • {esc(c)}</b><br>{esc(n)}</div>' for d,c,n in reversed(st.session_state.audit))+"</div>",unsafe_allow_html=True)
elif module=="Executive Brief Builder":
    st.markdown('<div class="section">Executive Brief Builder</div><div class="copy">Generate a leadership brief from the active filtered command view.</div>',unsafe_allow_html=True)
    b=brief(rows); st.markdown(f'<div class="brief">{esc(b)}</div>',unsafe_allow_html=True); st.download_button("Download executive brief",b,file_name="kori_pickle_enterprise_revenue_operations_brief.txt",mime="text/plain")
elif module=="About Kori":
    st.markdown('<div class="section">About Kori</div><div class="panel"><div class="copy"><b>Kori Pickle</b> is a University of Phoenix BSHA candidate focused on healthcare operations, revenue cycle management, patient access, prior authorization workflows, denial prevention, health informatics, and workflow intelligence.<br><br>Her patient-to-professional perspective shapes this platform: operational breakdowns affect access, trust, communication, care coordination, and patient experience.</div></div><div class="lossgrid"><div class="loss"><div class="kicker">Academic Standing</div><p>99 of 120 credits completed<br>GPA 3.6<br>Healthcare Administration</p></div><div class="loss"><div class="kicker">Core Focus</div><p>Revenue Cycle Management<br>Patient Access<br>Prior Authorization<br>Denial Prevention<br>Health Informatics</p></div><div class="loss"><div class="kicker">Portfolio Direction</div><p>Remote healthcare operations tools using synthetic data, responsible human review, workflow visibility, and operational stabilization logic.</p></div><div class="loss"><div class="kicker">Professional Value</div><p>Translate workflow friction into ownership, missing documentation, SLA pressure, readiness signals, and leadership ready action steps.</p></div></div>',unsafe_allow_html=True)
elif module=="Stabilization Simulator":
    st.markdown('<div class="section">Before and After Stabilization Simulator</div><div class="copy">Simulate operational improvement without using PHI.</div>',unsafe_allow_html=True)
    cap=st.slider("Documentation capture improvement",0,60,25); age=st.slider("SLA acceleration improvement",0,60,20); route=st.slider("Routing accuracy improvement",0,60,15)
    rate=min(.75,cap*.006+age*.005+route*.004); after=exposure*(1-rate)
    st.markdown(f'<div class="metrics">{metric("Before Exposure",money(exposure),"Current synthetic exposure.")}{metric("After Stabilization",money(after),"Projected synthetic exposure after controls.")}{metric("Avoidable Exposure",money(exposure-after),"Estimated stabilization opportunity.")}{metric("Reduction Rate",str(round(rate*100,1))+"%","Simulation only.")}</div>',unsafe_allow_html=True)
else:
    st.markdown('<div class="section">2027 API Readiness Checklist</div>',unsafe_allow_html=True)
    checks=["Synthetic data architecture is separated from real PHI.","Human review remains required for payer and patient-impacting decisions.","Workflow events are structured by owner, status, SLA, payer group, documentation readiness, and next action.","Audit log captures review notes without patient identifiers.","CSV ingestion validates required fields before analysis.","Future API integration needs authentication, role based access, encrypted storage, and compliance review."]
    st.markdown('<div class="panel">'+"".join(f'<div style="border-bottom:1px solid #000;padding:1rem 0">{esc(c)}</div>' for c in checks)+"</div>",unsafe_allow_html=True)

st.markdown(f'<div class="footer"><div class="kicker">Created by Kori Pickle</div><div class="footsig">Kori Pickle</div><div class="copy" style="margin:0 auto">Healthcare Operations Intelligence • Revenue Cycle • Patient Access • Prior Authorization • Denial Prevention</div><a href="{LINKEDIN_URL}" target="_blank">LinkedIn</a><a href="{GITHUB_URL}" target="_blank">GitHub</a></div></div>',unsafe_allow_html=True)
