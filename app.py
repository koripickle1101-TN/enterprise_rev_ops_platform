import base64
from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Enterprise Revenue Operations Platform",
    page_icon="KP",
    layout="wide",
    initial_sidebar_state="expanded",
)

TENNESSEE_ORANGE = "rgb(255, 130, 0)"
BLACK = "rgb(0, 0, 0)"
WHITE = "rgb(255, 255, 255)"


def get_logo_bytes():
    logo_path = Path("assets/brand_logo.b64")
    if logo_path.exists():
        try:
            return base64.b64decode(logo_path.read_text().strip())
        except Exception:
            return None
    return None


logo_bytes = get_logo_bytes()

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600&display=swap');

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
    max-width: 1440px !important;
    padding-top: 2rem !important;
    padding-left: 4.5rem !important;
    padding-right: 4.5rem !important;
    padding-bottom: 5rem !important;
}

p, div, label, span, button, input, textarea {
    font-family: Inter, Arial, sans-serif !important;
    color: var(--black) !important;
}

h1, h2, h3 {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-weight: 400 !important;
    letter-spacing: -0.045em !important;
    color: var(--black) !important;
}

[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 2px solid var(--black) !important;
}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
    color: var(--black) !important;
}

[data-testid="stSidebar"] label {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
textarea,
[data-testid="stTextArea"] textarea {
    background: var(--white) !important;
    border: 1.6px solid var(--black) !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    color: var(--black) !important;
}

span[data-baseweb="tag"], [data-baseweb="tag"] {
    background: var(--white) !important;
    color: var(--black) !important;
    border: 1.6px solid var(--orange) !important;
    border-radius: 0 !important;
    font-weight: 500 !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.65rem;
    border-bottom: 1.6px solid var(--black);
    padding-bottom: 0.6rem;
}

.stTabs [data-baseweb="tab"] {
    background: var(--white) !important;
    border: 1.6px solid var(--black) !important;
    border-radius: 0 !important;
    padding: 0.7rem 1rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
}

.stTabs [aria-selected="true"] {
    background: var(--orange) !important;
    border-color: var(--orange) !important;
}

.stTabs [aria-selected="true"] p {
    color: var(--black) !important;
}

.hero-shell {
    border-left: 2px solid var(--black);
    border-right: 2px solid var(--black);
    padding: 2rem 2.2rem 2.3rem 2.2rem;
    margin-bottom: 2rem;
}

.brand-rule {
    width: 100%;
    height: 9px;
    background: var(--orange);
    margin: 1.5rem 0 2.1rem 0;
}

.kicker {
    font-size: 0.72rem;
    letter-spacing: 0.34em;
    text-transform: uppercase;
    font-weight: 600;
    color: var(--black);
    margin-bottom: 1.1rem;
}

.hero-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.2fr) minmax(310px, 0.8fr);
    gap: 2rem;
    align-items: stretch;
}

.hero-title {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: clamp(4.2rem, 8vw, 8rem);
    line-height: 0.82;
    letter-spacing: -0.075em;
    font-weight: 400;
    color: var(--black);
    margin: 0;
}

.orange-word {
    color: var(--orange);
    font-weight: 400;
}

.hero-copy {
    max-width: 900px;
    margin-top: 1.8rem;
    font-size: 1.04rem;
    line-height: 1.8;
    font-weight: 400;
}

.identity-panel {
    border: 1.6px solid var(--black);
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 420px;
    background: var(--white);
}

.identity-statement {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: clamp(2.2rem, 4.5vw, 4rem);
    line-height: 0.93;
    letter-spacing: -0.055em;
    font-weight: 400;
}

.signature-line {
    height: 2px;
    background: var(--orange);
    width: 64%;
    margin: 1.4rem 0;
}

.badge {
    display: inline-block;
    border: 1.6px solid var(--black);
    border-left: 8px solid var(--orange);
    padding: 0.6rem 0.85rem;
    margin: 0.35rem 0.35rem 0.35rem 0;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    background: var(--white);
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 1rem;
    margin: 1.75rem 0 2.4rem 0;
}

.metric-card {
    border: 1.6px solid var(--black);
    background: var(--white);
    padding: 1.55rem;
    min-height: 170px;
    position: relative;
}

.metric-card:before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    width: 7px;
    height: 100%;
    background: var(--orange);
}

.metric-label {
    font-size: 0.68rem;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 0.9rem;
}

.metric-value {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: clamp(2.7rem, 4.6vw, 4.9rem);
    font-weight: 300;
    letter-spacing: -0.055em;
    line-height: 0.92;
    color: var(--black);
}

.orange-number {
    color: var(--orange);
    font-weight: 300;
}

.metric-note {
    font-size: 0.86rem;
    line-height: 1.5;
    margin-top: 1rem;
    font-weight: 400;
}

.section-panel {
    border: 1.6px solid var(--black);
    background: var(--white);
    padding: 2rem;
    margin: 1.2rem 0;
}

.section-title {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: clamp(2.4rem, 5vw, 4.5rem);
    line-height: 0.95;
    letter-spacing: -0.06em;
    font-weight: 400;
    margin: 1.8rem 0 0.8rem 0;
}

.editorial-note {
    border-left: 8px solid var(--orange);
    border-top: 1.6px solid var(--black);
    border-bottom: 1.6px solid var(--black);
    border-right: 1.6px solid var(--black);
    padding: 1.5rem;
    margin: 1rem 0;
    background: var(--white);
}

.editorial-note h3 {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: 2.8rem;
    line-height: 0.95;
    margin: 0 0 1rem 0;
    font-weight: 400 !important;
}

.process-grid {
    display: grid;
    grid-template-columns: repeat(6, minmax(0, 1fr));
    gap: 0.75rem;
    margin-top: 1.3rem;
}

.process-step {
    border: 1.6px solid var(--black);
    border-top: 7px solid var(--orange);
    padding: 1rem;
    min-height: 118px;
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    line-height: 1.35;
    background: var(--white);
}

.custom-bar-row {
    display: grid;
    grid-template-columns: 150px 1fr 58px;
    gap: 1rem;
    align-items: center;
    margin: 1rem 0;
    font-weight: 500;
}

.custom-bar-track {
    height: 15px;
    border: 1.6px solid var(--black);
    background: var(--white);
}

.custom-bar-fill {
    height: 100%;
    background: var(--orange);
}

.decision-card {
    border: 1.6px solid var(--black);
    padding: 1.35rem;
    margin: 0.85rem 0;
    background: var(--white);
}

.decision-title {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: 2rem;
    font-weight: 400;
    line-height: 1;
    margin-bottom: 0.5rem;
}

.small-caps {
    text-transform: uppercase;
    letter-spacing: 0.18em;
    font-size: 0.68rem;
    font-weight: 600;
}

.footer-brand {
    text-align: center;
    border-top: 3px solid var(--orange);
    border-bottom: 3px solid var(--orange);
    padding: 2.4rem 1rem;
    margin-top: 3rem;
}

.footer-logo-wrap img {
    width: min(760px, 100%);
    display: block;
    margin: 0 auto 1rem auto;
}

.footer-signature {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: 3.7rem;
    font-weight: 300;
    font-style: italic;
    letter-spacing: -0.04em;
    line-height: 1;
    margin: 0.7rem 0 0.4rem 0;
}

.icon-link {
    display: inline-block;
    border: 1.6px solid var(--black);
    padding: 0.65rem 1rem;
    margin: 0.3rem;
    text-decoration: none !important;
    font-size: 0.74rem;
    font-weight: 600;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    color: var(--black) !important;
}

.icon-link:hover {
    background: var(--orange);
}

[data-testid="stDataFrame"] {
    border: 1.6px solid var(--black);
}

[data-testid="stMetricValue"] {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-weight: 300 !important;
}

[data-testid="stMainMenu"], footer {
    visibility: hidden;
}

@media (max-width: 980px) {
    .block-container {
        padding-left: 0.9rem !important;
        padding-right: 0.9rem !important;
    }
    .hero-shell {
        padding: 1.2rem;
    }
    .hero-grid, .metric-grid, .process-grid {
        grid-template-columns: 1fr;
    }
    .hero-title {
        font-size: 4.3rem;
    }
    .custom-bar-row {
        grid-template-columns: 110px 1fr 42px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def build_records():
    rows = [
        ["REV-0001", "Commercial", "Patient Access", "Orthopedics", "Eligibility mismatch", 9, 12600, "High", "Subscriber relationship missing", "Eligibility correction", "Owner needed", "Registration desk"],
        ["REV-0002", "Medicare Advantage", "Authorization Control", "Cardiology", "Aging authorization", 6, 28750, "High", "Packet pending payer review", "Escalation", "Follow up due", "Authorization team"],
        ["REV-0003", "Medicaid", "Documentation Readiness", "Rehabilitation", "Incomplete plan of care", 4, 9300, "Moderate", "Therapy notes incomplete", "Documentation request", "Missing evidence", "Clinical documentation"],
        ["REV-0004", "Commercial", "Routing Intelligence", "Imaging", "Wrong portal route", 8, 14500, "High", "Benefit manager carve out", "Routing correction", "Portal mismatch", "Patient access lead"],
        ["REV-0005", "Marketplace", "Eligibility Verification", "Primary Care", "Coverage inactive", 3, 4200, "Moderate", "Coverage termination risk", "Recheck eligibility", "Coverage pending", "Eligibility desk"],
        ["REV-0006", "Self Pay", "Financial Clearance", "Surgery", "Estimate not completed", 2, 6800, "Low", "Patient estimate missing", "Financial counseling", "Estimate gap", "Financial clearance"],
        ["REV-0007", "Commercial", "Denial Prevention", "Oncology", "Policy criteria exposure", 7, 33100, "High", "Criteria unclear", "Human review", "Medical policy review", "Denial prevention"],
        ["REV-0008", "Medicare Advantage", "Authorization Control", "Neurology", "SLA pressure", 5, 18500, "Moderate", "Pending five days", "Escalate payer follow up", "Aging threshold", "Authorization team"],
        ["REV-0009", "Medicaid", "Documentation Readiness", "Behavioral Health", "Missing referral", 6, 7600, "Moderate", "Referral not attached", "Attach referral evidence", "Referral gap", "Intake support"],
        ["REV-0010", "Commercial", "Eligibility Verification", "Cardiology", "COB conflict", 8, 22100, "High", "Benefits unresolved", "Validate primary payer", "Coordination issue", "Eligibility desk"],
        ["REV-0011", "Marketplace", "Routing Intelligence", "Imaging", "Payer policy mismatch", 7, 11900, "High", "Delegated review required", "Check benefit manager", "Routing ambiguity", "Patient access lead"],
        ["REV-0012", "Medicare Advantage", "Denial Prevention", "Rehabilitation", "Appeal exposure", 5, 15200, "Moderate", "Denial reason pattern detected", "Prepare prevention brief", "Pattern forming", "Denial prevention"],
        ["REV-0013", "Commercial", "Patient Access", "Surgery", "Authorization not attached", 1, 9800, "Low", "Attachment missing from account", "Queue verification", "Pre bill risk", "Access coordinator"],
        ["REV-0014", "Medicare Advantage", "Documentation Readiness", "Orthopedics", "Medical necessity evidence gap", 10, 37600, "High", "Conservative therapy evidence missing", "Clinical packet rebuild", "Evidence gap", "Clinical documentation"],
    ]
    columns = [
        "Case ID", "Payer Group", "Workflow Domain", "Service Line", "Signal", "Aging Days", "Synthetic Exposure", "Risk Level", "Root Cause", "Recommended Action", "Control Gap", "Review Owner"
    ]
    return pd.DataFrame(rows, columns=columns)


records = build_records()

st.sidebar.markdown("### Command Filters")
risk_filter = st.sidebar.multiselect("Filter by risk level", sorted(records["Risk Level"].unique()), default=sorted(records["Risk Level"].unique()))
payer_filter = st.sidebar.multiselect("Filter by payer group", sorted(records["Payer Group"].unique()), default=sorted(records["Payer Group"].unique()))
domain_filter = st.sidebar.multiselect("Filter by workflow area", sorted(records["Workflow Domain"].unique()), default=sorted(records["Workflow Domain"].unique()))
service_filter = st.sidebar.multiselect("Filter by service line", sorted(records["Service Line"].unique()), default=sorted(records["Service Line"].unique()))
aging_threshold = st.sidebar.slider("SLA aging threshold", min_value=2, max_value=10, value=5, step=1)

filtered = records[
    records["Risk Level"].isin(risk_filter)
    & records["Payer Group"].isin(payer_filter)
    & records["Workflow Domain"].isin(domain_filter)
    & records["Service Line"].isin(service_filter)
]

high_count = int((filtered["Risk Level"] == "High").sum())
sla_count = int((filtered["Aging Days"] >= aging_threshold).sum())
exposure = int(filtered["Synthetic Exposure"].sum()) if not filtered.empty else 0
avg_age = round(float(filtered["Aging Days"].mean()), 1) if not filtered.empty else 0
owner_count = int(filtered["Review Owner"].nunique()) if not filtered.empty else 0

if logo_bytes:
    st.image(BytesIO(logo_bytes), use_container_width=True)

st.markdown(
    f"""
<div class="hero-shell">
    <div class="brand-rule"></div>
    <div class="hero-grid">
        <div>
            <div class="kicker">Kori Pickle • Healthcare Operations Intelligence</div>
            <div class="hero-title">Enterprise Revenue <span class="orange-word">Operations</span> Platform</div>
            <p class="hero-copy">A premium synthetic no PHI healthcare operations command center for patient access, eligibility verification, prior authorization pressure tracking, routing intelligence, documentation readiness, denial prevention, payer friction analysis, and leadership reporting.</p>
            <p class="hero-copy">This build is not another static dashboard. It functions as an operational review workbench: filter synthetic cases, isolate ownership gaps, simulate stabilization impact, generate escalation language, and build a leadership brief from the active command view.</p>
            <div>
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
                <div class="signature-line"></div>
                <p>Designed around one question: where did the workflow first lose control?</p>
            </div>
            <p class="small-caps">Patient access • authorization control • documentation readiness • denial prevention</p>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="metric-grid">
    <div class="metric-card"><div class="metric-label">High Risk Records</div><div class="metric-value"><span class="orange-number">{high_count}</span></div><div class="metric-note">Prioritized operational review queue.</div></div>
    <div class="metric-card"><div class="metric-label">SLA Pressure</div><div class="metric-value"><span class="orange-number">{sla_count}</span></div><div class="metric-note">Records aged at or above {aging_threshold} days.</div></div>
    <div class="metric-card"><div class="metric-label">Synthetic Exposure</div><div class="metric-value"><span class="orange-number">${exposure:,.0f}</span></div><div class="metric-note">Portfolio simulation only.</div></div>
    <div class="metric-card"><div class="metric-label">Ownership Spread</div><div class="metric-value"><span class="orange-number">{owner_count}</span></div><div class="metric-note">Distinct teams in the active review view.</div></div>
</div>
""",
    unsafe_allow_html=True,
)

tab_a, tab_b, tab_c, tab_d, tab_e, tab_f = st.tabs([
    "Command Center",
    "Ownership Grid",
    "Stabilization Lab",
    "Handoff Builder",
    "Leadership Brief",
    "Governance",
])

with tab_a:
    st.markdown('<div class="section-title">Live Command Center</div>', unsafe_allow_html=True)
    st.write("Use the sidebar filters to isolate operational pressure across payer group, workflow domain, service line, and risk level.")
    st.dataframe(filtered, hide_index=True, use_container_width=True)

    summary = filtered.groupby("Risk Level")["Case ID"].count().reset_index(name="Records") if not filtered.empty else pd.DataFrame(columns=["Risk Level", "Records"])
    max_records = int(summary["Records"].max()) if not summary.empty else 1
    bars = ""
    for _, row in summary.iterrows():
        width = int((row["Records"] / max_records) * 100) if max_records else 0
        bars += f'<div class="custom-bar-row"><div>{row["Risk Level"]}</div><div class="custom-bar-track"><div class="custom-bar-fill" style="width:{width}%;"></div></div><div>{row["Records"]}</div></div>'

    left, right = st.columns([5, 4])
    with left:
        st.markdown(f'<div class="section-panel"><div class="kicker">Risk Queue Distribution</div>{bars}</div>', unsafe_allow_html=True)
    with right:
        st.markdown(
            f'<div class="editorial-note"><h3>Executive Interpretation</h3><p>The active view shows {len(filtered)} synthetic records, {high_count} high risk records, {sla_count} SLA pressure signals, average aging of {avg_age} days, and ${exposure:,.0f} in simulated exposure. These are prioritization signals for human review, not automated payer or clinical decisions.</p></div>',
            unsafe_allow_html=True,
        )

with tab_b:
    st.markdown('<div class="section-title">Ownership Grid</div>', unsafe_allow_html=True)
    st.write("This view separates the operational failure point from the team responsible for stabilizing it.")
    st.markdown(
        '<div class="section-panel"><div class="kicker">Workflow Control Chain</div><div class="process-grid"><div class="process-step">Intake Signal</div><div class="process-step">Eligibility Control</div><div class="process-step">Routing Validation</div><div class="process-step">Authorization Aging</div><div class="process-step">Documentation Readiness</div><div class="process-step">Denial Prevention</div></div></div>',
        unsafe_allow_html=True,
    )
    owner_summary = filtered.groupby(["Review Owner", "Workflow Domain"]).agg(
        Records=("Case ID", "count"),
        Exposure=("Synthetic Exposure", "sum"),
        Average_Aging=("Aging Days", "mean"),
    ).reset_index() if not filtered.empty else pd.DataFrame(columns=["Review Owner", "Workflow Domain", "Records", "Exposure", "Average_Aging"])
    if not owner_summary.empty:
        owner_summary["Average_Aging"] = owner_summary["Average_Aging"].round(1)
    st.dataframe(owner_summary.sort_values("Exposure", ascending=False) if not owner_summary.empty else owner_summary, hide_index=True, use_container_width=True)

with tab_c:
    st.markdown('<div class="section-title">Stabilization Lab</div>', unsafe_allow_html=True)
    st.write("Model how stronger front end controls may reduce avoidable review burden before the claim or authorization becomes downstream rework.")
    col1, col2, col3 = st.columns(3)
    with col1:
        monthly_volume = st.number_input("Monthly front end record volume", min_value=0, value=18000, step=500)
    with col2:
        friction_rate = st.slider("Estimated workflow friction rate", min_value=0.01, max_value=0.25, value=0.08, step=0.01)
    with col3:
        capture_rate = st.slider("Stabilization capture rate", min_value=0.25, max_value=0.95, value=0.80, step=0.05)
    flagged = monthly_volume * friction_rate
    stabilized = flagged * capture_rate
    residual = flagged - stabilized
    st.markdown(
        f"""
<div class="metric-grid">
    <div class="metric-card"><div class="metric-label">Projected Flagged Records</div><div class="metric-value"><span class="orange-number">{int(flagged):,}</span></div><div class="metric-note">Records likely to need operational review.</div></div>
    <div class="metric-card"><div class="metric-label">Projected Stabilized</div><div class="metric-value"><span class="orange-number">{int(stabilized):,}</span></div><div class="metric-note">Records potentially stabilized before downstream escalation.</div></div>
    <div class="metric-card"><div class="metric-label">Residual Queue</div><div class="metric-value"><span class="orange-number">{int(residual):,}</span></div><div class="metric-note">Records still requiring manual follow up.</div></div>
    <div class="metric-card"><div class="metric-label">Control Lift</div><div class="metric-value"><span class="orange-number">{int(capture_rate * 100)}%</span></div><div class="metric-note">Synthetic operating assumption.</div></div>
</div>
""",
        unsafe_allow_html=True,
    )

with tab_d:
    st.markdown('<div class="section-title">Handoff Builder</div>', unsafe_allow_html=True)
    selected_case = st.selectbox("Select synthetic record", filtered["Case ID"].tolist() if not filtered.empty else records["Case ID"].tolist())
    case = records[records["Case ID"] == selected_case].iloc[0]
    handoff = f"""Operational Handoff\n\nCase: {case['Case ID']}\nPayer Group: {case['Payer Group']}\nWorkflow Domain: {case['Workflow Domain']}\nService Line: {case['Service Line']}\nRisk Level: {case['Risk Level']}\nAging Days: {case['Aging Days']}\nSynthetic Exposure: ${case['Synthetic Exposure']:,.0f}\n\nPrimary Signal:\n{case['Signal']}\n\nRoot Cause:\n{case['Root Cause']}\n\nControl Gap:\n{case['Control Gap']}\n\nRecommended Action:\n{case['Recommended Action']}\n\nAssigned Review Owner:\n{case['Review Owner']}\n\nHuman Review Boundary:\nThis is a synthetic portfolio artifact. It supports operational review thinking only and does not make payer, billing, coding, clinical, or patient specific decisions.\n\nCreated by Kori Pickle"""
    st.text_area("Generated handoff", handoff, height=390)
    st.download_button("Download handoff", data=handoff, file_name=f"{selected_case.lower()}_handoff.txt", mime="text/plain")

with tab_e:
    st.markdown('<div class="section-title">Leadership Brief</div>', unsafe_allow_html=True)
    brief_mode = st.selectbox("Brief output", ["Executive readout", "Daily huddle", "Payer friction memo", "Denial prevention note"])
    top_domain = filtered.groupby("Workflow Domain")["Case ID"].count().sort_values(ascending=False).index[0] if not filtered.empty else "No active domain"
    top_payer = filtered.groupby("Payer Group")["Case ID"].count().sort_values(ascending=False).index[0] if not filtered.empty else "No active payer"
    if brief_mode == "Executive readout":
        brief = f"""Enterprise Revenue Operations Brief\n\nActive command view:\n{len(filtered)} synthetic records\n{high_count} high risk records\n{sla_count} SLA pressure signals\nAverage aging: {avg_age} days\nSimulated exposure: ${exposure:,.0f}\n\nPrimary pressure domain:\n{top_domain}\n\nPrimary payer pressure group:\n{top_payer}\n\nOperational interpretation:\nWorkflow pressure is forming before downstream denial activity. Leadership should prioritize ownership clarity, documentation readiness, payer routing accuracy, and aged authorization follow up.\n\nCreated by Kori Pickle"""
    elif brief_mode == "Daily huddle":
        brief = f"""Daily Operations Huddle\n\nToday the team should review {len(filtered)} synthetic workflow records.\n\nFocus queue:\nHigh risk records: {high_count}\nSLA pressure records: {sla_count}\nAverage aging: {avg_age} days\n\nHuddle questions:\nWho owns each aged item?\nWhat documentation is missing?\nHas routing been validated?\nWhich payer follow ups need escalation today?\n\nCreated by Kori Pickle"""
    elif brief_mode == "Payer friction memo":
        brief = f"""Payer Friction Memo\n\nCurrent payer group requiring the most attention:\n{top_payer}\n\nOperational concern:\nPayer friction may be driven by routing ambiguity, unclear documentation readiness, aged authorization follow up, or unresolved eligibility conflicts.\n\nRecommended review:\nValidate payer owner, benefit manager pathway, portal route, authorization status, and documentation packet completeness before downstream denial risk increases.\n\nCreated by Kori Pickle"""
    else:
        brief = f"""Denial Prevention Note\n\nCurrent review population:\n{len(filtered)} synthetic records\n\nPrimary prevention target:\n{top_domain}\n\nAction logic:\nUse early operational visibility to identify records that may become avoidable denials if eligibility, routing, authorization aging, and documentation readiness are not stabilized before submission or final follow up.\n\nCreated by Kori Pickle"""
    st.text_area("Generated leadership brief", brief, height=390)
    st.download_button("Download leadership brief", data=brief, file_name="kori_pickle_leadership_brief.txt", mime="text/plain")

with tab_f:
    st.markdown('<div class="section-title">Responsible Use Governance</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="editorial-note"><h3>Synthetic Data Standard</h3><p>This public platform uses synthetic records only. It is designed for healthcare operations learning, portfolio demonstration, workflow intelligence, and responsible technology positioning. It does not use PHI and does not make payer, billing, coding, clinical, or patient specific decisions.</p></div>',
        unsafe_allow_html=True,
    )
    governance = pd.DataFrame(
        [
            ["Synthetic case identifiers", "Allowed"],
            ["Fake payer groups", "Allowed"],
            ["Simulated aging days", "Allowed"],
            ["Simulated documentation gaps", "Allowed"],
            ["Simulated exposure values", "Allowed"],
            ["Protected health information", "Not used"],
            ["Patient specific records", "Not used"],
            ["Clinical decision automation", "Not performed"],
            ["Payer decision automation", "Not performed"],
        ],
        columns=["Data Element", "Portfolio Status"],
    )
    st.dataframe(governance, hide_index=True, use_container_width=True)

st.markdown('<div class="footer-brand">', unsafe_allow_html=True)
if logo_bytes:
    st.image(BytesIO(logo_bytes), use_container_width=True)
st.markdown(
    """
<div class="kicker">Created by Kori Pickle</div>
<div class="footer-signature">Kori Pickle</div>
<p style="font-weight:400; line-height:1.7;">Healthcare Operations Intelligence • Revenue Cycle • Patient Access • Prior Authorization • Denial Prevention</p>
<a class="icon-link" href="https://www.linkedin.com/in/kori-pickle" target="_blank">LinkedIn</a>
<a class="icon-link" href="https://github.com/koripickle1101-TN" target="_blank">GitHub</a>
</div>
""",
    unsafe_allow_html=True,
)
