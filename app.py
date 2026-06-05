import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Enterprise Revenue Operations Platform",
    page_icon="🟠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=Inter:wght@400;500;600;700;800;900&family=Great+Vibes&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background: rgb(255,255,255) !important;
    color: rgb(0,0,0) !important;
    font-family: Inter, sans-serif !important;
}

.block-container {
    padding-top: 2rem !important;
    padding-left: 5rem !important;
    padding-right: 5rem !important;
    max-width: 1550px !important;
}

h1, h2, h3 {
    font-family: "Playfair Display", Georgia, serif !important;
    color: rgb(0,0,0) !important;
    letter-spacing: -0.05em !important;
}

p, div, label, span {
    font-family: Inter, sans-serif;
}

[data-testid="stSidebar"] {
    background: rgb(255,255,255) !important;
    border-right: 4px solid rgb(255,130,0) !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
textarea {
    background: rgb(255,255,255) !important;
    color: rgb(0,0,0) !important;
    border: 2px solid rgb(0,0,0) !important;
    border-radius: 18px !important;
}

span[data-baseweb="tag"], [data-baseweb="tag"] {
    background: rgb(255,130,0) !important;
    color: rgb(0,0,0) !important;
    border: 2px solid rgb(0,0,0) !important;
    border-radius: 999px !important;
    font-weight: 900 !important;
}

.stTabs [data-baseweb="tab"] {
    background: rgb(255,255,255) !important;
    color: rgb(0,0,0) !important;
    border: 2px solid rgb(0,0,0) !important;
    border-radius: 999px !important;
    padding: 0.75rem 1rem !important;
    font-weight: 900 !important;
}

.stTabs [aria-selected="true"] {
    background: rgb(255,130,0) !important;
    color: rgb(0,0,0) !important;
}

.hero-grid {
    display: grid;
    grid-template-columns: 1.25fr 0.75fr;
    gap: 2rem;
    align-items: stretch;
    margin-bottom: 2rem;
}

.hero-card {
    background: rgb(255,255,255);
    color: rgb(0,0,0);
    border: 3px solid rgb(0,0,0);
    border-radius: 38px;
    padding: 3.6rem;
    min-height: 520px;
    position: relative;
    overflow: hidden;
}

.hero-card:before {
    content: "";
    position: absolute;
    right: 48px;
    top: 48px;
    width: 108px;
    height: 108px;
    border: 4px solid rgb(255,130,0);
    border-radius: 50%;
    box-shadow: 0 0 0 16px rgb(255,255,255), 0 0 0 20px rgb(255,130,0);
}

.hero-card:after {
    content: "";
    position: absolute;
    right: -105px;
    bottom: -105px;
    width: 310px;
    height: 310px;
    border: 4px dotted rgb(255,130,0);
    border-radius: 50%;
}

.black-card {
    background: rgb(0,0,0);
    color: rgb(255,255,255);
    border: 4px solid rgb(255,130,0);
    border-radius: 38px;
    padding: 2.5rem;
    min-height: 520px;
    position: relative;
}

.black-card:before {
    content: "";
    position: absolute;
    top: 2rem;
    right: 2rem;
    width: 150px;
    height: 150px;
    border: 4px solid rgb(255,130,0);
    border-radius: 50%;
    box-shadow: inset 0 0 0 18px rgb(0,0,0), 0 0 0 22px rgb(255,130,0);
}

.kicker {
    font-size: 0.72rem;
    letter-spacing: 0.34em;
    text-transform: uppercase;
    font-weight: 900;
    color: rgb(0,0,0);
    margin-bottom: 1rem;
}

.black-card .kicker {
    color: rgb(255,255,255);
}

.hero-title {
    font-family: "Playfair Display", Georgia, serif;
    font-size: clamp(3.2rem, 7vw, 6.7rem);
    line-height: 0.88;
    letter-spacing: -0.08em;
    font-weight: 900;
    margin: 0;
    color: rgb(0,0,0);
}

.orange {
    color: rgb(255,130,0);
}

.orange-line {
    width: 220px;
    height: 4px;
    background: rgb(255,130,0);
    margin-top: 1.6rem;
    margin-bottom: 1.7rem;
}

.hero-copy {
    font-size: 1.05rem;
    line-height: 1.75;
    color: rgb(0,0,0);
    max-width: 900px;
    font-weight: 600;
}

.badge {
    display: inline-block;
    background: rgb(255,255,255);
    color: rgb(0,0,0);
    border: 2px solid rgb(255,130,0);
    border-radius: 999px;
    padding: 0.6rem 0.9rem;
    margin-top: 0.8rem;
    margin-right: 0.5rem;
    font-size: 0.74rem;
    font-weight: 900;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.metric-card {
    background: rgb(255,255,255);
    color: rgb(0,0,0);
    border: 3px solid rgb(0,0,0);
    border-left: 12px solid rgb(255,130,0);
    border-radius: 26px;
    padding: 1.45rem;
    min-height: 160px;
}

.metric-label {
    font-size: 0.70rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    font-weight: 900;
    color: rgb(0,0,0);
    margin-bottom: 0.75rem;
}

.metric-value {
    font-family: "Playfair Display", Georgia, serif;
    font-size: 3.15rem;
    font-weight: 900;
    line-height: 0.95;
    color: rgb(255,130,0);
}

.metric-note {
    font-size: 0.82rem;
    color: rgb(0,0,0);
    line-height: 1.45;
    margin-top: 0.9rem;
    font-weight: 700;
}

.panel {
    background: rgb(255,255,255);
    color: rgb(0,0,0);
    border: 3px solid rgb(0,0,0);
    border-radius: 30px;
    padding: 2.15rem;
    margin: 1.4rem 0;
}

.dark-panel {
    background: rgb(0,0,0);
    color: rgb(255,255,255);
    border: 4px solid rgb(255,130,0);
    border-left: 14px solid rgb(255,130,0);
    border-radius: 32px;
    padding: 2.35rem;
    margin: 1.4rem 0;
}

.dark-panel h3 {
    color: rgb(255,255,255) !important;
    font-size: 2.35rem;
    margin: 0 0 1rem 0;
}

.dark-panel p {
    color: rgb(255,255,255);
    line-height: 1.7;
    font-weight: 600;
}

.node-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(140px, 1fr));
    gap: 1rem;
    margin-top: 1.4rem;
}

.node {
    border: 3px solid rgb(255,130,0);
    border-radius: 999px;
    min-height: 88px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: rgb(255,255,255);
    color: rgb(0,0,0);
    box-shadow: inset 0 0 0 10px rgb(255,255,255), inset 0 0 0 13px rgb(255,130,0);
    font-size: 0.73rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    padding: 0.9rem;
}

.signature {
    font-family: "Great Vibes", cursive;
    font-size: 4rem;
    color: rgb(0,0,0);
    line-height: 1;
    transform: rotate(-1deg);
    margin-top: 0.3rem;
    margin-bottom: 0.8rem;
}

.icon-pill {
    display: inline-block;
    background: rgb(255,255,255);
    color: rgb(0,0,0) !important;
    border: 2px solid rgb(0,0,0);
    border-radius: 999px;
    padding: 0.58rem 0.85rem;
    margin: 0.25rem;
    text-decoration: none !important;
    font-size: 0.75rem;
    font-weight: 900;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.icon-pill:hover {
    background: rgb(255,130,0);
}

[data-testid="stDataFrame"] {
    border: 3px solid rgb(0,0,0);
    border-radius: 18px;
    overflow: hidden;
}

[data-testid="stMainMenu"], footer {
    visibility: hidden;
}

@media (max-width: 950px) {
    .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
    .hero-grid { grid-template-columns: 1fr; }
    .hero-card { padding: 2rem; min-height: auto; }
    .black-card { min-height: 380px; }
    .node-grid { grid-template-columns: 1fr; }
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def build_records():
    data = [
        ["REV-0001", "Commercial", "Patient Access", "Orthopedics", "Eligibility mismatch", 9, 12600, "High", "Missing subscriber relation", "Escalate eligibility verification"],
        ["REV-0002", "Medicare Advantage", "Authorization Control", "Cardiology", "Aging authorization", 6, 28750, "High", "Pending packet", "Request packet review"],
        ["REV-0003", "Medicaid", "Documentation Readiness", "Rehabilitation", "Incomplete plan of care", 4, 9300, "Moderate", "Therapy notes incomplete", "Validate documentation readiness"],
        ["REV-0004", "Commercial", "Routing Intelligence", "Imaging", "Wrong portal route", 8, 14500, "High", "Benefit manager carve out", "Confirm routing owner"],
        ["REV-0005", "Marketplace", "Eligibility Verification", "Primary Care", "Coverage inactive", 3, 4200, "Moderate", "Coverage termination risk", "Recheck eligibility"],
        ["REV-0006", "Self Pay", "Financial Clearance", "Surgery", "Estimate not completed", 2, 6800, "Low", "Estimate missing", "Create estimate review"],
        ["REV-0007", "Commercial", "Denial Prevention", "Oncology", "Policy criteria exposure", 7, 33100, "High", "Criteria unclear", "Route to human review"],
        ["REV-0008", "Medicare Advantage", "Authorization Control", "Neurology", "SLA risk", 5, 18500, "Moderate", "Pending five days", "Escalate payer follow up"],
        ["REV-0009", "Medicaid", "Documentation Readiness", "Behavioral Health", "Missing referral", 6, 7600, "Moderate", "Referral not attached", "Attach referral evidence"],
        ["REV-0010", "Commercial", "Eligibility Verification", "Cardiology", "COB conflict", 8, 22100, "High", "Benefits unresolved", "Validate primary payer"],
        ["REV-0011", "Marketplace", "Routing Intelligence", "Imaging", "Payer policy mismatch", 7, 11900, "High", "Delegated review required", "Check benefit manager"],
        ["REV-0012", "Medicare Advantage", "Denial Prevention", "Rehabilitation", "Appeal exposure", 5, 15200, "Moderate", "Denial reason pattern detected", "Prepare prevention brief"],
    ]
    columns = ["case_id", "payer_group", "workflow_domain", "service_line", "signal", "aging_days", "synthetic_exposure", "risk_level", "root_cause", "recommended_action"]
    return pd.DataFrame(data, columns=columns)

records = build_records()

st.markdown("""
<div class="hero-grid">
    <div class="hero-card">
        <div class="kicker">Kori Pickle • Healthcare Operations Intelligence</div>
        <h1 class="hero-title">Enterprise Revenue <span class="orange">Operations</span> Platform</h1>
        <div class="orange-line"></div>
        <p class="hero-copy">A premium synthetic operations control system for patient access, eligibility verification, authorization pressure, routing intelligence, documentation readiness, denial prevention, payer friction, and leadership reporting.</p>
        <p class="hero-copy">Built as a public portfolio artifact using synthetic records only. The platform demonstrates operational review signals and human review workflows.</p>
        <span class="badge">White</span>
        <span class="badge">Black</span>
        <span class="badge">Tennessee Orange</span>
        <span class="badge">Synthetic Data</span>
    </div>
    <div class="black-card">
        <div class="kicker">Operational Identity</div>
        <h3 style="color:rgb(255,255,255); font-size:2.9rem; line-height:0.95; margin-top:8rem;">Workflow visibility before revenue damage.</h3>
        <p style="color:rgb(255,255,255); line-height:1.7; font-weight:700;">Designed around one question: where did the workflow first lose control?</p>
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("Command Filters", expanded=True):
    f1, f2, f3 = st.columns(3)
    with f1:
        risk_filter = st.multiselect("Filter by risk level", sorted(records["risk_level"].unique()), default=sorted(records["risk_level"].unique()))
    with f2:
        payer_filter = st.multiselect("Filter by payer group", sorted(records["payer_group"].unique()), default=sorted(records["payer_group"].unique()))
    with f3:
        domain_filter = st.multiselect("Filter by workflow area", sorted(records["workflow_domain"].unique()), default=sorted(records["workflow_domain"].unique()))

filtered = records[records["risk_level"].isin(risk_filter) & records["payer_group"].isin(payer_filter) & records["workflow_domain"].isin(domain_filter)]
high_count = int((filtered["risk_level"] == "High").sum())
sla_count = int((filtered["aging_days"] >= 5).sum())
exposure = int(filtered["synthetic_exposure"].sum()) if not filtered.empty else 0
avg_age = round(float(filtered["aging_days"].mean()), 1) if not filtered.empty else 0

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">High Risk Records</div><div class="metric-value">{high_count}</div><div class="metric-note">Prioritized operational queue.</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">SLA Pressure</div><div class="metric-value">{sla_count}</div><div class="metric-note">Records aged five or more days.</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Synthetic Exposure</div><div class="metric-value">${exposure:,.0f}</div><div class="metric-note">Portfolio simulation only.</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="metric-card"><div class="metric-label">Academic Standing</div><div class="metric-value">99 / 120</div><div class="metric-note">BSHA candidate • GPA 3.6.</div></div>', unsafe_allow_html=True)

tab_a, tab_b, tab_c, tab_d, tab_e = st.tabs(["Command Center", "Control Grid", "Friction Map", "Brief Builder", "Governance"])

with tab_a:
    st.markdown("## Live Command Center")
    st.write("Use the filters above to isolate operational pressure across payer, workflow domain, and risk level.")
    st.dataframe(filtered, hide_index=True, use_container_width=True)
    left, right = st.columns([5, 4])
    with left:
        risk_summary = filtered.groupby("risk_level")["case_id"].count().reset_index(name="records")
        st.markdown("### Risk Queue Distribution")
        st.bar_chart(risk_summary.set_index("risk_level"))
    with right:
        st.markdown(f'<div class="dark-panel"><h3>Executive Interpretation</h3><p>The current filtered view shows {len(filtered)} synthetic records, {high_count} high risk records, {sla_count} SLA pressure signals, and ${exposure:,.0f} in simulated exposure. These are prioritization signals for human review.</p></div>', unsafe_allow_html=True)

with tab_b:
    st.markdown("## Revenue Operations Control Grid")
    st.markdown('<div class="panel"><div class="kicker">Workflow Chain</div><div class="node-grid"><div class="node">Patient Access Intake</div><div class="node">Eligibility Control</div><div class="node">Routing Intelligence</div><div class="node">Authorization Aging</div><div class="node">Documentation Readiness</div><div class="node">Denial Prevention</div></div></div>', unsafe_allow_html=True)
    domain_summary = filtered.groupby("workflow_domain").agg(records=("case_id", "count"), exposure=("synthetic_exposure", "sum"), average_aging=("aging_days", "mean")).reset_index()
    domain_summary["average_aging"] = domain_summary["average_aging"].round(1)
    st.dataframe(domain_summary, hide_index=True, use_container_width=True)
    st.markdown("### Stabilization Simulator")
    volume = st.number_input("Monthly front end record volume", min_value=0, value=15000, step=500)
    friction = st.slider("Estimated workflow friction rate", min_value=0.01, max_value=0.25, value=0.08, step=0.01)
    capture = st.slider("Estimated stabilization capture rate", min_value=0.25, max_value=0.95, value=0.85, step=0.05)
    flagged = volume * friction
    stabilized = flagged * capture
    k1, k2, k3 = st.columns(3)
    k1.metric("Projected Records Flagged", f"{int(flagged):,}")
    k2.metric("Projected Records Stabilized", f"{int(stabilized):,}")
    k3.metric("Residual Review Queue", f"{int(flagged - stabilized):,}")

with tab_c:
    st.markdown("## Payer Friction Map")
    payer_summary = filtered.groupby("payer_group").agg(records=("case_id", "count"), exposure=("synthetic_exposure", "sum"), average_aging=("aging_days", "mean"), high_risk=("risk_level", lambda s: int((s == "High").sum()))).reset_index()
    payer_summary["average_aging"] = payer_summary["average_aging"].round(1)
    payer_summary["friction_score"] = (payer_summary["records"] * 8 + payer_summary["high_risk"] * 25 + payer_summary["average_aging"] * 6).round(0).astype(int)
    st.dataframe(payer_summary.sort_values("friction_score", ascending=False), hide_index=True, use_container_width=True)
    st.bar_chart(payer_summary.set_index("payer_group")["friction_score"])

with tab_d:
    st.markdown("## Leadership Brief Builder")
    brief_type = st.selectbox("Brief type", ["Executive readout", "Daily huddle script", "Denial prevention action plan"])
    if brief_type == "Executive readout":
        brief = f"Enterprise Revenue Operations Brief\n\nCurrent synthetic command center view shows {len(filtered)} records, {high_count} high risk records, {sla_count} SLA pressure signals, average aging of {avg_age} days, and ${exposure:,.0f} in simulated exposure.\n\nPrimary concern:\nWorkflow pressure is forming before downstream denial activity.\n\nRecommended actions:\n1. Prioritize high risk records for human review.\n2. Validate payer routing before submission.\n3. Confirm documentation readiness before follow up.\n4. Track aged requests by payer and service line.\n\nCreated by Kori Pickle"
    elif brief_type == "Daily huddle script":
        brief = f"Daily Huddle Script\n\nToday we are reviewing {len(filtered)} synthetic workflow records.\n\nFocus areas:\nHigh risk queue: {high_count}\nSLA pressure queue: {sla_count}\nSimulated exposure: ${exposure:,.0f}\n\nCreated by Kori Pickle"
    else:
        brief = "Denial Prevention Action Plan\n\nObjective:\nUse early workflow visibility to identify operational risk before downstream denial activity develops.\n\nPriorities:\n1. Eligibility mismatch review\n2. Authorization aging review\n3. Documentation readiness review\n4. Payer routing validation\n5. Follow up escalation\n\nCreated by Kori Pickle"
    st.text_area("Generated leadership output", brief, height=390)
    st.download_button("Download brief", data=brief, file_name="kori_pickle_revenue_operations_brief.txt", mime="text/plain")

with tab_e:
    st.markdown("## Responsible Data Governance")
    st.markdown('<div class="dark-panel"><h3>Synthetic Portfolio Standard</h3><p>This public platform uses synthetic data only. It is built for healthcare operations learning, portfolio demonstration, workflow intelligence, and responsible technology positioning.</p></div>', unsafe_allow_html=True)
    boundary = pd.DataFrame([
        ["Synthetic case identifiers", "Allowed"],
        ["Fake payer groups", "Allowed"],
        ["Simulated authorization aging", "Allowed"],
        ["Simulated documentation gaps", "Allowed"],
        ["Simulated exposure values", "Allowed"],
        ["Protected data", "Not used"],
        ["EHR screenshots", "Not used"],
    ], columns=["Data Element", "Portfolio Status"])
    st.dataframe(boundary, hide_index=True, use_container_width=True)

st.markdown('<div class="panel" style="text-align:center; margin-top:3rem;"><div class="kicker">Created by Kori Pickle</div><div class="signature">Kori Pickle</div><p style="color:rgb(0,0,0); font-weight:800;">Healthcare Operations Intelligence • Revenue Cycle • Patient Access • Prior Authorization • Denial Prevention</p><a class="icon-pill" href="https://www.linkedin.com" target="_blank">in LinkedIn</a><a class="icon-pill" href="https://github.com/koripickle1101-TN" target="_blank">GitHub</a></div>', unsafe_allow_html=True)
