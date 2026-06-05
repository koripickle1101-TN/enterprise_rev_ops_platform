import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Enterprise Revenue Operations Platform",
    page_icon="🟠",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_logo():
    logo_path = Path("assets/brand_logo.b64")
    if logo_path.exists():
        return logo_path.read_text().strip()
    return ""


logo_b64 = load_logo()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --orange: rgb(255, 130, 0);
    --black: rgb(0, 0, 0);
    --white: rgb(255, 255, 255);
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"] {
    background: var(--white) !important;
    color: var(--black) !important;
}

.block-container {
    padding-top: 2.4rem !important;
    padding-left: 4.5rem !important;
    padding-right: 4.5rem !important;
    padding-bottom: 4rem !important;
    max-width: 1480px !important;
}

h1, h2, h3 {
    font-family: "Playfair Display", Georgia, serif !important;
    color: var(--black) !important;
    letter-spacing: -0.045em !important;
    font-weight: 600 !important;
}

p, div, label, span, button {
    font-family: Inter, Arial, sans-serif !important;
}

[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 2px solid var(--black) !important;
}

[data-testid="stSidebar"] label {
    color: var(--black) !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
    color: var(--black) !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
textarea {
    background: var(--white) !important;
    color: var(--black) !important;
    border: 2px solid var(--black) !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

span[data-baseweb="tag"], [data-baseweb="tag"] {
    background: var(--white) !important;
    color: var(--black) !important;
    border: 2px solid var(--orange) !important;
    border-radius: 0 !important;
    font-weight: 700 !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.7rem;
}

.stTabs [data-baseweb="tab"] {
    background: var(--white) !important;
    color: var(--black) !important;
    border: 2px solid var(--black) !important;
    border-radius: 0 !important;
    padding: 0.75rem 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em !important;
}

.stTabs [aria-selected="true"] {
    background: var(--black) !important;
    color: var(--white) !important;
    border-color: var(--black) !important;
}

.stTabs [aria-selected="true"] p {
    color: var(--white) !important;
}

.brand-shell {
    border: 2px solid var(--black);
    background: var(--white);
    padding: 2.35rem;
    margin-bottom: 2rem;
}

.brand-logo {
    width: 100%;
    max-width: 940px;
    display: block;
    margin: 0 auto 2.3rem auto;
}

.hero {
    display: grid;
    grid-template-columns: 1.08fr 0.92fr;
    gap: 2.35rem;
    align-items: stretch;
}

.hero-left {
    border-top: 8px solid var(--orange);
    padding-top: 2rem;
}

.kicker {
    font-size: 0.74rem;
    letter-spacing: 0.34em;
    text-transform: uppercase;
    font-weight: 800;
    color: var(--black);
    margin-bottom: 1.1rem;
}

.hero-title {
    font-family: "Playfair Display", Georgia, serif !important;
    font-size: clamp(3.6rem, 7vw, 6.8rem);
    line-height: 0.92;
    letter-spacing: -0.065em;
    font-weight: 600;
    color: var(--black);
    margin: 0;
}

.orange-word {
    color: var(--orange);
}

.hero-copy {
    max-width: 830px;
    margin-top: 1.7rem;
    font-size: 1.08rem;
    line-height: 1.78;
    font-weight: 600;
    color: var(--black);
}

.identity-card {
    border: 2px solid var(--black);
    padding: 2rem;
    min-height: 395px;
    position: relative;
    overflow: hidden;
    background: var(--white);
}

.identity-card:before {
    content: "";
    position: absolute;
    width: 210px;
    height: 210px;
    border: 5px solid var(--orange);
    border-radius: 50%;
    top: -45px;
    right: -45px;
    box-shadow: inset 0 0 0 28px var(--white), inset 0 0 0 32px var(--orange);
}

.identity-title {
    position: relative;
    z-index: 2;
    margin-top: 10rem;
    font-family: "Playfair Display", Georgia, serif !important;
    font-size: clamp(2.1rem, 4vw, 3.45rem);
    line-height: 1;
    letter-spacing: -0.045em;
    font-weight: 600;
    color: var(--black);
}

.identity-card p {
    position: relative;
    z-index: 2;
    font-size: 1rem;
    line-height: 1.65;
    font-weight: 600;
    color: var(--black);
}

.badge-row {
    margin-top: 1.25rem;
}

.badge {
    display: inline-block;
    border: 2px solid var(--black);
    border-left: 8px solid var(--orange);
    padding: 0.55rem 0.85rem;
    margin: 0.35rem 0.35rem 0.35rem 0;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--black);
    background: var(--white);
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 1.25rem;
    margin: 2rem 0;
}

.metric-card {
    background: var(--white);
    color: var(--black);
    border: 2px solid var(--black);
    border-top: 7px solid var(--orange);
    padding: 1.5rem;
    min-height: 180px;
}

.metric-label {
    font-size: 0.68rem;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    font-weight: 800;
    color: var(--black);
    margin-bottom: 0.9rem;
}

.metric-value {
    font-family: "Cormorant Garamond", "Playfair Display", Georgia, serif !important;
    font-size: clamp(3rem, 5.4vw, 5.4rem);
    font-weight: 500;
    letter-spacing: -0.035em;
    line-height: 0.9;
    color: var(--black);
}

.metric-value .orange-number {
    color: var(--orange);
    font-family: "Cormorant Garamond", "Playfair Display", Georgia, serif !important;
    font-weight: 500;
}

.metric-note {
    font-size: 0.88rem;
    color: var(--black);
    line-height: 1.45;
    margin-top: 1.05rem;
    font-weight: 600;
}

.section-panel {
    border: 2px solid var(--black);
    background: var(--white);
    padding: 2rem;
    margin: 1.3rem 0;
}

.section-title {
    font-family: "Playfair Display", Georgia, serif !important;
    font-size: clamp(2.2rem, 5vw, 4rem);
    line-height: 0.98;
    letter-spacing: -0.045em;
    font-weight: 600;
    margin-bottom: 1rem;
}

.black-panel {
    background: var(--black);
    color: var(--white);
    border: 2px solid var(--black);
    border-top: 8px solid var(--orange);
    padding: 2rem;
    margin: 1rem 0;
}

.black-panel h3, .black-panel p, .black-panel div {
    color: var(--white) !important;
}

.black-panel h3 {
    font-family: "Playfair Display", Georgia, serif !important;
    font-size: 2.25rem;
    line-height: 1;
    letter-spacing: -0.04em;
    font-weight: 600;
    margin: 0 0 1rem 0;
}

.node-map {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 0.85rem;
    margin-top: 1.5rem;
}

.node {
    min-height: 96px;
    border: 2px solid var(--orange);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: var(--black);
    font-weight: 800;
    font-size: 0.68rem;
    line-height: 1.15;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    box-shadow: inset 0 0 0 9px var(--white), inset 0 0 0 11px var(--orange);
    padding: 1rem;
}

.custom-bar-row {
    display: grid;
    grid-template-columns: 160px 1fr 60px;
    gap: 1rem;
    align-items: center;
    margin: 0.9rem 0;
    font-weight: 700;
}

.custom-bar-track {
    height: 18px;
    border: 2px solid var(--black);
    background: var(--white);
}

.custom-bar-fill {
    height: 100%;
    background: var(--orange);
}

.footer-brand {
    text-align: center;
    border-top: 3px solid var(--orange);
    border-bottom: 3px solid var(--orange);
    padding: 2.5rem 1rem;
    margin-top: 3rem;
}

.footer-logo {
    width: 100%;
    max-width: 760px;
    display: block;
    margin: 0 auto 1rem auto;
}

.icon-link {
    display: inline-block;
    color: var(--black) !important;
    background: var(--white);
    border: 2px solid var(--black);
    padding: 0.65rem 0.95rem;
    margin: 0.3rem;
    text-decoration: none !important;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.icon-link:hover {
    background: var(--orange);
}

[data-testid="stDataFrame"] {
    border: 2px solid var(--black);
}

[data-testid="stMetricValue"] {
    font-family: "Cormorant Garamond", "Playfair Display", Georgia, serif !important;
    color: var(--black) !important;
    font-weight: 500 !important;
}

[data-testid="stMainMenu"], footer {
    visibility: hidden;
}

@media (max-width: 980px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    .hero {
        grid-template-columns: 1fr;
    }
    .brand-shell {
        padding: 1.2rem;
    }
    .metric-grid {
        grid-template-columns: 1fr;
    }
    .node-map {
        grid-template-columns: repeat(2, 1fr);
    }
    .node {
        border-radius: 0;
    }
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
    columns = ["Case ID", "Payer Group", "Workflow Domain", "Service Line", "Signal", "Aging Days", "Synthetic Exposure", "Risk Level", "Root Cause", "Recommended Action"]
    return pd.DataFrame(data, columns=columns)


records = build_records()

st.sidebar.markdown("### Command Filters")
risk_filter = st.sidebar.multiselect("Filter by risk level", sorted(records["Risk Level"].unique()), default=sorted(records["Risk Level"].unique()))
payer_filter = st.sidebar.multiselect("Filter by payer group", sorted(records["Payer Group"].unique()), default=sorted(records["Payer Group"].unique()))
domain_filter = st.sidebar.multiselect("Filter by workflow area", sorted(records["Workflow Domain"].unique()), default=sorted(records["Workflow Domain"].unique()))

filtered = records[
    records["Risk Level"].isin(risk_filter)
    & records["Payer Group"].isin(payer_filter)
    & records["Workflow Domain"].isin(domain_filter)
]

high_count = int((filtered["Risk Level"] == "High").sum())
sla_count = int((filtered["Aging Days"] >= 5).sum())
exposure = int(filtered["Synthetic Exposure"].sum()) if not filtered.empty else 0
avg_age = round(float(filtered["Aging Days"].mean()), 1) if not filtered.empty else 0

logo_img = f'<img class="brand-logo" src="data:image/png;base64,{logo_b64}" alt="Kori Pickle Healthcare Operations Intelligence Logo" />' if logo_b64 else ""
footer_logo = f'<img class="footer-logo" src="data:image/png;base64,{logo_b64}" alt="Kori Pickle Healthcare Operations Intelligence Logo" />' if logo_b64 else ""

st.markdown(f"""
<div class="brand-shell">
    {logo_img}
    <div class="hero">
        <div class="hero-left">
            <div class="kicker">Kori Pickle • Healthcare Operations Intelligence</div>
            <div class="hero-title">Enterprise Revenue <span class="orange-word">Operations</span> Platform</div>
            <p class="hero-copy">A premium synthetic no PHI healthcare operations command center for patient access, eligibility verification, prior authorization pressure tracking, documentation readiness, denial prevention, payer friction analysis, and responsible operational intelligence.</p>
            <p class="hero-copy">This working portfolio system is built around operational review signals, human oversight, and workflow stabilization logic.</p>
            <div class="badge-row">
                <span class="badge">No PHI</span>
                <span class="badge">Synthetic Data</span>
                <span class="badge">Human Review Required</span>
                <span class="badge">Built by Kori Pickle</span>
            </div>
        </div>
        <div class="identity-card">
            <div class="kicker">Operational Identity</div>
            <div class="identity-title">Workflow visibility before revenue damage.</div>
            <p>Designed around one question: where did the workflow first lose control?</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-label">High Risk Records</div>
        <div class="metric-value"><span class="orange-number">{high_count}</span></div>
        <div class="metric-note">Filtered operational review queue.</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">SLA Risk Signals</div>
        <div class="metric-value"><span class="orange-number">{sla_count}</span></div>
        <div class="metric-note">Records aging at or above five days.</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Synthetic Exposure</div>
        <div class="metric-value"><span class="orange-number">${exposure:,.0f}</span></div>
        <div class="metric-note">Portfolio simulation only.</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Academic Standing</div>
        <div class="metric-value"><span class="orange-number">99</span> / 120</div>
        <div class="metric-note">BSHA candidate • GPA 3.6.</div>
    </div>
</div>
""", unsafe_allow_html=True)

tab_a, tab_b, tab_c, tab_d, tab_e = st.tabs(["Command Center", "Control Grid", "Friction Map", "Brief Builder", "Governance"])

with tab_a:
    st.markdown('<div class="section-title">Live Command Center</div>', unsafe_allow_html=True)
    st.write("Use the sidebar filters to isolate operational pressure across payer group, workflow domain, and risk level.")
    st.dataframe(filtered, hide_index=True, use_container_width=True)

    summary = filtered.groupby("Risk Level")["Case ID"].count().reset_index(name="Records")
    max_records = int(summary["Records"].max()) if not summary.empty else 1
    bars = ""
    for _, row in summary.iterrows():
        width = int((row["Records"] / max_records) * 100) if max_records else 0
        bars += f'<div class="custom-bar-row"><div>{row["Risk Level"]}</div><div class="custom-bar-track"><div class="custom-bar-fill" style="width:{width}%;"></div></div><div>{row["Records"]}</div></div>'

    left, right = st.columns([5, 4])
    with left:
        st.markdown(f'<div class="section-panel"><div class="kicker">Risk Queue Distribution</div>{bars}</div>', unsafe_allow_html=True)
    with right:
        st.markdown(f'<div class="black-panel"><h3>Executive Interpretation</h3><p>The filtered view shows {len(filtered)} synthetic records, {high_count} high risk records, {sla_count} SLA pressure signals, average aging of {avg_age} days, and ${exposure:,.0f} in simulated exposure. These are prioritization signals for human review, not automated decisions.</p></div>', unsafe_allow_html=True)

with tab_b:
    st.markdown('<div class="section-title">Revenue Operations Control Grid</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-panel"><div class="kicker">Workflow Intelligence Chain</div><div class="node-map"><div class="node">Patient Access Intake</div><div class="node">Eligibility Control</div><div class="node">Routing Intelligence</div><div class="node">Authorization Aging</div><div class="node">Documentation Readiness</div><div class="node">Denial Prevention</div></div></div>', unsafe_allow_html=True)
    domain_summary = filtered.groupby("Workflow Domain").agg(Records=("Case ID", "count"), Exposure=("Synthetic Exposure", "sum"), Average_Aging=("Aging Days", "mean")).reset_index()
    domain_summary["Average_Aging"] = domain_summary["Average_Aging"].round(1)
    st.dataframe(domain_summary, hide_index=True, use_container_width=True)

    st.markdown('<div class="section-panel"><div class="kicker">Stabilization Simulator</div>', unsafe_allow_html=True)
    volume = st.number_input("Monthly front end record volume", min_value=0, value=15000, step=500)
    friction = st.slider("Estimated workflow friction rate", min_value=0.01, max_value=0.25, value=0.08, step=0.01)
    capture = st.slider("Estimated stabilization capture rate", min_value=0.25, max_value=0.95, value=0.85, step=0.05)
    flagged = volume * friction
    stabilized = flagged * capture
    s1, s2, s3 = st.columns(3)
    s1.metric("Projected Records Flagged", f"{int(flagged):,}")
    s2.metric("Projected Records Stabilized", f"{int(stabilized):,}")
    s3.metric("Residual Review Queue", f"{int(flagged - stabilized):,}")
    st.markdown('</div>', unsafe_allow_html=True)

with tab_c:
    st.markdown('<div class="section-title">Payer Friction Map</div>', unsafe_allow_html=True)
    payer_summary = filtered.groupby("Payer Group").agg(Records=("Case ID", "count"), Exposure=("Synthetic Exposure", "sum"), Average_Aging=("Aging Days", "mean"), High_Risk=("Risk Level", lambda s: int((s == "High").sum()))).reset_index()
    payer_summary["Average_Aging"] = payer_summary["Average_Aging"].round(1)
    payer_summary["Friction Score"] = (payer_summary["Records"] * 8 + payer_summary["High_Risk"] * 25 + payer_summary["Average_Aging"] * 6).round(0).astype(int)
    st.dataframe(payer_summary.sort_values("Friction Score", ascending=False), hide_index=True, use_container_width=True)
    max_score = int(payer_summary["Friction Score"].max()) if not payer_summary.empty else 1
    payer_bars = ""
    for _, row in payer_summary.sort_values("Friction Score", ascending=False).iterrows():
        width = int((row["Friction Score"] / max_score) * 100) if max_score else 0
        payer_bars += f'<div class="custom-bar-row"><div>{row["Payer Group"]}</div><div class="custom-bar-track"><div class="custom-bar-fill" style="width:{width}%;"></div></div><div>{row["Friction Score"]}</div></div>'
    st.markdown(f'<div class="section-panel"><div class="kicker">Payer Pressure Index</div>{payer_bars}</div>', unsafe_allow_html=True)

with tab_d:
    st.markdown('<div class="section-title">Leadership Brief Builder</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="section-title">Responsible Data Governance</div>', unsafe_allow_html=True)
    st.markdown('<div class="black-panel"><h3>Synthetic Portfolio Standard</h3><p>This public platform uses synthetic data only. It is built for healthcare operations learning, portfolio demonstration, workflow intelligence, and responsible technology positioning.</p></div>', unsafe_allow_html=True)
    boundary = pd.DataFrame([
        ["Synthetic case identifiers", "Allowed"],
        ["Fake payer groups", "Allowed"],
        ["Simulated authorization aging", "Allowed"],
        ["Simulated documentation gaps", "Allowed"],
        ["Simulated exposure values", "Allowed"],
        ["Protected health information", "Not used"],
        ["Patient specific records", "Not used"],
        ["EHR screenshots", "Not used"],
    ], columns=["Data Element", "Portfolio Status"])
    st.dataframe(boundary, hide_index=True, use_container_width=True)

st.markdown(f"""
<div class="footer-brand">
    {footer_logo}
    <div class="kicker">Created by Kori Pickle</div>
    <p style="color:rgb(0,0,0); font-weight:700;">Healthcare Operations Intelligence • Revenue Cycle • Patient Access • Prior Authorization • Denial Prevention</p>
    <a class="icon-link" href="https://www.linkedin.com/in/kori-pickle" target="_blank">LinkedIn</a>
    <a class="icon-link" href="https://github.com/koripickle1101-TN" target="_blank">GitHub</a>
</div>
""", unsafe_allow_html=True)
