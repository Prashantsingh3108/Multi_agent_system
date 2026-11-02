import streamlit as st
from datetime import datetime
from pipline import run_research_pipeline

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="ResearchAI | Multi-Agent Research",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# CUSTOM STYLING
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background:
      radial-gradient(circle at 85% 0%, rgba(72, 90, 190, .16), transparent 28%),
      #0b1020;
    color: #edf1ff;
}
[data-testid="stSidebar"] {
    background: #10182b;
    border-right: 1px solid rgba(160,180,255,.12);
}
[data-testid="stSidebar"] * { color: #e7ebff; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1450px; }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; color: #f4f6ff; }
.hero {
    padding: 30px 34px;
    border: 1px solid rgba(150,170,255,.20);
    border-radius: 22px;
    background: linear-gradient(120deg, rgba(39,55,105,.88), rgba(25,34,65,.78));
    box-shadow: 0 18px 55px rgba(0,0,0,.22);
    margin-bottom: 24px;
}
.eyebrow {
    color: #9eafff; font-size: .76rem; font-weight: 700;
    letter-spacing: .16em; text-transform: uppercase;
}
.hero-title { font-family: 'Space Grotesk',sans-serif; font-size: 2.45rem; font-weight: 700; margin: 8px 0; }
.hero-sub { color: #c1cbea; font-size: 1rem; max-width: 760px; }
.agent-card {
    background: linear-gradient(145deg, #151f37, #111a2e);
    border: 1px solid rgba(150,170,255,.15);
    border-radius: 16px; padding: 18px; min-height: 142px;
}
.agent-icon { font-size: 1.55rem; }
.agent-name { font-weight: 700; font-size: 1rem; margin-top: 9px; color: #f2f4ff; }
.agent-desc { color: #9eaccd; font-size: .83rem; margin-top: 5px; }
.section-label {
    color: #9eafff; font-size: .75rem; font-weight: 700;
    letter-spacing: .14em; text-transform: uppercase; margin-bottom: 8px;
}
.panel {
    background: #111a2e; border: 1px solid rgba(150,170,255,.15);
    border-radius: 16px; padding: 20px;
}
div[data-testid="stMetric"] {
    background: #111a2e; border: 1px solid rgba(150,170,255,.14);
    padding: 16px; border-radius: 14px;
}
div[data-testid="stMetricLabel"] { color: #9eaccd; }
div[data-testid="stMetricValue"] { color: #f4f6ff; }
.stButton > button {
    border: 0; border-radius: 10px; padding: .65rem 1.2rem;
    font-weight: 700; color: white;
    background: linear-gradient(90deg, #6477f5, #8a63e8);
}
.stButton > button:hover { border: 0; color: white; filter: brightness(1.12); }
.stDownloadButton > button {
    border-radius: 10px; border: 1px solid #596bba;
    background: #172342; color: #e9edff;
}
div[data-testid="stTabs"] button { color: #cbd4f5; }
hr { border-color: rgba(150,170,255,.14); }
.small-note { color: #8f9dbd; font-size: .8rem; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "research_result" not in st.session_state:
    st.session_state.research_result = None
if "research_topic" not in st.session_state:
    st.session_state.research_topic = ""

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## 🧠 ResearchAI")
    st.caption("MULTI-AGENT INTELLIGENCE")
    st.divider()

    st.markdown("### Workspace")
    st.markdown("**✦ New research**")
    st.markdown("**▤ Research report**")
    st.markdown("**◉ Quality review**")

    st.divider()
    st.markdown("### Agent workflow")
    st.markdown("🔎 **01 — Search Agent**")
    st.caption("Finds recent information and sources.")
    st.markdown("📖 **02 — Reader Agent**")
    st.caption("Reads and extracts useful web content.")
    st.markdown("✍️ **03 — Writer Agent**")
    st.caption("Creates a structured research report.")
    st.markdown("🛡️ **04 — Critic Agent**")
    st.caption("Reviews quality and gives feedback.")

    st.divider()
    st.markdown("### System")
    st.caption("Powered by LangChain · Groq · Tavily")
    st.caption("UI: Streamlit")

# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------
st.markdown("""
<div class="hero">
  <div class="eyebrow">AUTONOMOUS RESEARCH WORKSPACE</div>
  <div class="hero-title">Turn questions into <span style="color:#aab6ff">knowledge.</span></div>
  <div class="hero-sub">
    Research complex topics with a coordinated team of AI agents.
    Discover sources, read deeply, generate a report, and review its quality —
    all in one workspace.
  </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# AGENT OVERVIEW
# ---------------------------------------------------------
agent_cols = st.columns(4)
agents = [
    ("🔎", "Search Agent", "Discovers relevant web sources"),
    ("📖", "Reader Agent", "Extracts detailed page content"),
    ("✍️", "Writer Agent", "Drafts your research report"),
    ("🛡️", "Critic Agent", "Scores and reviews the report"),
]
for col, (icon, name, desc) in zip(agent_cols, agents):
    with col:
        st.markdown(
            f'<div class="agent-card"><div class="agent-icon">{icon}</div>'
            f'<div class="agent-name">{name}</div>'
            f'<div class="agent-desc">{desc}</div></div>',
            unsafe_allow_html=True,
        )

st.write("")
st.markdown('<div class="section-label">START A NEW RESEARCH TASK</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# RESEARCH INPUT
# ---------------------------------------------------------
with st.container():
    topic = st.text_input(
        "What would you like to research?",
        placeholder="e.g. Impact of generative AI on education in India",
        help="Enter a focused topic. Your four agents will process it in sequence.",
    )
    run_col, hint_col = st.columns([1, 3])
    with run_col:
        start_research = st.button("🚀  Start research", use_container_width=True)
    with hint_col:
        st.markdown(
            '<div class="small-note" style="padding-top:12px;">'
            'The pipeline may take some time because agents search, scrape, write, and review sequentially.'
            '</div>',
            unsafe_allow_html=True,
        )

if start_research:
    if not topic.strip():
        st.warning("Please enter a research topic before starting.")
    else:
        st.session_state.research_result = None
        st.session_state.research_topic = topic.strip()
        try:
            with st.status("Your AI research team is working...", expanded=True) as status:
                st.write("🔎 Search Agent: finding relevant information...")
                st.write("📖 Reader Agent: extracting detailed content...")
                st.write("✍️ Writer Agent: preparing the report...")
                st.write("🛡️ Critic Agent: evaluating the report...")
                result = run_research_pipeline(topic.strip())
                st.session_state.research_result = result
                status.update(
                    label="Research completed successfully!",
                    state="complete",
                    expanded=False,
                )
        except Exception as exc:
            st.error("The research pipeline encountered an error.")
            st.exception(exc)
            st.info(
                "Check that your API keys are available in the .env file and that "
                "the project modules and dependencies are installed."
            )

# ---------------------------------------------------------
# RESULTS
# ---------------------------------------------------------
result = st.session_state.research_result

if result:
    st.write("")
    st.divider()
    st.markdown('<div class="section-label">RESEARCH OVERVIEW</div>', unsafe_allow_html=True)
    st.subheader(st.session_state.research_topic)

    search_text = result.get("search_results", "")
    scraped_text = result.get("scraped_content", "")
    report_text = result.get("report", "")
    feedback_text = result.get("feedback", "")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Agents completed", "4 / 4")
    m2.metric("Search output", f"{len(search_text):,} chars")
    m3.metric("Page content", f"{len(scraped_text):,} chars")
    m4.metric("Report length", f"{len(report_text.split()):,} words")

    st.write("")
    report_tab, review_tab, sources_tab, reader_tab = st.tabs([
        "📄  Final Report",
        "🛡️  Critic Review",
        "🔎  Search Results",
        "📖  Reader Content",
    ])

    with report_tab:
        st.markdown("### Your research report")
        st.caption("Generated by the Writer Agent")
        if report_text:
            st.markdown(report_text)
            st.download_button(
                "⬇️ Download research report",
                data=report_text,
                file_name="research_report.md",
                mime="text/markdown",
                use_container_width=False,
            )
        else:
            st.info("The pipeline did not return a report.")

    with review_tab:
        st.markdown("### Quality assessment")
        st.caption("Generated by the Critic Agent")
        if feedback_text:
            st.markdown(feedback_text)
            st.download_button(
                "⬇️ Download critic review",
                data=feedback_text,
                file_name="critic_review.txt",
                mime="text/plain",
            )
        else:
            st.info("No critic feedback was returned.")

    with sources_tab:
        st.markdown("### Web search output")
        st.caption("Titles, URLs, and snippets returned by Tavily")
        st.text_area("Search results", search_text, height=420, disabled=True)

    with reader_tab:
        st.markdown("### Extracted page content")
        st.caption("Content returned by the Reader Agent")
        st.text_area("Scraped content", scraped_text, height=420, disabled=True)

    st.caption(
        f"Research generated on {datetime.now().strftime('%d %b %Y, %I:%M %p')} "
        "· Verify important claims against the original sources."
    )

else:
    st.write("")
    st.markdown("""
    <div class="panel">
      <div class="section-label">YOUR WORKSPACE IS READY</div>
      <h3 style="margin-top:4px;">Your next discovery starts here.</h3>
      <p style="color:#9eaccd;margin-bottom:0;">
        Enter a research topic above to activate the four-agent workflow.
        Your report and quality review will appear here when the pipeline finishes.
      </p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.caption("ResearchAI · Multi-Agent Research Assistant")

