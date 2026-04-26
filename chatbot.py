"""
Bremen Company Intelligence Chatbot
WHU · Data-Driven Entrepreneurship · SS 2026

Single-file RAG chatbot over the agent-collected Bremen company dataset.
Data source: df_agent_progress final (agent-enriched, 911 companies)
LLM: Groq llama-3.3-70b-versatile | Embeddings: FAISS + MiniLM
"""

import os
import re
import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
from groq import Groq
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# ── Constants ─────────────────────────────────────────────────────────────────
WHU_BLUE = "#2C4592"
WHU_RED  = "#E7331A"
DATA_FILE = "df_agent_progress final(Sheet1).csv"

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bremen Company Intelligence · WHU",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
  html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

  /* sidebar */
  section[data-testid="stSidebar"] {{
    background: {WHU_BLUE} !important;
  }}
  section[data-testid="stSidebar"] * {{
    color: #fff !important;
  }}
  section[data-testid="stSidebar"] input {{
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    color: #fff !important;
    border-radius: 4px;
  }}
  section[data-testid="stSidebar"] .stTextInput label {{
    color: rgba(255,255,255,0.75) !important;
    font-size: 12px !important;
  }}

  /* header bar */
  .whu-header {{
    background: {WHU_BLUE};
    padding: 16px 24px;
    border-radius: 0;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 16px;
  }}
  .whu-header h1 {{
    color: #fff;
    font-size: 20px;
    font-weight: 600;
    margin: 0;
  }}
  .whu-header .sub {{
    color: rgba(255,255,255,0.65);
    font-size: 12px;
    margin: 0;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }}

  /* metric cards */
  .metric-row {{ display: flex; gap: 12px; margin-bottom: 24px; flex-wrap: wrap; }}
  .metric-card {{
    flex: 1; min-width: 130px;
    background: #fff;
    border: 1px solid #e5e2d9;
    padding: 16px 18px;
    border-radius: 4px;
  }}
  .metric-card .val {{
    font-size: 28px; font-weight: 600;
    color: {WHU_BLUE}; line-height: 1;
  }}
  .metric-card .lbl {{
    font-size: 11px; color: #6b7493;
    margin-top: 5px; text-transform: uppercase;
    letter-spacing: 0.06em;
  }}

  /* chat bubbles */
  .bubble-user {{
    background: {WHU_BLUE}; color: #fff;
    padding: 12px 16px; border-radius: 4px;
    margin: 8px 0; font-size: 14px; line-height: 1.55;
    max-width: 80%; margin-left: auto;
  }}
  .bubble-bot {{
    background: #f4f6fb; color: #0e1530;
    border: 1px solid #e5e2d9;
    padding: 14px 18px; border-radius: 4px;
    margin: 8px 0; font-size: 14px; line-height: 1.6;
    max-width: 92%;
  }}
  .agent-tag {{
    font-size: 10px; font-weight: 600;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: {WHU_BLUE}; margin-bottom: 6px;
  }}
  .cited-bar {{
    margin-top: 10px; padding-top: 10px;
    border-top: 1px dashed #d6d2c5;
    font-size: 11px; color: #6b7493;
  }}

  /* chip */
  .chip {{
    display: inline-block; padding: 3px 10px;
    border: 1px solid #e5e2d9; border-radius: 999px;
    font-size: 10px; color: #3b4566;
    letter-spacing: 0.05em; text-transform: uppercase;
    background: #fff; margin-right: 4px;
  }}
  .chip.red {{ background: {WHU_RED}; color: #fff; border-color: {WHU_RED}; }}
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading Bremen dataset…")
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="latin-1", sep=";", engine="python", on_bad_lines="skip")

    # Keep only agent-collected columns, rename to friendly names
    col_map = {
        "company_name":                  "Company",
        "Legal_Form":                    "Legal Form",
        "Industry":                      "Industry",
        "B2B_or_B2C":                    "Customer Model",
        "Company_Description":           "Description",
        "Key_Activities_Product_Offerings": "Key Activities",
        "nace_section":                  "NACE Section",
        "incorporation_date":            "Founded",
        "country":                       "Country",
        "city":                          "City",
    }
    df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})

    keep = list(col_map.values())
    df = df[[c for c in keep if c in df.columns]].copy()

    # Clean up
    df.replace(["Not found", "n.a.", "N/A", "NA", "nan", ""], pd.NA, inplace=True)
    df = df[df["Company"].notna()].drop_duplicates(subset=["Company"]).reset_index(drop=True)

    # Normalise B2B/B2C
    def clean_b2b(v):
        if pd.isna(v): return "Unknown"
        v = str(v).strip().lower()
        if v.startswith("b2b") or v == "business": return "B2B"
        if v.startswith("b2c"): return "B2C"
        if "both" in v or ("b2b" in v and "b2c" in v): return "Both"
        return "Unknown"
    if "Customer Model" in df.columns:
        df["Customer Model"] = df["Customer Model"].apply(clean_b2b)

    return df


# ── Build FAISS vector store ──────────────────────────────────────────────────
@st.cache_resource(show_spinner="Building search index…")
def build_index(df: pd.DataFrame):
    docs = []
    for _, row in df.iterrows():
        parts = [
            f"Company: {row.get('Company', '')}",
            f"Industry: {row.get('Industry', '')}",
            f"Legal Form: {row.get('Legal Form', '')}",
            f"Customer Model: {row.get('Customer Model', '')}",
            f"NACE: {row.get('NACE Section', '')}",
            f"Founded: {row.get('Founded', '')}",
            f"Description: {row.get('Description', '')}",
            f"Key Activities: {row.get('Key Activities', '')}",
        ]
        text = "\n".join(p for p in parts if not p.endswith(": ") and "nan" not in p.lower())
        docs.append(Document(page_content=text, metadata={"company": row.get("Company", "")}))

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    return FAISS.from_documents(docs, embeddings), embeddings


# ── Groq client ───────────────────────────────────────────────────────────────
def get_client(api_key: str) -> Groq:
    return Groq(api_key=api_key)


def ask_llm(client: Groq, system: str, user: str, model: str = "llama-3.3-70b-versatile") -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=0.3,
        max_tokens=600,
    )
    return resp.choices[0].message.content.strip()


# ── Router ────────────────────────────────────────────────────────────────────
def route(client: Groq | None, question: str) -> str:
    """Returns 'lookup', 'filter', or 'general'."""
    if client:
        try:
            ans = ask_llm(client,
                "Classify the question. Reply with ONLY one word: 'lookup' (asking about a specific company), "
                "'filter' (asking to list/compare companies by industry, legal form, B2B/B2C etc.), "
                "or 'general' (anything else about Bremen companies or the dataset).",
                f"Question: {question}")
            w = ans.lower().strip().replace("'", "")
            if w in ("lookup", "filter", "general"): return w
        except Exception:
            pass

    q = question.lower()
    if re.search(r"(tell me about|who is|what does|describe|is .+ a)", q): return "lookup"
    if re.search(r"(list|show|find|which companies|all companies|companies (in|with|that)|filter|b2b|b2c)", q): return "filter"
    return "general"


# ── Agents ────────────────────────────────────────────────────────────────────
def lookup_agent(client: Groq | None, df: pd.DataFrame, vectorstore, question: str):
    """Look up a specific company by name or keyword."""
    docs = vectorstore.similarity_search(question, k=5)
    cited = [d.metadata["company"] for d in docs]
    ctx = "\n\n---\n".join(d.page_content for d in docs)

    if client:
        answer = ask_llm(client,
            "You are a Bremen company analyst. Use ONLY the context below. "
            "Answer in 3–5 sentences. Be specific — name the company, its industry, "
            "legal form, customer model, and what it does.",
            f"Context:\n{ctx}\n\nQuestion: {question}")
    else:
        r = df[df["Company"].str.contains(docs[0].metadata["company"][:15], case=False, na=False)]
        if not r.empty:
            row = r.iloc[0]
            answer = (f"**{row.get('Company','')}** is in the **{row.get('Industry','—')}** sector. "
                      f"Legal form: {row.get('Legal Form','—')}. "
                      f"Customer model: {row.get('Customer Model','—')}. "
                      f"{str(row.get('Description',''))[:300]}")
        else:
            answer = ctx[:500]

    return answer, cited


def filter_agent(client: Groq | None, df: pd.DataFrame, question: str):
    """Filter companies by industry, legal form, B2B/B2C etc."""
    q = question.lower()

    # Detect filters
    filtered = df.copy()
    filter_desc = []

    # B2B / B2C
    if "b2b" in q:
        filtered = filtered[filtered["Customer Model"] == "B2B"]
        filter_desc.append("B2B")
    elif "b2c" in q:
        filtered = filtered[filtered["Customer Model"] == "B2C"]
        filter_desc.append("B2C")

    # Industry keyword match
    industry_kw = re.findall(r"(logistics|tech|software|real estate|construction|finance|health|education|"
                              r"manufacturing|retail|transport|hospitality|hotel|food|energy|legal|media|"
                              r"consulting|engineering|shipping|insurance)", q)
    if industry_kw and "Industry" in filtered.columns:
        pattern = "|".join(industry_kw)
        mask = filtered["Industry"].str.contains(pattern, case=False, na=False)
        if mask.sum() > 0:
            filtered = filtered[mask]
            filter_desc.append(f"industry: {', '.join(industry_kw)}")

    # Legal form
    for lf in ["gmbh", "ag", "kg", "e.v."]:
        if lf in q and "Legal Form" in filtered.columns:
            mask = filtered["Legal Form"].str.contains(lf, case=False, na=False)
            if mask.sum() > 0:
                filtered = filtered[mask]
                filter_desc.append(f"legal form: {lf.upper()}")

    n = len(filtered)
    sample = filtered.head(10)
    rows_text = "\n".join(
        f"• {r.get('Company','?')} | {r.get('Industry','—')} | {r.get('Legal Form','—')} | {r.get('Customer Model','—')}"
        for _, r in sample.iterrows()
    )
    b2b_n = (filtered["Customer Model"] == "B2B").sum() if "Customer Model" in filtered.columns else 0
    b2c_n = (filtered["Customer Model"] == "B2C").sum() if "Customer Model" in filtered.columns else 0

    summary = f"Found **{n} companies**" + (f" matching: {', '.join(filter_desc)}" if filter_desc else "") + "."
    stats = f"B2B: {b2b_n} · B2C: {b2c_n}"

    if client:
        ctx = f"{summary}\n{stats}\n\nSample:\n{rows_text}"
        answer = ask_llm(client,
            "You are a Bremen company analyst. Summarise the filtered results clearly. "
            "Mention total count, B2B/B2C split, and highlight any interesting patterns. Be concise.",
            f"{ctx}\n\nUser asked: {question}")
    else:
        answer = f"{summary}\n{stats}\n\n**Sample companies:**\n{rows_text}"

    cited = sample["Company"].tolist()
    return answer, cited, filtered


def general_agent(client: Groq | None, df: pd.DataFrame, vectorstore, question: str):
    """General Q&A about the Bremen dataset."""
    docs = vectorstore.similarity_search(question, k=6)
    cited = [d.metadata["company"] for d in docs]
    ctx = "\n\n---\n".join(d.page_content for d in docs)

    n = len(df)
    b2b_pct = round((df["Customer Model"] == "B2B").sum() / n * 100, 1) if "Customer Model" in df.columns else 0
    b2c_pct = round((df["Customer Model"] == "B2C").sum() / n * 100, 1) if "Customer Model" in df.columns else 0
    top_industries = df["Industry"].value_counts().head(5).to_dict() if "Industry" in df.columns else {}

    stats = (f"Dataset: {n} Bremen companies. B2B: {b2b_pct}%, B2C: {b2c_pct}%. "
             f"Top industries: {', '.join(f'{k} ({v})' for k,v in top_industries.items())}.")

    if client:
        answer = ask_llm(client,
            f"You are a Bremen company analyst for WHU DDE project. {stats} "
            "Use the retrieved context and dataset stats to answer. Be concise and specific.",
            f"Context:\n{ctx}\n\nQuestion: {question}")
    else:
        answer = (f"**Dataset overview:** {stats}\n\n"
                  f"Most relevant companies for your query:\n" +
                  "\n".join(f"• {d.metadata['company']}" for d in docs[:4]))

    return answer, cited


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏛️ WHU DDE")
    st.markdown("**Bremen Company Intelligence**")
    st.markdown("---")

    # API Key
    default_key = ""
    if os.path.exists("groq.txt"):
        with open("groq.txt") as f:
            default_key = f.readline().strip()
    if not default_key:
        try:
            default_key = st.secrets.get("GROQ_API_KEY", "")
        except Exception:
            default_key = ""

    api_key = st.text_input("Groq API Key", value=default_key, type="password", placeholder="gsk_…")

    st.markdown("---")

    # Data file path
    data_path = st.text_input("Dataset path", value=DATA_FILE,
                               help="Path to your agent-collected CSV file")

    st.markdown("---")
    st.markdown("""
**Agent pipeline:**
- ⌥ **Router** — classifies intent
- 🔍 **Lookup** — specific company
- 📋 **Filter** — list / compare
- 💬 **General** — open questions
""")
    st.markdown("---")
    st.markdown("*WHU · DDE · SS 2026*")


# ── Load data & index ─────────────────────────────────────────────────────────
try:
    df = load_data(data_path)
except FileNotFoundError:
    st.error(f"Dataset not found at `{data_path}`. Update the path in the sidebar.")
    st.stop()

vectorstore, _ = build_index(df)
client = get_client(api_key) if api_key else None

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="whu-header">
  <div>
    <h1>Bremen Company Intelligence</h1>
    <p class="sub">WHU · Data-Driven Entrepreneurship · SS 2026 · {len(df):,} companies</p>
  </div>
</div>
""", unsafe_allow_html=True)

# Metrics
n = len(df)
b2b = int((df["Customer Model"] == "B2B").sum()) if "Customer Model" in df.columns else 0
b2c = int((df["Customer Model"] == "B2C").sum()) if "Customer Model" in df.columns else 0
industries = df["Industry"].nunique() if "Industry" in df.columns else 0

st.markdown(f"""
<div class="metric-row">
  <div class="metric-card"><div class="val">{n:,}</div><div class="lbl">Companies</div></div>
  <div class="metric-card"><div class="val">{b2b}</div><div class="lbl">B2B</div></div>
  <div class="metric-card"><div class="val">{b2c}</div><div class="lbl">B2C</div></div>
  <div class="metric-card"><div class="val">{industries}</div><div class="lbl">Industries</div></div>
</div>
""", unsafe_allow_html=True)

# Mode chip
mode = "🤖 Groq · Llama-3.3-70B" if client else "⚡ Offline mode (add Groq key for smarter answers)"
st.markdown(f'<span class="chip{"  red" if client else ""}">{mode}</span>', unsafe_allow_html=True)

# ── Chat ──────────────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# Suggestions
if not st.session_state.history:
    st.markdown("**Try asking:**")
    cols = st.columns(3)
    suggestions = [
        "Tell me about ArcelorMittal",
        "List all B2B logistics companies",
        "Which companies are in real estate?",
        "Show me GmbH companies in tech",
        "What industries are most common?",
        "Find consulting companies",
    ]
    for i, s in enumerate(suggestions):
        if cols[i % 3].button(s, key=f"sug_{i}"):
            st.session_state.history.append({"role": "user", "content": s})
            st.rerun()

# Display history
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(f'<div class="bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        agent_tag = msg.get("agent", "AGENT")
        cited = msg.get("cited", [])
        cited_html = ""
        if cited:
            cited_html = f'<div class="cited-bar">📌 Cited: {" · ".join(cited[:4])}</div>'
        st.markdown(
            f'<div class="bubble-bot"><div class="agent-tag">{agent_tag}</div>'
            f'{msg["content"]}{cited_html}</div>',
            unsafe_allow_html=True
        )

# Input
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        question = st.text_input("", placeholder="Ask anything about Bremen's companies…", label_visibility="collapsed")
    with col2:
        submitted = st.form_submit_button("Send →", use_container_width=True)

if submitted and question.strip():
    st.session_state.history.append({"role": "user", "content": question})

    with st.spinner("Thinking…"):
        intent = route(client, question)

        if intent == "lookup":
            answer, cited = lookup_agent(client, df, vectorstore, question)
            st.session_state.history.append({"role": "bot", "content": answer, "cited": cited, "agent": "🔍 LOOKUP"})

        elif intent == "filter":
            answer, cited, _ = filter_agent(client, df, question)
            st.session_state.history.append({"role": "bot", "content": answer, "cited": cited, "agent": "📋 FILTER"})

        else:
            answer, cited = general_agent(client, df, vectorstore, question)
            st.session_state.history.append({"role": "bot", "content": answer, "cited": cited, "agent": "💬 GENERAL"})

    st.rerun()

# Clear button
if st.session_state.history:
    if st.button("🗑 Clear chat"):
        st.session_state.history = []
        st.rerun()
