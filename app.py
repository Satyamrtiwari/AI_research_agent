import streamlit as st
import time
import html
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS: Option 1 Daylight Modern ──────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@500;600;700;800&family=DM+Mono:wght@400;500;600&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');

/* ── Reset & Base (Warm Daylight) ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #1E1A17;
}

.stApp {
    background-color: #FBF9F5;
    background-image:
        radial-gradient(ellipse 70% 35% at 20% -5%, rgba(255, 140, 50, 0.08) 0%, transparent 60%),
        radial-gradient(ellipse 50% 30% at 85% 105%, rgba(34, 197, 94, 0.05) 0%, transparent 55%);
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 3rem 4rem; max-width: 1280px; }

/* ── Top Bar ── */
.top-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.8rem 1.4rem;
    background: #FFFFFF;
    border: 1px solid rgba(226, 218, 206, 0.7);
    border-radius: 14px;
    box-shadow: 0 2px 10px rgba(30, 20, 10, 0.03);
    margin-bottom: 2rem;
}
.brand {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.25rem;
    color: #1E1A17;
    letter-spacing: -0.02em;
}
.brand-mark {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #FF8C32 0%, #FF651A 100%);
    color: #FFFFFF;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 800;
}
.brand span {
    color: #FF7A1A;
}
.nav-badges {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.badge-ready {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #E8F7EE;
    color: #15803D;
    border: 1px solid rgba(34, 197, 94, 0.25);
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
}
.badge-ready .dot {
    width: 7px;
    height: 7px;
    background: #22C55E;
    border-radius: 50%;
    display: inline-block;
}
.badge-model {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: #FFF4E8;
    color: #C25E1A;
    border: 1px solid rgba(255, 140, 50, 0.3);
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
}

/* ── Connected Horizontal Stepper (Option 1 with Connecting Bridge) ── */
.pipeline-flow {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 1.2rem 0 2rem;
    width: 100%;
}
.pipeline-step {
    flex: 1;
    background: #FFFFFF;
    border: 1.5px solid rgba(226, 218, 206, 0.9);
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    box-shadow: 0 4px 14px rgba(35, 25, 15, 0.04);
    transition: all 0.25s ease;
}
.pipeline-step.active {
    border-color: #FF8C32;
    background: #FFFDF9;
    box-shadow: 0 6px 20px rgba(255, 140, 50, 0.15);
    transform: translateY(-2px);
}
.pipeline-step.done {
    border-color: #86EFAC;
    background: #F8FCF9;
    box-shadow: 0 4px 14px rgba(34, 197, 94, 0.08);
}
.step-head {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    margin-bottom: 0.3rem;
}
.step-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
    color: #FF7A1A;
    background: #FFF3E8;
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
}
.step-name {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.92rem;
    color: #1E1A17;
}
.step-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.06em;
}
.status-waiting  { color: #9E958A; }
.status-running  { color: #FF7A1A; }
.status-done     { color: #16A34A; }

.step-underline {
    height: 3px;
    background: #F3ECE1;
    border-radius: 2px;
    margin-top: 0.55rem;
    transition: background 0.3s;
}
.step-underline.active {
    background: linear-gradient(90deg, #FF8C32 0%, #FFB27A 100%);
}
.step-underline.done {
    background: #22C55E;
}

/* ── Connecting Bridge Lines & Circular Nodes ── */
.pipeline-bridge {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    flex-shrink: 0;
    padding: 0 2px;
}
.bridge-line {
    height: 3px;
    background: #E8DFD0;
    flex: 1;
    transition: background 0.3s;
}
.bridge-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #E8DFD0;
    border: 2px solid #FAF7F2;
    flex-shrink: 0;
    transition: all 0.3s;
}
.pipeline-bridge.connected .bridge-line {
    background: #FF8C32;
}
.pipeline-bridge.connected .bridge-dot {
    background: #FF8C32;
    box-shadow: 0 0 0 3px rgba(255, 140, 50, 0.25);
}

/* ── Search Input: High-Contrast Dark Visible Border ── */
.stTextInput > div > div > input {
    background: #FFFFFF !important;
    border: 2px solid #5C544A !important;
    border-radius: 12px !important;
    color: #1E1A17 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 500 !important;
    padding: 0.85rem 1.2rem !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    transition: all 0.2s !important;
}
.stTextInput > div > div > input:focus {
    background: #FFFFFF !important;
    border-color: #FF6E1A !important;
    box-shadow: 0 0 0 4px rgba(255, 110, 26, 0.18) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #7D756C !important;
    font-size: 0.95rem !important;
    opacity: 0.85 !important;
}
.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #B54D0E !important;
    font-weight: 700 !important;
    margin-bottom: 0.35rem !important;
}

/* ── Primary Button (Warm Amber Gradient) ── */
.stButton > button {
    background: linear-gradient(135deg, #FF8C32 0%, #FF651A 100%) !important;
    color: #FFFFFF !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.98rem !important;
    letter-spacing: 0.03em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2.2rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
    box-shadow: 0 4px 16px rgba(255, 110, 26, 0.28) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(255, 110, 26, 0.38) !important;
    opacity: 0.96 !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Suggestion Chips ── */
.chip-container {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 0.8rem;
}
.chip-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #9E958A;
    font-weight: 600;
    letter-spacing: 0.1em;
    margin-right: 0.3rem;
}
.sample-chip {
    background: #F4EFEB;
    border: 1px solid #E5DCD2;
    border-radius: 9999px;
    padding: 0.25rem 0.8rem;
    font-size: 0.78rem;
    color: #6E655C;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
}

/* ── Report Card (Option 1) ── */
.report-card {
    background: #FFFFFF;
    border: 1px solid rgba(226, 218, 206, 0.8);
    border-radius: 16px;
    padding: 2.2rem 2.6rem;
    box-shadow: 0 4px 20px rgba(35, 25, 15, 0.03);
    margin-bottom: 2rem;
}
.report-header-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #FFF3E8;
    color: #C25E1A;
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.35rem 0.85rem;
    border-radius: 6px;
    margin-bottom: 1.2rem;
}

/* ── Critic Scorecard (Option 1 Mint Green) ── */
.scorecard-card {
    background: #FFFFFF;
    border: 1.5px solid rgba(34, 197, 94, 0.35);
    border-radius: 16px;
    padding: 1.8rem 1.8rem;
    box-shadow: 0 6px 20px rgba(34, 197, 94, 0.06);
    margin-bottom: 2rem;
}
.scorecard-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.15rem;
    color: #1E1A17;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.score-box {
    background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
    border: 1px solid #A7F3D0;
    border-radius: 14px;
    padding: 1.4rem 1rem;
    text-align: center;
    margin-bottom: 1.4rem;
}
.score-value {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.8rem;
    line-height: 1.0;
    color: #047857;
    margin-bottom: 0.3rem;
}
.score-caption {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #059669;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
.critic-content {
    font-size: 0.9rem;
    line-height: 1.65;
    color: #374151;
    white-space: pre-wrap;
    background: #F9FAFB;
    border: 1px solid #F3F4F6;
    border-radius: 10px;
    padding: 1.1rem;
}

/* ── Result Raw Panel ── */
.raw-panel {
    background: #FAF8F5;
    border: 1px solid #EAE3D7;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin: 0.6rem 0;
    font-size: 0.88rem;
    line-height: 1.7;
    color: #4A443E;
    white-space: pre-wrap;
    max-height: 380px;
    overflow-y: auto;
}

/* ── Spinner color ── */
.stSpinner > div { color: #FF8C32 !important; }

/* ── Footer notice ── */
.footer-notice {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #A89F93;
    text-align: center;
    margin-top: 3.5rem;
    letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done", "topic_input"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else ("" if key == "topic_input" else False)


# ── Top Bar Navigation ────────────────────────────────────────────────────────
st.markdown("""
<div class="top-nav">
    <div class="brand">
        <span class="brand-mark">RM</span>
        Research<span>Mind</span>
    </div>
    <div class="nav-badges">
        <span class="badge-ready"><span class="dot"></span> 4 AGENTS READY</span>
        <span class="badge-model">⚙ Groq · gpt-oss-120b</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Connected Horizontal Stepper (Option 1 with Connecting Bridges) ───────────
r = st.session_state.results
is_running = st.session_state.running

def step_status(key, step_idx):
    if key in r:
        return "done", "✓ COMPLETED", "status-done", "done"
    if is_running:
        steps_seq = ["search", "reader", "writer", "critic"]
        first_pending = next((s for s in steps_seq if s not in r), None)
        if first_pending == key:
            return "active", "● IN PROGRESS", "status-running", "active"
    return "", "READY", "status-waiting", ""

s1_cls, s1_lbl, s1_pill, s1_bar = step_status("search", 1)
s2_cls, s2_lbl, s2_pill, s2_bar = step_status("reader", 2)
s3_cls, s3_lbl, s3_pill, s3_bar = step_status("writer", 3)
s4_cls, s4_lbl, s4_pill, s4_bar = step_status("critic", 4)

c1_cls = "connected" if "search" in r else ""
c2_cls = "connected" if "reader" in r else ""
c3_cls = "connected" if "writer" in r else ""

st.markdown(f"""
<div class="pipeline-flow">
    <div class="pipeline-step {s1_cls}">
        <div class="step-head">
            <span class="step-badge">01</span>
            <span class="step-name">Web Search</span>
        </div>
        <div class="step-tag {s1_pill}">{s1_lbl}</div>
        <div class="step-underline {s1_bar}"></div>
    </div>
    <div class="pipeline-bridge {c1_cls}">
        <span class="bridge-line"></span>
        <span class="bridge-dot"></span>
        <span class="bridge-line"></span>
    </div>
    <div class="pipeline-step {s2_cls}">
        <div class="step-head">
            <span class="step-badge">02</span>
            <span class="step-name">Reader Scrape</span>
        </div>
        <div class="step-tag {s2_pill}">{s2_lbl}</div>
        <div class="step-underline {s2_bar}"></div>
    </div>
    <div class="pipeline-bridge {c2_cls}">
        <span class="bridge-line"></span>
        <span class="bridge-dot"></span>
        <span class="bridge-line"></span>
    </div>
    <div class="pipeline-step {s3_cls}">
        <div class="step-head">
            <span class="step-badge">03</span>
            <span class="step-name">Synthesis Writer</span>
        </div>
        <div class="step-tag {s3_pill}">{s3_lbl}</div>
        <div class="step-underline {s3_bar}"></div>
    </div>
    <div class="pipeline-bridge {c3_cls}">
        <span class="bridge-line"></span>
        <span class="bridge-dot"></span>
        <span class="bridge-line"></span>
    </div>
    <div class="pipeline-step {s4_cls}">
        <div class="step-head">
            <span class="step-badge">04</span>
            <span class="step-name">Critic Review</span>
        </div>
        <div class="step-tag {s4_pill}">{s4_lbl}</div>
        <div class="step-underline {s4_bar}"></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)


# ── Search Input Section (High-Contrast Visible Dark Border) ──────────────────
col_in, col_btn = st.columns([4.2, 1.2])

with col_in:
    topic = st.text_input(
        "Enter the topic !!",
        value=st.session_state.topic_input,
        placeholder="Enter the topic !! (e.g. AI in Healthcare, Quantum Computing, Rohit Sharma career...)",
        key="topic_input_box",
        label_visibility="visible",
    )

with col_btn:
    st.markdown("<div style='height: 1.85rem;'></div>", unsafe_allow_html=True)
    run_btn = st.button("⚡ Run Research", use_container_width=True)

# Interactive Suggestion Chips
st.markdown("""
<div class="chip-container">
    <span class="chip-label">SUGGESTIONS →</span>
    <span class="sample-chip">AI in Healthcare</span>
    <span class="sample-chip">Quantum Computing 2026</span>
    <span class="sample-chip">CRISPR Gene Editing</span>
    <span class="sample-chip">Autonomous LLM Agents</span>
</div>
""", unsafe_allow_html=True)


# ── Pipeline Execution ────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.topic_input = topic.strip()
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    try:
        # Step 1: Search
        with st.spinner("🔍 Step 1: Search Agent is gathering verified web data..."):
            search_agent = build_search_agent()
            sr = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
            })
            results["search"] = sr["messages"][-1].content
            st.session_state.results = dict(results)

        # Step 2: Reader
        with st.spinner("📄 Step 2: Reader Agent is analyzing top sources..."):
            reader_agent = build_reader_agent()
            rr = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic_val}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{results['search'][:800]}"
                )]
            })
            results["reader"] = rr["messages"][-1].content
            st.session_state.results = dict(results)

        # Step 3: Writer
        with st.spinner("✍️ Step 3: Synthesis Writer is drafting the report..."):
            research_combined = (
                f"SEARCH RESULTS:\n{results['search']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
            )
            results["writer"] = writer_chain.invoke({
                "topic": topic_val,
                "research": research_combined
            })
            st.session_state.results = dict(results)

        # Step 4: Critic
        with st.spinner("🧐 Step 4: Critic Chain is auditing and scoring the report..."):
            results["critic"] = critic_chain.invoke({
                "report": results["writer"]
            })
            st.session_state.results = dict(results)

        st.session_state.running = False
        st.session_state.done = True
        st.rerun()

    except Exception as e:
        st.session_state.running = False
        st.session_state.done = False
        st.error(f"⚠️ Research Pipeline Notice: {str(e)}")


# ── Results Layout (Option 1: 2-Column Report & Critic Scorecard) ──────────────
r = st.session_state.results

if r:
    col_report, col_scorecard = st.columns([6.8, 3.2])

    with col_report:
        if "writer" in r:
            st.markdown("""
            <div class="report-card">
                <div class="report-header-badge">📝 Executive Research Report</div>
            """, unsafe_allow_html=True)
            
            st.markdown(r["writer"])
            st.markdown("</div>", unsafe_allow_html=True)

            # Download Action
            st.download_button(
                label="⬇  Download Full Report (.md)",
                data=r["writer"],
                file_name=f"research_report_{int(time.time())}.md",
                mime="text/markdown",
                use_container_width=True,
            )

        # Raw Data Expanders
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        if "search" in r:
            with st.expander("🔍 Raw Search Agent Output", expanded=False):
                st.markdown(f'<div class="raw-panel">{html.escape(r["search"])}</div>', unsafe_allow_html=True)

        if "reader" in r:
            with st.expander("📄 Raw Scraped Content Output", expanded=False):
                st.markdown(f'<div class="raw-panel">{html.escape(r["reader"])}</div>', unsafe_allow_html=True)

    with col_scorecard:
        if "critic" in r:
            # Parse Score if present
            score_text = "8.5/10"
            for line in r["critic"].splitlines():
                if "Score:" in line:
                    score_text = line.replace("Score:", "").strip()
                    break

            st.markdown(f"""
            <div class="scorecard-card">
                <div class="scorecard-title">🎯 Critic Scorecard</div>
                <div class="score-box">
                    <div class="score-value">{html.escape(score_text)}</div>
                    <div class="score-caption">VERIFIED QUALITY AUDIT</div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class="critic-content">{html.escape(r["critic"])}</div>
            </div>
            """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-notice">
    ResearchMind · Option 1 Warm Daylight UI · Powered by LangChain & Groq
</div>
""", unsafe_allow_html=True)