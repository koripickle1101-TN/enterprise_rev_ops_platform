import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Enterprise Revenue Operations Platform",
    page_icon="🟠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ORANGE = "rgb(255, 130, 0)"
BLACK = "rgb(0, 0, 0)"
WHITE = "rgb(255, 255, 255)"
WARM = "rgb(246, 243, 238)"
LINE = "rgb(230, 224, 216)"
INK = "rgb(24, 24, 24)"

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800;900&family=Inter:wght@400;500;600;700;800&family=Great+Vibes&display=swap');

    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: rgb(255, 255, 255);
        color: rgb(0, 0, 0);
        font-family: Inter, sans-serif;
    }

    [data-testid="stSidebar"] {
        background: rgb(255, 255, 255);
        border-right: 1px solid rgb(230, 224, 216);
    }

    [data-testid="stSidebar"] label {
        color: rgb(0, 0, 0) !important;
        font-weight: 800 !important;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-size: 0.70rem;
    }

    div[data-baseweb="select"] > div {
        background: rgb(255, 255, 255) !important;
        border: 1px solid rgb(230, 224, 216) !important;
        border-radius: 18px !important;
        box-shadow: 0 10px 28px rgba(0,0,0,0.05) !important;
    }

    span[data-baseweb="tag"] {
        background: rgb(255, 130, 0) !important;
        color: rgb(0, 0, 0) !important;
        border-radius: 999px !important;
        font-weight: 800 !important;
    }

    .block-container {
        padding-top: 2.2rem;
        padding-left: 5.2rem;
        padding-right: 5.2rem;
        max-width: 1560px;
    }

    h1, h2, h3 {
        font-family: "Playfair Display", Georgia, serif;
        color: rgb(0, 0, 0);
        letter-spacing: -0.05em;
    }

    .brand-shell {
        display: grid;
        grid-template-columns: 1.25fr 0.75fr;
        gap: 2rem;
        align-items: stretch;
        margin-bottom: 2rem;
    }

    .hero-card {
        border: 1px solid rgb(230, 224, 216);
        border-radius: 38px;
        padding: 3.6rem;
        background: linear-gradient(135deg, rgb(255,255,255) 0%, rgb(255,248,239) 100%);
        box-shadow: 0 28px 75px rgba(0,0,0,0.065);
        min-height: 530px;
        position: relative;
        overflow: hidden;
    }

    .hero-card:after {
        content: "";
        position: absolute;
        right: -90px;
        bottom: -90px;
        width: 260px;
        height: 260px;
        border: 2px dotted rgb(255,130,0);
        border-radius: 50%;
        opacity: 0.25;
    }

    .brand-mark {
        border: 1px solid rgb(230, 224, 216);
        border-radius: 38px;
        background: rgb(0, 0, 0);
        color: rgb(255, 255, 255);
        padding: 2.2rem;
        box-shadow: 0 28px 75px rgba(0,0,0,0.14);
        position: relative;
        overflow: hidden;
    }

    .brand-mark:before {
        content: "";
        position: absolute;
        top: 2rem;
        right: 2rem;
        width: 150px;
        height: 150px;
        border: 2px solid rgb(255,130,0);
        border-radius: 50%;
        box-shadow: inset 0 0 0 18px rgb(22,22,22), 0 0 45px rgba(255,130,0,0.28);
    }

    .kicker {
        font-size: 0.72rem;
        letter-spacing: 0.32em;
        text-transform: uppercase;
        font-weight: 900;
        color: rgb(0,0,0);
        margin-bottom: 1rem;
    }

    .brand-mark .kicker { color: rgb(255,255,255); }

    .hero-title {
        font-family: "Playfair Display", Georgia, serif;
        font-size: clamp(3.1rem, 7vw, 6.4rem);
        line-height: 0.88;
        letter-spacing: -0.075em;
        font-weight: 900;
        margin: 0;
    }

    .orange { color: rgb(255,130,0); }

    .orange-line {
        width: 190px;
        height: 3px;
        background: rgb(255,130,0);
        margin-top: 1.5rem;
        margin-bottom: 1.6rem;
    }

    .hero-copy {
        font-size: 1.05rem;
        line-height: 1.78;
        color: rgb(24,24,24);
        max-width: 900px;
    }

    .badge {
        display: inline-block;
        padding: 0.58rem 0.86rem;
        margin-top: 0.75rem;
        margin-right: 0.45rem;
        border: 1px solid rgb(255,130,0);
        border-radius: 999px;
        background: rgb(255,251,245);
        color: rgb(0,0,0);
        font-size: 0.74rem;
        font-weight: 900;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .metric-card {
        border: 1px solid rgb(230,224,216);
        border-left: 6px solid rgb(255,130,0);
        border-radius: 26px;
        padding: 1.4rem;
        background: rgb(255,255,255);
        box-shadow: 0 18px 48px rgba(0,0,0,0.05);
        min-height: 150px;
    }

    .metric-label {
        font-size: 0.70rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        font-weight: 900;
        color: rgb(0,0,0);
        margin-bottom: 0.7rem;
    }

    .metric-value {
        font-family: "Playfair Display", Georgia, serif;
        font-size: 3rem;
        font-weight: 900;
        line-height: 0.95;
        color: rgb(255,130,0);
        font-variant-numeric: lining-nums;
    }

    .metric-note {
        font-size: 0.82rem;
        color: rgb(78,78,78);
        line-height: 1.45;
        margin-top: 0.85rem;
    }

    .panel {
        border: 1px solid rgb(230,224,216);
        border-radius: 30px;
        padding: 2.1rem;
        background: rgb(255,255,255);
        box-shadow: 0 20px 52px rgba(0,0,0,0.045);
        margin: 1.3rem 0;
    }

    .black-panel {
        border-radius: 32px;
        padding: 2.3rem;
        background: rgb(0,0,0);
        color: rgb(255,255,255);
        border-left: 8px solid rgb(255,130,0);
        box-shadow: 0 28px 65px rgba(0,0,0,0.18);
        margin: 1.3rem 0;
    }

    .black-panel h3 {
        color: rgb(255,255,255);
        font-size: 2.2rem;
        margin: 0 0 1rem 0;
    }

    .black-panel p { color: rgb(245,245,245); line-height: 1.7; }

    .node-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(140px, 1fr));
        gap: 1rem;
        margin-top: 1.4rem;
    }

    .node {
        border: 2px solid rgb(255,130,0);
        border-radius: 999px;
        min-height: 84px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        background: rgb(255,255,255);
        box-shadow: inset 0 0 0 10px rgb(255,246,235), 0 0 28px rgba(255,130,0,0.13);
        font-size: 0.73rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        padding: 0.9rem;
    }

    .signature {
        font-family: "Great Vibes", cursive;
        font-size: 3.8rem;
        color: rgb(20,20,20);
        line-height: 1;
        transform: rotate(-1deg);
        margin-top: 0.3rem;
        margin-bottom: 0.8rem;
    }

    .icon-pill {
        display: inline-block;
        border: 1px solid rgb(230,224,216);
        border-radius: 999px;
        padding: 0.55rem 0.8rem;
        margin: 0.25rem;
        color: rgb(0,0,0) !important;
        text-decoration: none !important;
        font-size: 0.75rem;
        font-weight: 900;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    div[data-testid="stMetric"] {
        background: rgb(255,255,255);
        border: 1px solid rgb(230,224,216);
        border-left: 6px solid rgb(255,130,0);
        border-radius: 24px;
        padding: 1rem;
    }

    div[data-testid="stMetricValue"] {
        color: rgb(255,130,0);
        font-family: "Playfair Display", Georgia, serif;
        font-size: 2.2rem;
        font-weight: 900;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 999px;
        background: rgb(255,251,245);
        border: 1px solid rgb(230,224,216);
        padding: 0.7rem 1rem;
        font-weight: 900;
        color: rgb(0,0,0);
    }

    [data-testid="stMainMenu"], footer { visibility: hidden; }

    @media (max-width: 950px) {
        .block-container { padding-left: 1rem; padding-right: 1rem; }
        .brand-shell { grid-template-columns: 1fr; }
        .hero-card { padding: 2rem; min-height: auto; }
        .node-grid { grid-template-columns: 1fr; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def build_records():
    data = [
        ["REV-0001", "Commercial", "Patient Access", "Orthopedics", "Eligibility mismatch", 9, 12600, "High", "Missing subscriber relation", "Escalate eligibility verification"],
        ["REV-0002", "Medicare Advantage", "Authorization Control", "Cardiology", "Aging authorization", 6, 28750, "High", "Pending clinical packet", "Request documentation packet"],
        ["REV-0003", "Medicaid", "Documentation Readiness", "Rehabilitation", "Incomplete plan of care", 4, 9300, "Moderate", "Therapy notes incomplete", "Validate documentation readiness"],
        ["REV-0004", "Commercial", "Routing Intelligence", "Imaging", "Wrong portal route", 8, 14500, "High", "Benefit manager carve out", "Confirm routing owner"],
        ["REV-0005", "Marketplace", "Eligibility Verification", "Primary Care", "Coverage inactive", 3, 4200, "Moderate", "Coverage termination risk", "Recheck eligibility"],
        ["REV-0006", "Self Pay", "Financial Clearance", "Surgery", "Estimate not completed", 2, 6800, "Low", "Patient estimate missing", "Create estimate review"],
        ["REV-0007", "Commercial", "Denial Prevention", "Oncology", "Medical necessity exposure", 7, 33100, "High", "Policy criteria unclear", "Route to human review"],
        ["REV-0008", "Medicare Advantage", "Authorization Control", "Neurology", "SLA risk", 5, 18500, "Moderate", "Authorization pending five days", "Escalate payer follow up"],
        ["REV-0009", "Medicaid", "Documentation Readiness", "Behavioral Health", "Missing referral", 6, 7600, "Moderate", "Referral not attached", "Attach referral evidence"],
        ["REV-0010", "Commercial", "Eligibility Verification", "Cardiology", "COB conflict", 8, 22100, "High", "Coordination of benefits unresolved", "Validate primary payer"],
        ["REV-0011", "Marketplace", "Routing Intelligence", "Imaging", "Payer policy mismatch", 7, 11900, "High", "Delegated review required", "Check benefit manager"],
        ["REV-0012", "Medicare Advantage", "Denial Prevention", "Rehabilitation", "Appeal exposure", 5, 15200, "Moderate", "Denial reason pattern detected", "Prepare prevention brief"],
    ]
    columns = ["case_id", "payer_group", "workflow_domain", "service_line", "signal", "aging_days", "synthetic_exposure", "risk_level", "root_cause", "recommended_action"]
    return pd.DataFrame(data, columns=columns)

records = build_records()

st.sidebar.markdown("### Control Filters")
risk_filter = st.sidebar.multiselect("Filter by risk level", sorted(records["risk_level"].unique()), default=sorted(records["risk_level"].unique()))
payer_filter = st.sidebar.multiselect("Filter by payer group", sorted(records["payer_group"].unique()), default=sorted(records["payer_group"].unique()))
domain_filter = st.sidebar.multiselect("Filter by workflow area", sorted(records["workflow_domain"].unique()), default=sorted(records["workflow_domain"].unique()))

filtered = records[
    records["risk_level"].isin(risk_filter)
    & records["payer_group"].isin(payer_filter)
    & records["workflow_domain"].isin(domain_filter)
]

high_count = int((filtered["risk_level"] == "High").sum())
sla_count = int((filtered["aging_days"] >= 5).sum())
exposure = int(filtered["synthetic_exposure"].sum()) if not filtered.empty else 0
avg_age = round(float(filtered["aging_days"].mean()), 1) if not filtered.empty else 0

st.markdown("""
<div class="brand-shell">
    <div class="hero-card">
        <div class="kicker">Kori Pickle • Healthcare Operations Intelligence</div>
        <h1 class="hero-title">Enterprise Revenue <span class="orange">Operations</span> Platform</h1>
        <div class="orange-line"></div>
        <p class="hero-copy">
            A premium synthetic healthcare operations control system for patient access, eligibility verification,
            prior authorization pressure, routing intelligence, documentation readiness, denial prevention,
            payer friction, and leadership reporting.
        </p>
        <p class="hero-copy">
            Built as a public portfolio artifact using synthetic records only. The platform demonstrates operational review signals,
            not clinical judgment, payer determination, coding direction, billing direction, or case specific recommendations.
        </p>
        <span class="badge">Synthetic Data</span>
        <span class="badge">Human Review Required</span>
        <span class="badge">No Real Records</span>
        <span class="badge">Built by Kori Pickle</span>
    </div>
    <div class="brand-mark">
        <div class="kicker">Operational Identity</div>
        <h3 style="color:white; font-size:2.8rem; line-height:0.95; margin-top:8rem;">Workflow visibility before revenue damage.</h3>
        <p style="color:rgb(245,245,245); line-height:1.7;">Designed around one question: where did the workflow first lose control?</p>
    </div>
</div>
""", unsafe_allow_html=True)

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
    st.write("Use the sidebar filters to isolate operational pressure across payer, workflow domain, and risk level.")
    st.dataframe(filtered, hide_index=True, use_container_width=True)
    left, right = st.columns([5, 4])
    with left:
        risk_summary = filtered.groupby("risk_level")["case_id"].count().reset_index(name="records")
        st.markdown("### Risk Queue Distribution")
        st.bar_chart(risk_summary.set_index("risk_level"))
    with right:
        st.markdown(f"""
        <div class="black-panel">
            <h3>Executive Interpretation</h3>
            <p>The current filtered view shows {len(filtered)} synthetic records, {high_count} high risk records, {sla_count} SLA pressure signals, and ${exposure:,.0f} in simulated exposure. These are prioritization signals for human review, not automated determinations.</p>
        </div>
        """, unsafe_allow_html=True)

with tab_b:
    st.markdown("## Revenue Operations Control Grid")
    st.markdown("""
    <div class="panel">
        <div class="kicker">Workflow Chain</div>
        <div class="node-grid">
            <div class="node">Patient Access Intake</div>
            <div class="node">Eligibility Control</div>
            <div class="node">Routing Intelligence</div>
            <div class="node">Authorization Aging</div>
            <div class="node">Documentation Readiness</div>
            <div class="node">Denial Prevention</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
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
        brief = f"Enterprise Revenue Operations Brief\n\nCurrent synthetic command center view shows {len(filtered)} records, {high_count} high risk records, {sla_count} SLA pressure signals, average aging of {avg_age} days, and ${exposure:,.0f} in simulated exposure.\n\nPrimary concern:\nWorkflow pressure is forming before downstream denial activity. The most important control points are eligibility verification, routing ownership, documentation readiness, authorization aging, and payer follow up.\n\nRecommended actions:\n1. Prioritize high risk records for human review.\n2. Validate payer routing before submission.\n3. Confirm documentation readiness before follow up.\n4. Track aged requests by payer and service line.\n5. Maintain responsible use boundaries.\n\nCreated by Kori Pickle"
    elif brief_type == "Daily huddle script":
        brief = f"Daily Huddle Script\n\nToday we are reviewing {len(filtered)} synthetic workflow records.\n\nFocus areas:\nHigh risk queue: {high_count}\nSLA pressure queue: {sla_count}\nSimulated exposure: ${exposure:,.0f}\n\nHuddle questions:\n1. Which records are aging before payer response?\n2. Which requests may be routed incorrectly?\n3. Which documentation packets need review?\n4. What can be stabilized today before rework, delay, denial, or patient frustration occurs?\n\nCreated by Kori Pickle"
    else:
        brief = "Denial Prevention Action Plan\n\nObjective:\nUse early workflow visibility to identify operational risk before downstream denial activity develops.\n\nPriorities:\n1. Eligibility mismatch review\n2. Authorization aging review\n3. Documentation readiness review\n4. Payer routing validation\n5. Follow up escalation\n6. Human review governance\n\nOperating question:\nWhere did the workflow first lose control?\n\nCreated by Kori Pickle"
    st.text_area("Generated leadership output", brief, height=390)
    st.download_button("Download brief", data=brief, file_name="kori_pickle_revenue_operations_brief.txt", mime="text/plain")

with tab_e:
    st.markdown("## Responsible Data Governance")
    st.markdown("""
    <div class="black-panel">
        <h3>Synthetic Portfolio Standard</h3>
        <p>This public platform uses synthetic data only. It is built for healthcare operations learning, portfolio demonstration, workflow intelligence, and responsible technology positioning.</p>
        <p>It does not use real records, EHR screenshots, claim files, member identifiers, or organization owned production data.</p>
    </div>
    <div class="black-panel">
        <h3>Use Boundary</h3>
        <p>The platform does not make clinical decisions, payer decisions, coding decisions, billing determinations, medical necessity decisions, or case specific recommendations. All outputs are operational review signals requiring human validation.</p>
    </div>
    """, unsafe_allow_html=True)
    boundary = pd.DataFrame([
        ["Synthetic case identifiers", "Allowed"],
        ["Fake payer groups", "Allowed"],
        ["Simulated authorization aging", "Allowed"],
        ["Simulated documentation gaps", "Allowed"],
        ["Simulated exposure values", "Allowed"],
        ["Real records", "Not used"],
        ["EHR screenshots", "Not used"],
        ["Organization owned production data", "Not used"],
    ], columns=["Data Element", "Portfolio Status"])
    st.dataframe(boundary, hide_index=True, use_container_width=True)

st.markdown("""
<div class="panel" style="text-align:center; margin-top:3rem;">
    <div class="kicker">Created by Kori Pickle</div>
    <div class="signature">Kori Pickle</div>
    <p class="small">Healthcare Operations Intelligence • Revenue Cycle • Patient Access • Prior Authorization • Denial Prevention</p>
    <a class="icon-pill" href="https://www.linkedin.com" target="_blank">in LinkedIn</a>
    <a class="icon-pill" href="https://github.com/koripickle1101-TN" target="_blank">GitHub</a>
</div>
""", unsafe_allow_html=True)
