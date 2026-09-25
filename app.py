"""
Cortex — Streamlit UI for the Multi-Agent Research Pipeline.

Place this file inside Multi_Agent_System/ (next to pipeline.py, agents.py,
tools.py, .env) and run:

    streamlit run app.py
"""

import streamlit as st
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

st.set_page_config(
    page_title="Cortex — Multi-Agent Research",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

    .stApp {
        background: #0a0a12;
        background-image:
            radial-gradient(circle at 15% 10%, rgba(124,58,237,0.18) 0%, transparent 45%),
            radial-gradient(circle at 85% 0%, rgba(6,182,212,0.14) 0%, transparent 40%),
            radial-gradient(circle at 50% 100%, rgba(124,58,237,0.10) 0%, transparent 50%);
        color: #e7e7ee;
    }
    #MainMenu, header, footer { visibility: hidden; }
    .block-container { padding-top: 2.2rem; max-width: 1150px; }

    /* ---- Top bar ---- */
    .topbar { display:flex; justify-content:space-between; align-items:center; margin-bottom: 2.6rem; }
    .brand { font-weight:700; font-size:1.05rem; letter-spacing:0.02em; }
    .brand .dot { color:#a78bfa; }
    .topbar-pills { display:flex; gap:0.5rem; }
    .pill {
        font-family:'JetBrains Mono', monospace; font-size:0.68rem; letter-spacing:0.08em;
        color:#9d9daa; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
        padding:0.3rem 0.7rem; border-radius:999px;
    }

    /* ---- Hero ---- */
    .kicker {
        font-family:'JetBrains Mono', monospace; font-size:0.72rem; letter-spacing:0.25em;
        background: linear-gradient(90deg,#a78bfa,#22d3ee);
        -webkit-background-clip:text; background-clip:text; color:transparent;
        font-weight:600; margin-bottom:0.7rem;
    }
    .hero-title { font-size:3.1rem; font-weight:700; line-height:1.12; margin:0 0 1rem 0; max-width:640px; }
    .hero-title .grad {
        background: linear-gradient(90deg,#c4b5fd,#67e8f9);
        -webkit-background-clip:text; background-clip:text; color:transparent;
    }
    .hero-sub { color:#9d9daa; font-size:1rem; line-height:1.6; max-width:480px; margin-bottom:1.8rem; }

    /* ---- Glass card / input ---- */
    .glass {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 16px;
        backdrop-filter: blur(12px);
    }
    div[data-testid="stTextInput"] input {
        background-color: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 12px !important;
        color: #eee !important;
        padding: 0.8rem 1rem !important;
        font-size: 0.95rem !important;
    }
    div[data-testid="stTextInput"] input::placeholder { color: #6b6b78 !important; }

    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(90deg, #7c3aed, #06b6d4) !important;
        border: none !important;
        border-radius: 12px !important;
        color: #fff !important;
        font-weight: 600 !important;
        padding: 0.8rem 1.3rem !important;
        box-shadow: 0 10px 30px rgba(124,58,237,0.28);
    }

    .stat-row { display:flex; gap:1.6rem; margin-top:0.3rem; }
    .stat { font-family:'JetBrains Mono', monospace; font-size:0.75rem; color:#8a8a96; }
    .stat b { color:#c9c9d4; }

    /* ---- decorative orb column ---- */
    .orb-wrap { position:relative; height: 260px; }
    .orb {
        position:absolute; border-radius:50%; filter: blur(2px);
        opacity:0.9; display:flex; align-items:center; justify-content:center;
        font-family:'JetBrains Mono', monospace; font-size:0.65rem; letter-spacing:0.1em;
        color:#0a0a12; font-weight:700;
    }
    .orb1 { width:120px; height:120px; top:10px; right:70px; background:linear-gradient(135deg,#a78bfa,#7c3aed); }
    .orb2 { width:78px; height:78px; top:120px; right:190px; background:linear-gradient(135deg,#67e8f9,#06b6d4); opacity:0.85;}
    .orb3 { width:56px; height:56px; top:170px; right:40px; background:linear-gradient(135deg,#f0abfc,#a78bfa); opacity:0.75;}

    /* ---- Timeline ---- */
    .timeline-wrap { margin: 1.2rem 0 1.6rem 0; padding: 1.6rem 1.8rem; }
    .timeline-row { display:flex; align-items:flex-start; }
    .tl-node-col { display:flex; flex-direction:column; align-items:center; flex:1; position:relative; }
    .tl-line {
        position:absolute; top:17px; left:50%; width:100%; height:2px;
        background: rgba(255,255,255,0.10); z-index:0;
    }
    .tl-node-col:last-child .tl-line { display:none; }
    .tl-dot {
        width:34px; height:34px; border-radius:50%; z-index:1;
        display:flex; align-items:center; justify-content:center;
        font-family:'JetBrains Mono', monospace; font-size:0.72rem; font-weight:700;
        border: 2px solid rgba(255,255,255,0.14); background:#14141c; color:#6b6b78;
    }
    .tl-dot.running {
        border-color:#a78bfa; color:#fff;
        background: linear-gradient(135deg,#7c3aed,#a78bfa);
        box-shadow: 0 0 0 6px rgba(124,58,237,0.15);
        animation: pulse 1.4s ease-in-out infinite;
    }
    .tl-dot.done { border-color:#22d3ee; color:#0a0a12; background: linear-gradient(135deg,#67e8f9,#22d3ee); }
    @keyframes pulse {
        0%   { box-shadow: 0 0 0 4px rgba(124,58,237,0.16); }
        50%  { box-shadow: 0 0 0 10px rgba(124,58,237,0.06); }
        100% { box-shadow: 0 0 0 4px rgba(124,58,237,0.16); }
    }
    .tl-label { margin-top:0.6rem; font-size:0.82rem; font-weight:600; text-align:center; }
    .tl-status {
        font-family:'JetBrains Mono', monospace; font-size:0.62rem; letter-spacing:0.1em;
        margin-top:0.15rem; color:#6b6b78;
    }
    .tl-status.running { color:#c4b5fd; }
    .tl-status.done { color:#67e8f9; }

    /* ---- Terminal log ---- */
    .term {
        font-family:'JetBrains Mono', monospace; font-size:0.8rem; line-height:1.75;
        padding: 1.1rem 1.3rem; max-height: 260px; overflow-y:auto;
        color:#a5f3c4;
    }
    .term .line-dim { color:#6b6b78; }
    .term .line-tag { color:#a78bfa; }

    .section-label {
        font-family:'JetBrains Mono', monospace; font-size:0.7rem; letter-spacing:0.2em;
        color:#7a7a86; margin: 2rem 0 0.6rem 0;
    }

    .footer-note {
        text-align:center; color:#4a4a55; font-family:'JetBrains Mono', monospace;
        font-size:0.7rem; margin-top:2.6rem; letter-spacing:0.05em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Top bar
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="topbar">
        <div class="brand">◆ CORTEX<span class="dot">.</span></div>
        <div class="topbar-pills">
            <div class="pill">LANGCHAIN</div>
            <div class="pill">4 AGENTS</div>
            <div class="pill">● LIVE</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""
if "state" not in st.session_state:
    st.session_state.state = None
if "step_status" not in st.session_state:
    st.session_state.step_status = ["idle", "idle", "idle", "idle"]
if "log_lines" not in st.session_state:
    st.session_state.log_lines = []

STEPS = ["Search", "Read", "Write", "Critique"]
SUGGESTIONS = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]

# ---------------------------------------------------------------------------
# Hero row: form (left) + decorative orbs (right)
# ---------------------------------------------------------------------------
hero_left, hero_right = st.columns([1.3, 1], gap="large")

with hero_left:
    st.markdown('<div class="kicker">MULTI-AGENT RESEARCH ENGINE</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-title">Ask a question.<br><span class="grad">Four agents</span> chase the answer.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hero-sub">Search, read, write and critique run in sequence — each one handing '
        'its work to the next — until a reviewed report lands in front of you.</div>',
        unsafe_allow_html=True,
    )

    with st.form("topic_form", clear_on_submit=False):
        topic = st.text_input(
            "Research topic",
            value=st.session_state.topic_input,
            placeholder="What do you want researched?",
            label_visibility="collapsed",
        )
        run_clicked = st.form_submit_button("Run pipeline →")

    chip_row = st.columns(len(SUGGESTIONS) + 1)
    chip_row[0].markdown(
        '<div style="font-family:JetBrains Mono, monospace; font-size:0.72rem; color:#6b6b78; '
        'padding-top:0.45rem;">TRY</div>',
        unsafe_allow_html=True,
    )
    for i, s in enumerate(SUGGESTIONS):
        if chip_row[i + 1].button(s, key=f"chip_{i}"):
            st.session_state.topic_input = s
            st.rerun()

with hero_right:
    st.markdown(
        """
        <div class="orb-wrap">
            <div class="orb orb1">SEARCH</div>
            <div class="orb orb2">WRITE</div>
            <div class="orb orb3">READ</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Timeline
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">PIPELINE STATUS</div>', unsafe_allow_html=True)
timeline_ph = st.empty()

def render_timeline():
    labels = {"idle": "WAITING", "running": "RUNNING", "done": "DONE"}
    nodes_html = ""
    for i, name in enumerate(STEPS):
        status = st.session_state.step_status[i]
        cls = "" if status == "idle" else status
        dot_content = "✓" if status == "done" else f"0{i+1}"
        nodes_html += (
            f'<div class="tl-node-col">'
            f'<div class="tl-line"></div>'
            f'<div class="tl-dot {cls}">{dot_content}</div>'
            f'<div class="tl-label">{name}</div>'
            f'<div class="tl-status {cls}">{labels[status]}</div>'
            f'</div>'
        )
    timeline_ph.markdown(
        f'<div class="glass timeline-wrap"><div class="timeline-row">{nodes_html}</div></div>',
        unsafe_allow_html=True,
    )

render_timeline()

# ---------------------------------------------------------------------------
# Terminal log
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">AGENT LOG</div>', unsafe_allow_html=True)
log_ph = st.empty()

def render_log():
    if not st.session_state.log_lines:
        body = '<span class="line-dim">$ waiting for a topic...</span>'
    else:
        body = "<br>".join(st.session_state.log_lines)
    log_ph.markdown(f'<div class="glass term">{body}</div>', unsafe_allow_html=True)

def log(msg, dim=False):
    cls = "line-dim" if dim else ""
    st.session_state.log_lines.append(f'<span class="{cls}">{msg}</span>')
    render_log()

render_log()

st.markdown(
    '<div class="footer-note">CORTEX · SEARCH → READ → WRITE → CRITIQUE · BUILT WITH STREAMLIT</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Run pipeline with live timeline + log updates
# ---------------------------------------------------------------------------
if run_clicked:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        st.session_state.topic_input = topic
        st.session_state.log_lines = []
        state = {}

        try:
            log(f"$ topic: <span class='line-tag'>{topic}</span>")

            # Step 1 — Search
            st.session_state.step_status = ["running", "idle", "idle", "idle"]
            render_timeline()
            log("[01] search agent — gathering sources...", dim=True)
            search_agent = build_search_agent()
            search_result = search_agent.invoke(
                {"messages": [("user", f"find recent,reliable and detailed information about :{topic}")]}
            )
            state["search_results"] = search_result["messages"][-1].content
            st.session_state.step_status[0] = "done"
            render_timeline()
            log("[01] search agent — done ✓")

            # Step 2 — Reader
            st.session_state.step_status[1] = "running"
            render_timeline()
            log("[02] reader agent — scraping top result...", dim=True)
            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            f"""
You are a web research reader.

Topic: {topic}

Below are the search results from Tavily.

{state['search_results']}

Your task:
1. Identify the most relevant result.
2. Extract its complete URL.
3. Call the scrape_url tool using that URL.
4. Return the scraped content.

Do NOT ask the user for a URL.
You must extract the URL from the search results and use the scrape_url tool.
""",
                        )
                    ]
                }
            )
            state["scraped_content"] = reader_result["messages"][-1].content
            st.session_state.step_status[1] = "done"
            render_timeline()
            log("[02] reader agent — done ✓")

            # Step 3 — Writer
            st.session_state.step_status[2] = "running"
            render_timeline()
            log("[03] writer chain — drafting report...", dim=True)
            research_combined = (
                f"SEARCH RESULTS : \n {state['search_results']}"
                f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
            )
            state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})
            st.session_state.step_status[2] = "done"
            render_timeline()
            log("[03] writer chain — done ✓")

            # Step 4 — Critic
            st.session_state.step_status[3] = "running"
            render_timeline()
            log("[04] critic chain — reviewing report...", dim=True)
            state["Critic"] = critic_chain.invoke({"report": state["report"]})
            st.session_state.step_status[3] = "done"
            render_timeline()
            log("[04] critic chain — done ✓")
            log("$ pipeline complete")

            st.session_state.state = state

        except Exception as e:
            log(f"<span style='color:#f87171'>! error: {e}</span>")
            st.error(f"Pipeline failed: {e}")

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
if st.session_state.state:
    state = st.session_state.state
    st.markdown("<br>", unsafe_allow_html=True)
    tab_report, tab_critic, tab_search, tab_scraped = st.tabs(
        ["📄 Final Report", "🧐 Critic Review", "🔍 Search Results", "📑 Scraped Content"]
    )

    with tab_report:
        report_text = state.get("report", "")
        st.markdown(report_text if isinstance(report_text, str) else str(report_text))
        st.download_button(
            "Download report as .md",
            data=report_text if isinstance(report_text, str) else str(report_text),
            file_name="report.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with tab_critic:
        critic_text = state.get("Critic", "")
        st.markdown(critic_text if isinstance(critic_text, str) else str(critic_text))

    with tab_search:
        st.text(state.get("search_results", ""))

    with tab_scraped:
        st.text(state.get("scraped_content", ""))
