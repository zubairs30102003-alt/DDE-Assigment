"""
WHU Bremen Company Intelligence Platform
Multi-Agent AI Explorer with WHU Branding
"""

import streamlit as st
import os
import re
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from groq import Groq
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# ── Brand Constants ───────────────────────────────────────────────────────────
WHU_BLUE    = "#2C4592"
WHU_BLUE_LT = "#3D5BA9"
WHU_RED     = "#E7331A"
WHU_GREY    = "#F4F6FB"
WHU_DARK    = "#1A2D6B"
WHU_TEXT    = "#1C2B4A"

LOGO_PATH      = "whu_brand_styler/assets/whu-logo-full.png"
LOGO_ICON_PATH = "whu_brand_styler/assets/whu-logo-icon.png"
LOGO_B64_PATH  = "whu_brand_styler/assets/logo_full_base64.txt"
ICON_B64_PATH  = "whu_brand_styler/assets/logo_icon_base64.txt"

def get_logo_b64(path):
    try:
        with open(path) as f:
            return f.read().strip()
    except:
        return ""

LOGO_B64 = get_logo_b64(LOGO_B64_PATH)
ICON_B64 = get_logo_b64(ICON_B64_PATH)

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WHU · Bremen Company Intelligence",
    page_icon=f"data:image/png;base64,{ICON_B64}" if ICON_B64 else "🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    color: {WHU_TEXT};
}}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 0 !important; max-width: 1400px; }}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {WHU_DARK};
    border-right: none;
}}
[data-testid="stSidebar"] * {{
    color: white !important;
}}
[data-testid="stSidebar"] .stTextInput input {{
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    color: white !important;
    border-radius: 8px;
}}
[data-testid="stSidebar"] .stTextInput input::placeholder {{
    color: rgba(255,255,255,0.5) !important;
}}
[data-testid="stSidebar"] [data-testid="stMetricValue"] {{
    color: white !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
}}
[data-testid="stSidebar"] [data-testid="stMetricLabel"] {{
    color: rgba(255,255,255,0.7) !important;
    font-size: 0.75rem !important;
}}
[data-testid="stSidebar"] hr {{
    border-color: rgba(255,255,255,0.15) !important;
}}

/* ── Top Header Bar ── */
.whu-header {{
    background: linear-gradient(135deg, {WHU_DARK} 0%, {WHU_BLUE} 100%);
    padding: 18px 36px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: -1rem -1rem 0 -1rem;
    box-shadow: 0 2px 12px rgba(44,69,146,0.3);
}}
.whu-header-left {{ display: flex; align-items: center; gap: 20px; }}
.whu-header-title {{
    color: white;
    font-size: 1.15rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    border-left: 2px solid rgba(255,255,255,0.3);
    padding-left: 20px;
    line-height: 1.3;
}}
.whu-header-sub {{
    color: rgba(255,255,255,0.65);
    font-size: 0.75rem;
    font-weight: 400;
    margin-top: 2px;
}}
.whu-header-badge {{
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    color: white;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 0.05em;
}}

/* ── Tabs ── */
[data-testid="stTabs"] button {{
    font-weight: 500;
    font-size: 0.875rem;
    color: #6B7280;
    border-radius: 0;
    padding: 10px 20px;
}}
[data-testid="stTabs"] button[aria-selected="true"] {{
    color: {WHU_BLUE} !important;
    border-bottom: 2px solid {WHU_BLUE} !important;
    font-weight: 600;
}}

/* ── Metric Cards ── */
.metric-row {{ display: flex; gap: 16px; margin: 20px 0; flex-wrap: wrap; }}
.metric-card {{
    background: white;
    border: 1px solid #E5E9F5;
    border-radius: 12px;
    padding: 20px 24px;
    flex: 1;
    min-width: 160px;
    box-shadow: 0 1px 4px rgba(44,69,146,0.06);
    position: relative;
    overflow: hidden;
}}
.metric-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, {WHU_BLUE}, {WHU_BLUE_LT});
}}
.metric-value {{
    font-size: 2rem;
    font-weight: 700;
    color: {WHU_BLUE};
    line-height: 1;
    margin-bottom: 4px;
}}
.metric-label {{
    font-size: 0.75rem;
    color: #6B7280;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
.metric-sub {{
    font-size: 0.8rem;
    color: #9CA3AF;
    margin-top: 4px;
}}

/* ── Chat Messages ── */
[data-testid="stChatMessage"] {{
    border-radius: 12px !important;
    margin-bottom: 8px !important;
}}

/* ── Example Question Buttons ── */
.stButton button {{
    background: white !important;
    border: 1.5px solid #E5E9F5 !important;
    color: {WHU_BLUE} !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    padding: 8px 12px !important;
    text-align: left !important;
    line-height: 1.3 !important;
    transition: all 0.15s ease !important;
    height: auto !important;
    white-space: normal !important;
}}
.stButton button:hover {{
    background: {WHU_GREY} !important;
    border-color: {WHU_BLUE} !important;
    box-shadow: 0 2px 8px rgba(44,69,146,0.12) !important;
}}

/* ── Chat Input ── */
[data-testid="stChatInput"] textarea {{
    border-radius: 12px !important;
    border: 1.5px solid #E5E9F5 !important;
    font-size: 0.9rem !important;
}}
[data-testid="stChatInput"] textarea:focus {{
    border-color: {WHU_BLUE} !important;
    box-shadow: 0 0 0 3px rgba(44,69,146,0.1) !important;
}}

/* ── Agent Status ── */
.agent-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: {WHU_GREY};
    border: 1px solid #E5E9F5;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.72rem;
    font-weight: 600;
    color: {WHU_BLUE};
    margin-top: 6px;
}}

/* ── Section headers ── */
.section-header {{
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: rgba(255,255,255,0.5);
    margin: 20px 0 8px 0;
}}

/* ── Finding chips ── */
.finding-chip {{
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    font-size: 0.8rem;
    line-height: 1.4;
}}
.finding-chip:last-child {{ border-bottom: none; }}
.chip-dot {{
    width: 6px; height: 6px;
    border-radius: 50%;
    background: {WHU_RED};
    margin-top: 5px;
    flex-shrink: 0;
}}

/* ── Sidebar logo area ── */
.sidebar-logo-area {{
    padding: 20px 16px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.12);
    margin-bottom: 4px;
}}
.sidebar-logo-area img {{ height: 36px; filter: brightness(0) invert(1); }}
.sidebar-app-name {{
    font-size: 0.7rem;
    color: rgba(255,255,255,0.5);
    margin-top: 6px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}}

/* ── Plotly charts ── */
.js-plotly-plot {{ border-radius: 12px; }}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {{ border-radius: 12px !important; }}

/* ── Select/multiselect ── */
[data-baseweb="select"] {{
    border-radius: 8px !important;
}}

/* ── Status boxes ── */
[data-testid="stStatus"] {{
    border-radius: 10px !important;
    border: 1px solid #E5E9F5 !important;
}}

/* ── Sidebar warning/info ── */
[data-testid="stSidebar"] .stWarning {{
    background: rgba(231,51,26,0.15) !important;
    border: 1px solid rgba(231,51,26,0.3) !important;
    border-radius: 8px;
}}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
logo_html = (
    f'<img src="data:image/png;base64,{LOGO_B64}" style="height:38px;">'
    if LOGO_B64 else
    f'<span style="color:white;font-size:1.5rem;font-weight:800;">WHU</span>'
)

st.markdown(f"""
<div class="whu-header">
    <div class="whu-header-left">
        {logo_html}
        <div class="whu-header-title">
            Bremen Company Intelligence
            <div class="whu-header-sub">Data-Driven Entrepreneurship · SS 2025</div>
        </div>
    </div>
    <div class="whu-header-badge">MULTI-AGENT AI PLATFORM</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    icon_html = (
        f'<img src="data:image/png;base64,{ICON_B64}" style="height:40px;">'
        if ICON_B64 else ""
    )
    st.markdown(f"""
    <div class="sidebar-logo-area">
        {icon_html}
        <div class="sidebar-app-name">Company Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">API Configuration</div>', unsafe_allow_html=True)

    default_key = ""
    if os.path.exists("groq.txt"):
        with open("groq.txt") as f:
            default_key = f.readline().strip()
    if not default_key:
        try:
            default_key = st.secrets.get("GROQ_API_KEY", "")
        except Exception:
            default_key = ""

    api_key = st.text_input(
        "Groq API Key",
        value=default_key,
        type="password",
        placeholder="gsk_..."
    )
    if default_key:
        st.caption("🔒 Pre-filled from secrets")

    st.markdown("---")
    st.markdown('<div class="section-header">Agent Workflow</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.8rem; line-height:1.9;">
        <div>🔀 <b>Router</b> — classifies intent</div>
        <div>📝 <b>Text Agent</b> — RAG answers</div>
        <div>💻 <b>Code Agent</b> — live queries</div>
        <div>📊 <b>Visual Agent</b> — charts</div>
        <div>✏️ <b>Editor</b> — polishes output</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-header">Key Findings</div>', unsafe_allow_html=True)
    findings = [
        ("11.8%", "of Bremen companies are Scalers"),
        ("Hospitality", "highest scaling sector (32.5%)"),
        ("AG legal form", "scales best at 18.2%"),
        ("B2C companies", "scale less (6.7% vs 12.2%)"),
        ("KG legal form", "least likely to scale (3.2%)"),
    ]
    for val, desc in findings:
        st.markdown(f"""
        <div class="finding-chip">
            <div class="chip-dot"></div>
            <div><b>{val}</b> {desc}</div>
        </div>
        """, unsafe_allow_html=True)

if not api_key:
    st.warning("⚠️ Enter your Groq API key in the sidebar to activate the platform.")
    st.stop()

os.environ["GROQ_API_KEY"] = api_key
groq_client = Groq(api_key=api_key)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_df():
    if os.path.exists("bremen_merged_final.csv"):
        return pd.read_csv("bremen_merged_final.csv").fillna("Not found")
    return pd.read_excel("df_agent_progress.xlsx").fillna("Not found")

df = load_df()

# ── Sidebar metrics (after data loads) ───────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    st.markdown('<div class="section-header">Dataset</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.metric("Companies", f"{len(df):,}")
    if 'Scaler_2024' in df.columns:
        c2.metric("Scalers", f"{int(df['Scaler_2024'].sum())}")

# ── RAG Chain ─────────────────────────────────────────────────────────────────
@st.cache_resource
def build_rag(_key):
    docs = [
        Document(page_content="\n".join(f"{c}: {row[c]}" for c in df.columns))
        for _, row in df.iterrows()
    ]
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vs = FAISS.from_documents(docs, embeddings)
    retriever = vs.as_retriever(search_kwargs={"k": 8})
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=_key)
    prompt = ChatPromptTemplate.from_template("""You are an analyst for Bremen, Germany company data.
Answer using ONLY the context. Be concise and data-driven.

Context: {context}
Question: {question}
Answer:""")
    return (
        {"context": retriever | (lambda docs: "\n\n---\n\n".join(d.page_content for d in docs)),
         "question": RunnablePassthrough()}
        | prompt | llm | StrOutputParser()
    )

rag_chain = build_rag(api_key)

# ══════════════════════════════════════════════════════════════════════════════
# AGENTS
# ══════════════════════════════════════════════════════════════════════════════
def call_groq(system, user, model="llama-3.3-70b-versatile"):
    r = groq_client.chat.completions.create(
        model=model,
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        temperature=0.1, max_tokens=1024
    )
    return r.choices[0].message.content.strip()

def router_agent(q):
    sys = ('Classify the question into exactly one: "text", "code", or "visual".\n'
           '"text"=factual/company specific. "code"=stats/counts/aggregation. "visual"=chart/graph.\n'
           'Reply with ONLY one word.')
    r = call_groq(sys, q).lower().strip().strip('"').strip("'")
    return r if r in ["text","code","visual"] else "text"

def text_agent(q):
    return rag_chain.invoke(q), None

def code_agent(q):
    cols = ", ".join(df.columns)
    sys = f"""You are a pandas analyst. DataFrame `df` has columns: {cols}
Write a short snippet, store result in `result` (str/number/DataFrame).
No imports, no print(). Return ONLY code."""
    code = re.sub(r"```(?:python)?|```", "", call_groq(sys, q)).strip()
    safe = {"df":df,"pd":pd,"np":np,"result":None}
    try:
        exec(code, safe)
        r = safe.get("result","No result.")
        if isinstance(r, pd.DataFrame):
            ans = r.to_markdown() if len(r)<=30 else r.head(20).to_markdown()+f"\n\n*...+{len(r)-20} more*"
        else:
            ans = str(r)
    except Exception as e:
        ans = f"Query error: {e}"
    return ans, None

def visual_agent(q):
    cols = ", ".join(df.columns)
    sys = f"""You are a Plotly expert. DataFrame `df` columns: {cols}
Create a plotly figure, store in `fig`. Use px or go (available).
No imports. Return ONLY code."""
    code = re.sub(r"```(?:python)?|```", "", call_groq(sys, q)).strip()
    safe = {"df":df,"pd":pd,"np":np,"px":px,"go":go,"fig":None}
    try:
        exec(code, safe)
        fig = safe.get("fig")
        if fig:
            # Apply WHU styling
            fig.update_layout(
                font_family="Inter",
                paper_bgcolor="white",
                plot_bgcolor="white",
                title_font_color=WHU_BLUE,
                colorway=[WHU_BLUE, WHU_RED, WHU_BLUE_LT, "#5B7FD4", "#8CA5E0"],
            )
            return "Here's your chart:", fig
        return "Could not generate chart.", None
    except Exception as e:
        return f"Visualization error: {e}", None

def editor_agent(q, raw, route):
    if route == "visual": return raw
    sys = ("Edit this analyst answer: fix grammar, make it concise and professional. "
           "Keep all numbers exact. Return only the polished answer.")
    return call_groq(sys, f"Q: {q}\nAnswer: {raw}")

def run_pipeline(q):
    with st.status("🔀 **Router Agent** — classifying your question…", expanded=False) as s:
        route = router_agent(q)
        icon = {"text":"📝","code":"💻","visual":"📊"}.get(route,"📝")
        s.update(label=f"🔀 Routed to **{icon} {route.upper()} Agent**", state="complete")

    label = {"text":"📝 **Text Agent** — searching knowledge base…",
             "code":"💻 **Code Agent** — running data query…",
             "visual":"📊 **Visual Agent** — generating chart…"}.get(route,"📝 Thinking…")

    with st.status(label, expanded=False) as s:
        if route=="text":    raw, fig = text_agent(q)
        elif route=="code":  raw, fig = code_agent(q)
        else:                raw, fig = visual_agent(q)
        s.update(label=label.split("—")[0]+"— done", state="complete")

    if route != "visual":
        with st.status("✏️ **Editor Agent** — polishing answer…", expanded=False) as s:
            final = editor_agent(q, raw, route)
            s.update(label="✏️ **Editor Agent** — done", state="complete")
    else:
        final = raw

    return route, final, fig

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["💬  Chat", "📊  Analytics Dashboard", "🔍  Data Explorer"])

# ── Tab 1: Chat ───────────────────────────────────────────────────────────────
with tab1:
    # Metric strip
    if 'Scaler_2024' in df.columns:
        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{len(df):,}</div>
                <div class="metric-label">Companies</div>
                <div class="metric-sub">&gt;10 employees · Bremen</div>
            </div>""", unsafe_allow_html=True)
        with mc2:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{int(df['Scaler_2024'].sum())}</div>
                <div class="metric-label">Scalers 2024</div>
                <div class="metric-sub">{df['Scaler_2024'].mean():.1%} of dataset</div>
            </div>""", unsafe_allow_html=True)
        with mc3:
            b2b_n = int((df.get('B2B_or_B2C',pd.Series())=='B2B').sum()) if 'B2B_or_B2C' in df.columns else 0
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{b2b_n}</div>
                <div class="metric-label">B2B Companies</div>
                <div class="metric-sub">Business-to-business</div>
            </div>""", unsafe_allow_html=True)
        with mc4:
            gmbh_n = int((df.get('Legal_Form',pd.Series())=='GmbH').sum()) if 'Legal_Form' in df.columns else 0
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{gmbh_n}</div>
                <div class="metric-label">GmbH Companies</div>
                <div class="metric-sub">Most common legal form</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Example questions
    st.markdown("**💡 Quick questions — click to ask:**")
    examples = [
        "Which industries scale the most?",
        "Show scaling rate by legal form as a chart",
        "How many B2B companies are scalers?",
        "Tell me about logistics companies",
        "Show employee growth as a histogram",
    ]
    ecols = st.columns(5)
    for i, q in enumerate(examples):
        if ecols[i].button(q, key=f"ex_{i}", use_container_width=True):
            st.session_state["pending_q"] = q

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("fig"):
                st.plotly_chart(msg["fig"], use_container_width=True)
            if msg.get("route"):
                icons = {"text":"📝","code":"💻","visual":"📊"}
                st.markdown(
                    f'<div class="agent-badge">'
                    f'{icons.get(msg["route"],"🤖")} Handled by {msg["route"].upper()} Agent'
                    f'</div>',
                    unsafe_allow_html=True
                )

    pending = st.session_state.pop("pending_q", None)
    question = st.chat_input("Ask anything about Bremen companies…") or pending

    if question:
        st.session_state.messages.append({"role":"user","content":question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            route, answer, fig = run_pipeline(question)
            st.markdown(answer)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            icons = {"text":"📝","code":"💻","visual":"📊"}
            st.markdown(
                f'<div class="agent-badge">'
                f'{icons.get(route,"🤖")} Handled by {route.upper()} Agent'
                f'</div>',
                unsafe_allow_html=True
            )

        st.session_state.messages.append({
            "role":"assistant","content":answer,"fig":fig,"route":route
        })

# ── Tab 2: Dashboard ──────────────────────────────────────────────────────────
with tab2:
    st.markdown("### Bremen Company Analytics")

    CHART_THEME = dict(
        font_family="Inter",
        paper_bgcolor="white",
        plot_bgcolor="white",
        title_font=dict(color=WHU_BLUE, size=14, family="Inter"),
        margin=dict(t=48, b=32, l=20, r=20),
    )

    # Row 1: Legal form + B2B
    c1, c2 = st.columns(2)
    with c1:
        if 'Legal_Form' in df.columns and 'Scaler_2024' in df.columns:
            lf = df.groupby('Legal_Form')['Scaler_2024'].agg(['mean','count']).reset_index()
            lf = lf[lf['count']>=10].sort_values('mean')
            lf.columns = ['Legal Form','Scale Rate','Count']
            fig = px.bar(lf, x='Scale Rate', y='Legal Form', orientation='h',
                         title='Scaling Rate by Legal Form',
                         color='Scale Rate', color_continuous_scale=[[0,'#E5E9F5'],[1,WHU_BLUE]],
                         text=lf['Scale Rate'].map(lambda x: f"{x:.1%}"),
                         hover_data=['Count'])
            fig.update_traces(textposition='outside')
            fig.update_coloraxes(showscale=False)
            fig.update_layout(**CHART_THEME, xaxis_title="Scale Rate", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        if 'B2B_or_B2C' in df.columns and 'Scaler_2024' in df.columns:
            b2b = df[df['B2B_or_B2C'].isin(['B2B','B2C','Both'])].groupby('B2B_or_B2C')['Scaler_2024'].agg(['mean','count']).reset_index()
            b2b.columns = ['Business Model','Scale Rate','Count']
            colors = {
                'B2B': WHU_BLUE,
                'B2C': WHU_RED,
                'Both': WHU_BLUE_LT
            }
            fig2 = px.bar(b2b, x='Business Model', y='Scale Rate',
                          title='Scaling Rate by Business Model',
                          color='Business Model',
                          color_discrete_map=colors,
                          text=b2b['Scale Rate'].map(lambda x: f"{x:.1%}"),
                          hover_data=['Count'])
            fig2.update_traces(textposition='outside')
            fig2.update_layout(**CHART_THEME, showlegend=False, yaxis_title="Scale Rate")
            st.plotly_chart(fig2, use_container_width=True)

    # Row 2: NACE sectors
    if 'NACE_Section' in df.columns and 'Scaler_2024' in df.columns:
        nace_labels = {
            'C':'Manufacturing','F':'Construction','G':'Wholesale/Retail',
            'H':'Transport','I':'Hospitality','J':'ICT',
            'K':'Finance','L':'Real Estate','M':'Professional Services',
            'N':'Admin Support','P':'Education','Q':'Health',
            'R':'Arts & Recreation','S':'Other Services'
        }
        nace = df.groupby('NACE_Section')['Scaler_2024'].agg(['mean','count']).reset_index()
        nace = nace[nace['count']>=5].sort_values('mean',ascending=False)
        nace.columns = ['NACE','Scale Rate','Count']
        nace['Sector'] = nace['NACE'].map(nace_labels).fillna(nace['NACE'])
        fig3 = px.bar(nace, x='Sector', y='Scale Rate',
                      title='Scaling Rate by Industry Sector (NACE)',
                      color='Scale Rate',
                      color_continuous_scale=[[0,'#E5E9F5'],[0.5,WHU_BLUE_LT],[1,WHU_BLUE]],
                      text=nace['Scale Rate'].map(lambda x: f"{x:.1%}"),
                      hover_data=['Count','NACE'])
        fig3.update_traces(textposition='outside')
        fig3.update_coloraxes(showscale=False)
        fig3.update_layout(**CHART_THEME, xaxis_tickangle=30, yaxis_title="Scale Rate", xaxis_title="")
        st.plotly_chart(fig3, use_container_width=True)

    # Row 3: Age box + employee dist
    c3, c4 = st.columns(2)
    with c3:
        if 'Company_Age' in df.columns and 'Scaler_2024' in df.columns:
            age_df = df[df['Scaler_2024'].isin([0,1])].copy()
            age_df['Status'] = age_df['Scaler_2024'].map({0:'Non-Scaler',1:'Scaler'})
            fig4 = px.box(age_df, x='Status', y='Company_Age',
                          title='Company Age: Scalers vs Non-Scalers',
                          color='Status',
                          color_discrete_map={'Scaler':WHU_BLUE,'Non-Scaler':'#CBD5E1'})
            fig4.update_layout(**CHART_THEME, showlegend=False, yaxis_title="Age (years)")
            st.plotly_chart(fig4, use_container_width=True)

    with c4:
        emp_col = 'Number of employees 2024'
        if emp_col in df.columns:
            emp_df = pd.to_numeric(df[emp_col], errors='coerce').dropna()
            emp_df = emp_df[emp_df <= emp_df.quantile(0.95)]
            fig5 = px.histogram(emp_df, nbins=40,
                                title='Employee Size Distribution (2024)',
                                color_discrete_sequence=[WHU_BLUE])
            fig5.update_layout(**CHART_THEME, xaxis_title="Employees", yaxis_title="Count")
            st.plotly_chart(fig5, use_container_width=True)

# ── Tab 3: Explorer ───────────────────────────────────────────────────────────
with tab3:
    st.markdown("### Filter & Explore Companies")

    fc1, fc2, fc3 = st.columns(3)
    scaler_f = fc1.selectbox("Scaler Status", ["All","✅ Scaler","Non-Scaler"])
    legal_opts = sorted(df['Legal_Form'].dropna().unique().tolist()) if 'Legal_Form' in df.columns else []
    legal_f = fc2.multiselect("Legal Form", options=legal_opts)
    b2b_f = fc3.multiselect("Business Model", options=["B2B","B2C","Both"])

    fdf = df.copy()
    if scaler_f == "✅ Scaler" and 'Scaler_2024' in df.columns:
        fdf = fdf[fdf['Scaler_2024']==1]
    elif scaler_f == "Non-Scaler" and 'Scaler_2024' in df.columns:
        fdf = fdf[fdf['Scaler_2024']==0]
    if legal_f:
        fdf = fdf[fdf['Legal_Form'].isin(legal_f)]
    if b2b_f and 'B2B_or_B2C' in df.columns:
        fdf = fdf[fdf['B2B_or_B2C'].isin(b2b_f)]

    st.markdown(f"<div style='color:{WHU_BLUE};font-weight:600;font-size:0.85rem;margin:8px 0'>Showing {len(fdf):,} companies</div>", unsafe_allow_html=True)

    disp = ['Company name Latin alphabet','Legal_Form','B2B_or_B2C',
            'Industry','Scaler_2024','Number of employees 2024',
            'Company_Age','Company_Description']
    disp = [c for c in disp if c in fdf.columns]
    st.dataframe(fdf[disp].reset_index(drop=True), use_container_width=True, height=480)

    dl1, dl2, _ = st.columns([1,1,4])
    csv = fdf[disp].to_csv(index=False)
    dl1.download_button(
        "⬇️ Download CSV", csv,
        file_name="bremen_filtered.csv", mime="text/csv",
        use_container_width=True
    )
