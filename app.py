import streamlit as st
import pandas as pd
from datetime import datetime

TENNESSEE_ORANGE = "rgb(255, 130, 0)"
BLACK = "rgb(0, 0, 0)"
WHITE = "rgb(255, 255, 255)"
SOFT_LINE = "rgb(232, 232, 232)"
INK = "rgb(24, 24, 24)"

st.set_page_config(
    page_title="Enterprise Revenue Operations Platform",
    page_icon="🟠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600;700;800&family=Great+Vibes&display=swap');

    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: rgb(255, 255, 255);
        color: rgb(0, 0, 0);
        font-family: Inter, sans-serif;
    }

    [data-testid="stSidebar"] {
        background: rgb(255, 255, 255);
        border-right: 1px solid rgb(232, 232, 232);
    }

    .block-container {
        padding-top: 2.2rem;
        padding-left: 5.5rem;
        padding-right: 5.5rem;
        max-width: 1500px;
    }

    h1, h2, h3 {
        font-family: "Playfair Display", Georgia, serif;
        color: rgb(0, 0, 0);
        letter-spacing: -0.045em;
    }

    .brand-kicker {
        font-size: 0.76rem;
        letter-spacing: 0.32em;
        text-transform: uppercase;
        font-weight: 800;
        color: rgb(0, 0, 0);
        margin-bottom: 0.85rem;
    }

    .orange-line {
        height: 3px;
        width: 180px;
        background: rgb(255, 130, 0);
        margin-top: 1.1rem;
        margin-bottom: 1.8rem;
    }

    .hero {
        border: 1px solid rgb(232, 232, 232);
        border-radius: 34px;
        padding: 3.3rem;
        background: linear-gradient(135deg, rgb(255, 255, 255) 0%, rgb(255, 249, 241) 100%);
        box-shadow: 0 24px 70px rgba(0,0,0,0.06);
        margin-bottom: 2.1rem;
    }

    .hero-title {
        font-family: "Playfair Display", Georgia, serif;
        font-size: clamp(3rem, 7vw, 6.4rem);
        line-height: 0.88;
        letter-spacing: -0.06em;
        font-weight: 800;
        margin: 0;
        color: rgb(0, 0, 0);
    }

    .hero-title .orange {
        color: rgb(255, 130, 0);
    }

    .hero-copy {
        max-width: 880px;
        font-size: 1.05rem;
        line-height: 1.75;
        margin-top: 1.4rem;
        color: rgb(24, 24, 24);
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        border: 1px solid rgb(255, 130, 0);
        border-radius: 999px;
        padding: 0.55rem 0.85rem;
        margin-right: 0.55rem;
        margin-top: 0.8rem;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: rgb(0, 0, 0);
        background: rgb(255, 251, 245);
    }

    .metric-card {
        border: 1px solid rgb(232, 232, 232);
        border-left: 5px solid rgb(255, 130, 0);
        border-radius: 24px;
        padding: 1.35rem;
        background: rgb(255, 255, 255);
        box-shadow: 0 14px 42px rgba(0,0,0,0.045);
        min-height: 145px;
    }

    .metric-label {
        font-size: 0.72rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        font-weight: 800;
        color: rgb(0, 0, 0);
        margin-bottom: 0.65rem;
    }

    .metric-value {
        font-family: "Playfair Display", Georgia, serif;
        font-size: 2.65rem;
        font-weight: 800;
        line-height: 1;
        color: rgb(255, 130, 0);
    }

    .metric-note {
        font-size: 0.82rem;
        color: rgb(72, 72, 72);
        margin-top: 0.8rem;
        line-height: 1.45;
    }

    .section-card {
        border: 1px solid rgb(232, 232, 232);
        border-radius: 28px;
        padding: 2rem;
        background: rgb(255, 255, 255);
        box-shadow: 0 18px 50px rgba(0,0,0,0.04);
        margin-top: 1.3rem;
        margin-bottom: 1.3rem;
    }

    .black-card {
        border-radius: 30px;
        padding: 2rem;
        background: rgb(0, 0, 0);
        color: rgb(255, 255, 255);
        border-left: 7px solid rgb(255, 130, 0);
        box-shadow: 0 24px 60px rgba(0,0,0,0.16);
        margin-top: 1.3rem;
        margin-bottom: 1.3rem;
    }

    .black-card h3 {
        color: rgb(255, 255, 255);
        font-family: "Playfair Display", Georgia, serif;
        font-size: 2.15rem;
        margin: 0 0 1rem 0;
    }

    .black-card p {
        color: rgb(242, 242, 242);
        line-height: 1.65;
        font-size: 0.98rem;
    }

    .node-row {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin-top: 1.25rem;
    }

    .node {
        border: 2px solid rgb(255, 130, 0);
        border-radius: 999px;
        padding: 1rem 1.15rem;
        min-width: 150px;
        text-align: center;
        font-weight: 800;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-size: 0.72rem;
        background: rgb(255, 255, 255);
        box-shadow: inset 0 0 0 8px rgb(255, 246, 235);
    }

    .signature {
        font-family: "Great Vibes", cursive;
        font-size: 3.2rem;
        color: rgb(0, 0, 0);
        line-height: 1;
        margin-top: 0.5rem;
    }

    .small-muted {
        color: rgb(78, 78, 78);
        font-size: 0.88rem;
        line-height: 1.55;
    }

    div[data-testid="stMetric"] {
        background: rgb(255, 255, 255);
        border: 1px solid rgb(232, 232, 232);
        border-left: 5px solid rgb(255, 130, 0);
        padding: 1rem;
        border-radius: 20px;
    }

    div[data-testid="stMetricValue"] {
        color: rgb(255, 130, 0);
        font-family: "Playfair Display", Georgia, serif;
        font-size: 2rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        border-bottom: 1px solid rgb(232, 232, 232);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 999px;
        padding: 0.65rem 1rem;
        background: rgb(255, 251, 245);
        border: 1px solid rgb(232, 232, 232);
        font-weight: 800;
        color: rgb(0, 0, 0);
    }

    [data-testid="stMainMenu"], footer {
        visibility: hidden;
    }

    @media (max-width: 900px) {
        .block-container {
            padding-left: 1.1rem;
            padding-right: 1.1rem;
        }
        .hero {
            padding: 2rem;
            border-radius: 26px;
        }
        .hero-title {
            font-size: 3.3rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def load_command_center_data():
    records = [
        ["AUTH-0001", "Commercial", "Patient Access", "Orthopedics", "Eligibility mismatch", 9, 12600, "High", "Missing subscriber relation", "Escalate eligibility verification"],
        ["AUTH-0002", "Medicare Advantage", "Prior Authorization", "Cardiology", "Authorization aging", 6, 28750, "High", "Pending clinical packet", "Request documentation packet"],
        ["AUTH-0003", "Medicaid", "Documentation Review", "Rehabilitation", "Incomplete plan of care", 4, 9300, "Moderate", "Therapy notes incomplete", "Validate documentation readiness"],
        ["AUTH-0004", "Commercial", "Prior Authorization", "Imaging", "Wrong portal route", 8, 14500, "High", "Benefit manager carve out", "Confirm routing owner"],
        ["AUTH-0005", "Marketplace", "Eligibility Verification", "Primary Care", "Coverage inactive", 3, 4200, "Moderate", "Coverage termination risk", "Recheck eligibility"],
        ["AUTH-0006", "Self Pay", "Patient Access", "Surgery", "Estimate not completed", 2, 6800, "Low", "Patient financial clearance", "Create estimate review"],
        ["AUTH-0007", "Commercial", "Denial Prevention", "Oncology", "Medical necessity risk", 7, 33100, "High", "Policy criteria unclear", "Route to human review"],
        ["AUTH-0008", "Medicare Advantage", "Prior Authorization", "Neurology", "SLA risk", 5, 18500, "Moderate", "Authorization pending 5 days", "Escalate payer follow up"],
        ["AUTH-0009", "Medicaid", "Documentation Review", "Behavioral Health", "Missing referral", 6, 7600, "Moderate", "Referral not attached", "Attach referral evidence"],
        ["AUTH-0010", "Commercial", "Eligibility Verification", "Cardiology", "COB conflict", 8, 22100, "High", "Coordination of benefits unresolved", "Validate primary payer"],
        ["AUTH-0011", "Marketplace", "Prior Authorization", "Imaging", "Payer policy mismatch", 7, 11900, "High", "Procedure requires delegated review", "Check benefit manager"],
        ["AUTH-0012", "Medicare Advantage", "Denial Prevention", "Rehabilitation", "Appeal exposure", 5, 15200, "Moderate", "Denial reason pattern detected", "Prepare prevention brief"],
    ]
    columns = [
        "case_id", "payer_group", "workflow_area", "service_line", "risk_signal",
        "aging_days", "synthetic_exposure", "risk_level", "root_cause", "next_action"
    ]
    return pd.DataFrame(records, columns=columns)

df = load_command_center_data()

risk_filter = st.sidebar.multiselect(
    "Filter by risk level",
    sorted(df["risk_level"].unique()),
    default=sorted(df["risk_level"].unique())
)

payer_filter = st.sidebar.multiselect(
    "Filter by payer group",
    sorted(df["payer_group"].unique()),
    default=sorted(df["payer_group"].unique())
)

area_filter = st.sidebar.multiselect(
    "Filter by workflow area",
    sorted(df["workflow_area"].unique()),
    default=sorted(df["workflow_area"].unique())
)

filtered = df[
    df["risk_level"].isin(risk_filter)
    & df["payer_group"].isin(payer_filter)
    & df["workflow_area"].isin(area_filter)
]

high_risk_count = int((filtered["risk_level"] == "High").sum())
moderate_risk_count = int((filtered["risk_level"] == "Moderate").sum())
sla_risk_count = int((filtered["aging_days"] >= 5).sum())
synthetic_exposure = int(filtered["synthetic_exposure"].sum()) if not filtered.empty else 0

st.markdown(
    """
    <div class="hero">
        <div class="brand-kicker">Kori Pickle • Healthcare Operations Intelligence</div>
        <h1 class="hero-title">Enterprise Revenue <span class="orange">Operations</span> Platform</h1>
        <div class="orange-line"></div>
        <p class="hero-copy">
            A premium synthetic no PHI healthcare operations command center for patient access,
            eligibility verification, prior authorization pressure tracking, documentation readiness,
            denial prevention, payer friction analysis, and responsible operational intelligence.
        </p>
        <span class="status-pill">No PHI</span>
        <span class="status-pill">Synthetic Data</span>
        <span class="status-pill">Human Review Required</span>
        <span class="status-pill">Built by Kori Pickle</span>
    </div>
    """,
    unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">High Risk Records</div><div class="metric-value">{high_risk_count}</div><div class="metric-note">Filtered operational review queue.</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">SLA Risk Signals</div><div class="metric-value">{sla_risk_count}</div><div class="metric-note">Records aging at or above five days.</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Synthetic Exposure</div><div class="metric-value">${synthetic_exposure:,.0f}</div><div class="metric-note">Portfolio simulation only.</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="metric-card"><div class="metric-label">Academic Standing</div><div class="metric-value">99 / 120</div><div class="metric-note">BSHA candidate • GPA 3.6.</div></div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Live Command Center",
    "Workflow Intelligence",
    "Payer Friction",
    "Leadership Brief",
    "Responsible Use"
])

with tab1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("## Live Command Center")
    st.write("Use the filters in the sidebar to simulate how leadership can isolate workflow pressure by risk level, payer group, and operational area.")
    st.dataframe(filtered, hide_index=True, use_container_width=True)

    c1, c2 = st.columns([5, 4])
    with c1:
        risk_summary = filtered.groupby("risk_level")["case_id"].count().reset_index(name="records")
        st.markdown("### Risk Queue Distribution")
        st.bar_chart(risk_summary.set_index("risk_level"))
    with c2:
        st.markdown(
            """
            <div class="black-card">
                <h3>Executive Interpretation</h3>
                <p>
                This command center is showing workflow review signals, not automated decisions.
                High risk records should be used to prioritize eligibility validation, documentation readiness,
                payer follow up, routing review, and safe escalation.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

with tab2:
    st.markdown("## Workflow Intelligence Model")
    st.markdown(
        """
        <div class="section-card">
            <div class="brand-kicker">Front End Revenue Cycle Control Map</div>
            <div class="node-row">
                <div class="node">Patient Access</div>
                <div class="node">Eligibility</div>
                <div class="node">Prior Auth</div>
                <div class="node">Documentation</div>
                <div class="node">Payer Follow Up</div>
                <div class="node">Denial Prevention</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    area_summary = filtered.groupby("workflow_area").agg(
        records=("case_id", "count"),
        exposure=("synthetic_exposure", "sum"),
        average_aging=("aging_days", "mean")
    ).reset_index()
    area_summary["average_aging"] = area_summary["average_aging"].round(1)
    st.dataframe(area_summary, hide_index=True, use_container_width=True)

    st.markdown("### Workflow Stabilization Calculator")
    volume = st.number_input("Monthly front end record volume", min_value=0, value=15000, step=500)
    friction = st.slider("Estimated workflow friction rate", min_value=0.01, max_value=0.25, value=0.08, step=0.01)
    capture = st.slider("Estimated stabilization capture rate", min_value=0.25, max_value=0.95, value=0.85, step=0.05)
    flagged = volume * friction
    stabilized = flagged * capture
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Projected Records Flagged", f"{int(flagged):,}")
    col_b.metric("Projected Records Stabilized", f"{int(stabilized):,}")
    col_c.metric("Residual Review Queue", f"{int(flagged - stabilized):,}")

with tab3:
    st.markdown("## Payer Friction Heatmap")
    payer_summary = filtered.groupby("payer_group").agg(
        records=("case_id", "count"),
        high_risk=("risk_level", lambda x: int((x == "High").sum())),
        exposure=("synthetic_exposure", "sum"),
        average_aging=("aging_days", "mean")
    ).reset_index()
    payer_summary["average_aging"] = payer_summary["average_aging"].round(1)
    payer_summary["friction_score"] = (
        payer_summary["high_risk"] * 25
        + payer_summary["records"] * 8
        + payer_summary["average_aging"] * 6
    ).round(0).astype(int)
    st.dataframe(payer_summary.sort_values("friction_score", ascending=False), hide_index=True, use_container_width=True)
    st.bar_chart(payer_summary.set_index("payer_group")["friction_score"])

    selected_payer = st.selectbox("Select payer group for operational interpretation", payer_summary["payer_group"].tolist() if not payer_summary.empty else ["No data"])
    if selected_payer != "No data":
        payer_rows = filtered[filtered["payer_group"] == selected_payer]
        st.markdown(
            f"""
            <div class="section-card">
                <h3>{selected_payer} Operational Readout</h3>
                <p class="small-muted">
                This payer group currently shows {len(payer_rows)} synthetic review records and
                ${int(payer_rows["synthetic_exposure"].sum()):,} in simulated exposure.
                Recommended review focus: validate routing ownership, confirm documentation readiness,
                and prioritize aged authorization records before downstream denial activity develops.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

with tab4:
    st.markdown("## Leadership Brief Generator")
    brief_type = st.selectbox(
        "Select brief type",
        ["Executive leadership brief", "Daily huddle script", "Denial prevention action plan"]
    )

    if brief_type == "Executive leadership brief":
        brief = f"""Enterprise Revenue Operations Brief

Current synthetic command center review shows {high_risk_count} high risk records, {moderate_risk_count} moderate risk records, {sla_risk_count} SLA risk signals, and ${synthetic_exposure:,.0f} in simulated financial exposure.

Primary operational concern:
Workflow pressure is forming before final denial activity. The highest concern areas are payer routing, prior authorization aging, documentation readiness, and eligibility verification instability.

Recommended leadership actions:
1. Prioritize high risk authorization and eligibility records for human review.
2. Validate payer routing and delegated benefit manager ownership before submission.
3. Review documentation packets before payer follow up.
4. Track aged authorization requests by payer group and service line.
5. Maintain responsible use boundaries. This system supports prioritization only and does not make clinical, payer, billing, coding, or patient specific decisions.

Created by Kori Pickle"""
    elif brief_type == "Daily huddle script":
        brief = f"""Daily Operations Huddle Script

Today we are reviewing {len(filtered)} synthetic workflow records across patient access, eligibility, prior authorization, documentation review, and denial prevention.

Focus areas:
High risk queue: {high_risk_count}
SLA risk queue: {sla_risk_count}
Simulated exposure: ${synthetic_exposure:,.0f}

Huddle questions:
1. Which records are aging before payer response?
2. Which requests may be routed to the wrong payer, portal, or delegated entity?
3. Which documentation packets are incomplete before submission?
4. Which records require escalation but not automated decision making?
5. What can be stabilized today before the issue becomes rework, delay, denial, or patient frustration?

Created by Kori Pickle"""
    else:
        brief = f"""Denial Prevention Action Plan

Objective:
Use early workflow visibility to identify operational risk before downstream denial activity develops.

Review priorities:
1. Eligibility mismatch records
2. Prior authorization aging
3. Missing documentation packets
4. Payer routing uncertainty
5. Coordination of benefits conflict
6. Medical necessity review readiness
7. Appeal exposure patterns

Operating principle:
The question is not only whether the task was completed. The question is where the workflow first lost control.

Responsible boundary:
All outputs are synthetic no PHI workflow review signals. Human validation is required.

Created by Kori Pickle"""

    st.text_area("Generated leadership output", brief, height=420)
    st.download_button(
        "Download leadership brief",
        data=brief,
        file_name="kori_pickle_enterprise_rev_ops_brief.txt",
        mime="text/plain"
    )

with tab5:
    st.markdown(
        """
        <div class="black-card">
            <h3>Responsible Use Boundary</h3>
            <p>
            This platform uses synthetic no PHI data only. It does not make clinical decisions,
            payer decisions, coding decisions, billing determinations, medical necessity determinations,
            or patient specific recommendations.
            </p>
            <p>
            All flagged records are workflow review signals for prioritization, documentation validation,
            payer follow up, escalation awareness, and healthcare operations learning.
            Human review is required.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## Professional Ledger")
    ledger = pd.DataFrame([
        ["Architect", "Kori Pickle"],
        ["Academic Track", "University of Phoenix BSHA Candidate"],
        ["Credits Completed", "99 of 120"],
        ["GPA", "3.6"],
        ["Portfolio Focus", "Healthcare Operations, Revenue Cycle, Patient Access, Prior Authorization, Denial Prevention, Health Informatics"],
        ["Data Standard", "Synthetic no PHI data only"],
    ], columns=["Category", "Value"])
    st.dataframe(ledger, hide_index=True, use_container_width=True)

st.markdown(
    """
    <div class="section-card" style="text-align:center;">
        <div class="brand-kicker">Created by</div>
        <div class="signature">Kori Pickle</div>
        <p class="small-muted">Healthcare Operations Intelligence • Revenue Cycle • Patient Access • Prior Authorization • Denial Prevention</p>
    </div>
    """,
    unsafe_allow_html=True
)
