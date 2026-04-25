"""
Bremen Companies — Multi-Agent Explorer
5-Step Agent Workflow:
  1. User Question
  2. Router Agent  → classifies as text / code / visual
  3. Specialist Agent (Text | Code | Visual)
  4. Editor Agent  → polishes the answer
  5. Final Output
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

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bremen Companies Explorer",
    layout="wide",
    page_icon="🏭"
)

# ── Sidebar: API Key ──────────────────────────────────────────────────────────
st.sidebar.title("⚙️ Configuration")

# Load key: Streamlit Cloud secrets → groq.txt → empty
default_key = st.secrets.get("GROQ_API_KEY", "") if hasattr(st, "secrets") else ""
if not default_key and os.path.exists("groq.txt"):
    with open("groq.txt") as f:
        default_key = f.readline().strip()

api_key = st.sidebar.text_input(
    "Groq API Key", value=default_key, type="password",
    placeholder="Enter your Groq API key..."
)
if default_key:
    st.sidebar.caption("Pre-filled from secrets / groq.txt")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🤖 Agent Workflow")
st.sidebar.markdown("""
1. **Router** — classifies your question
2. **Text Agent** — factual RAG answers
3. **Code Agent** — live data queries
4. **Visual Agent** — generates charts
5. **Editor** — polishes the output
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Key Findings")
st.sidebar.markdown("""
- **11.8%** of companies are Scalers
- **Top sectors:** Hospitality · Education · Arts
- **AG** scales most (18.2%), **KG** least (3.2%)
- **B2C** companies scale less than B2B
""")

if not api_key:
    st.warning("⚠️ Enter your Groq API key in the sidebar.")
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

# ── Build RAG chain (Text Agent) ──────────────────────────────────────────────
@st.cache_resource
def build_rag(_api_key):
    docs = []
    for _, row in df.iterrows():
        content = "\n".join([f"{col}: {row[col]}" for col in df.columns])
        docs.append(Document(page_content=content))

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 8})

    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=_api_key)
    template = """You are a data analyst for Bremen, Germany companies.
Answer using ONLY the context below. Be concise, specific, and data-driven.

Context:
{context}

Question: {question}
Answer:"""
    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n---\n\n".join(doc.page_content for doc in docs)

    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt | llm | StrOutputParser()
    )

rag_chain = build_rag(api_key)

# ── Sidebar stats ─────────────────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.markdown("### 🗂️ Dataset")
st.sidebar.metric("Total Companies", len(df))
if 'Scaler_2024' in df.columns:
    st.sidebar.metric("Scalers 2024", f"{int(df['Scaler_2024'].sum())} ({df['Scaler_2024'].mean():.1%})")
if 'Company_Description' in df.columns:
    st.sidebar.metric("With Agent Data", int(df['Company_Description'].ne('Not found').sum()))


# ══════════════════════════════════════════════════════════════════════════════
# AGENT DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════

def call_groq(system: str, user: str, model: str = "llama-3.3-70b-versatile") -> str:
    response = groq_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        temperature=0.1,
        max_tokens=1024
    )
    return response.choices[0].message.content.strip()


# ── Agent 1: Router ───────────────────────────────────────────────────────────
def router_agent(question: str) -> str:
    system = """You are a router that classifies user questions into exactly one of three categories:
- "text"   → factual questions about specific companies, descriptions, comparisons
- "code"   → questions requiring data aggregation, statistics, counts, averages, filtering
- "visual" → questions asking for charts, graphs, visualizations, trends, distributions

Reply with ONLY one word: text, code, or visual."""
    result = call_groq(system, question, model="llama-3.3-70b-versatile")
    result = result.lower().strip().strip('"').strip("'")
    if result not in ["text", "code", "visual"]:
        return "text"
    return result


# ── Agent 2a: Text Agent (RAG) ────────────────────────────────────────────────
def text_agent(question: str) -> tuple[str, None]:
    answer = rag_chain.invoke(question)
    return answer, None


# ── Agent 2b: Code Agent ──────────────────────────────────────────────────────
def code_agent(question: str) -> tuple[str, None]:
    cols_info = ", ".join(df.columns.tolist())
    sample = df.head(3).to_string()

    system = f"""You are a Python/pandas data analyst.
You have a DataFrame called `df` with these columns: {cols_info}

Sample rows:
{sample}

Write a SHORT pandas code snippet to answer the question.
Rules:
- Use only pandas and numpy (already imported as pd, np)
- Store the final answer in a variable called `result`
- `result` must be a string, number, or DataFrame
- Do NOT import anything
- Do NOT use print()
- Return ONLY the code, no explanation, no markdown fences"""

    code = call_groq(system, question)
    code = re.sub(r"```(?:python)?|```", "", code).strip()

    safe_globals = {"df": df, "pd": pd, "np": np, "result": None}
    try:
        exec(code, safe_globals)
        result = safe_globals.get("result", "No result returned.")
        if isinstance(result, pd.DataFrame):
            answer = result.to_markdown() if len(result) <= 30 else result.head(20).to_markdown() + f"\n\n*...and {len(result)-20} more rows*"
        else:
            answer = str(result)
    except Exception as e:
        answer = f"Code execution error: {e}\n\nGenerated code:\n```python\n{code}\n```"

    return answer, None


# ── Agent 2c: Visual Agent ────────────────────────────────────────────────────
def visual_agent(question: str) -> tuple[str, object]:
    cols_info = ", ".join(df.columns.tolist())

    system = f"""You are a data visualization expert using Plotly.
You have a DataFrame called `df` with columns: {cols_info}

Write Python code to create a plotly figure that answers the question.
Rules:
- Use only pandas (pd), numpy (np), plotly.express (px), plotly.graph_objects (go)
- Store the figure in a variable called `fig`
- Make it visually clear and professional
- Do NOT import anything
- Return ONLY the code, no markdown fences, no explanation"""

    code = call_groq(system, question)
    code = re.sub(r"```(?:python)?|```", "", code).strip()

    safe_globals = {"df": df, "pd": pd, "np": np, "px": px, "go": go, "fig": None}
    try:
        exec(code, safe_globals)
        fig = safe_globals.get("fig")
        if fig is not None:
            return "Here's the chart based on your question:", fig
        else:
            return "Could not generate chart.", None
    except Exception as e:
        return f"Visualization error: {e}", None


# ── Agent 3: Editor Agent ─────────────────────────────────────────────────────
def editor_agent(question: str, raw_answer: str, route: str) -> str:
    system = """You are an editor reviewing an AI analyst's answer.
Your job:
- Fix any grammar or clarity issues
- Make it concise and professional
- If it's a data result, frame it as an insight
- Keep numbers and facts exactly as they are
- Do NOT add new information
- Return only the polished answer, nothing else"""

    user = f"Question: {question}\n\nRaw answer: {raw_answer}"
    return call_groq(system, user)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN PIPELINE
# ══════════════════════════════════════════════════════════════════════════════

def run_pipeline(question: str):
    steps = {}

    # Step 1: Route
    with st.status("🤖 Router Agent — classifying question...", expanded=False):
        route = router_agent(question)
        steps["route"] = route
        st.write(f"Classified as: **{route.upper()}**")

    # Step 2: Specialist agent
    if route == "text":
        with st.status("📝 Text Agent — searching knowledge base...", expanded=False):
            raw_answer, fig = text_agent(question)
    elif route == "code":
        with st.status("💻 Code Agent — running data query...", expanded=False):
            raw_answer, fig = code_agent(question)
    else:
        with st.status("📊 Visual Agent — generating chart...", expanded=False):
            raw_answer, fig = visual_agent(question)

    # Step 3: Editor (skip for visuals to avoid rewriting chart captions)
    if route != "visual":
        with st.status("✏️ Editor Agent — polishing answer...", expanded=False):
            final_answer = editor_agent(question, raw_answer, route)
    else:
        final_answer = raw_answer

    return route, final_answer, fig


# ══════════════════════════════════════════════════════════════════════════════
# UI
# ══════════════════════════════════════════════════════════════════════════════

st.title("🏭 Bremen Companies — Multi-Agent Explorer")
st.caption("5-Agent Workflow · Data-Driven Entrepreneurship · WHU 2025")

tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Dashboard", "🔍 Data Explorer"])

# ── Tab 1: Chat ───────────────────────────────────────────────────────────────
with tab1:
    examples = [
        "Which industries have the highest scaling rate?",
        "Show a chart of scaling rate by legal form",
        "How many B2B companies are there?",
        "Which companies are in logistics?",
        "Show employee growth distribution as a histogram",
    ]

    st.markdown("**💡 Try these:**")
    ecols = st.columns(len(examples))
    for i, q in enumerate(examples):
        if ecols[i].button(q, key=f"ex_{i}"):
            st.session_state.setdefault("messages", [])
            st.session_state["pending_question"] = q

    st.markdown("---")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg.get("fig"):
                st.plotly_chart(msg["fig"], use_container_width=True)
            if msg.get("route"):
                st.caption(f"🔀 Routed to: **{msg['route'].upper()} Agent**")

    # Handle pending question from example buttons
    pending = st.session_state.pop("pending_question", None)
    question = st.chat_input("Ask anything about Bremen companies...") or pending

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            route, answer, fig = run_pipeline(question)
            st.write(answer)
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True)
            st.caption(f"🔀 Routed to: **{route.upper()} Agent**")

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "fig": fig,
            "route": route
        })

# ── Tab 2: Dashboard ──────────────────────────────────────────────────────────
with tab2:
    st.subheader("📊 Bremen Company Analytics")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Companies", len(df))
    if 'Scaler_2024' in df.columns:
        col2.metric("Scalers 2024", f"{int(df['Scaler_2024'].sum())} ({df['Scaler_2024'].mean():.1%})")
    if 'B2B_or_B2C' in df.columns:
        col3.metric("B2B Companies", int((df['B2B_or_B2C'] == 'B2B').sum()))
    if 'Legal_Form' in df.columns:
        col4.metric("GmbH Companies", int((df['Legal_Form'] == 'GmbH').sum()))

    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        if 'Legal_Form' in df.columns and 'Scaler_2024' in df.columns:
            lf = df.groupby('Legal_Form')['Scaler_2024'].agg(['mean','count']).reset_index()
            lf = lf[lf['count'] >= 10].sort_values('mean', ascending=True)
            lf.columns = ['Legal Form', 'Scale Rate', 'Count']
            fig1 = px.bar(lf, x='Scale Rate', y='Legal Form', orientation='h',
                         title='Scaling Rate by Legal Form',
                         color='Scale Rate', color_continuous_scale='Blues',
                         text=lf['Scale Rate'].apply(lambda x: f"{x:.1%}"))
            fig1.update_traces(textposition='outside')
            st.plotly_chart(fig1, use_container_width=True)

    with c2:
        if 'B2B_or_B2C' in df.columns and 'Scaler_2024' in df.columns:
            b2b = df[df['B2B_or_B2C'].isin(['B2B','B2C','Both'])].groupby('B2B_or_B2C')['Scaler_2024'].agg(['mean','count']).reset_index()
            b2b.columns = ['Business Model', 'Scale Rate', 'Count']
            fig2 = px.bar(b2b, x='Business Model', y='Scale Rate',
                         title='Scaling Rate by Business Model',
                         color='Scale Rate', color_continuous_scale='Greens',
                         text=b2b['Scale Rate'].apply(lambda x: f"{x:.1%}"))
            fig2.update_traces(textposition='outside')
            st.plotly_chart(fig2, use_container_width=True)

    if 'NACE_Section' in df.columns and 'Scaler_2024' in df.columns:
        nace_labels = {
            'C': 'C · Manufacturing', 'F': 'F · Construction',
            'G': 'G · Wholesale/Retail', 'H': 'H · Transport',
            'I': 'I · Hospitality', 'J': 'J · ICT',
            'K': 'K · Finance', 'L': 'L · Real Estate',
            'M': 'M · Professional Services', 'N': 'N · Admin Support',
            'P': 'P · Education', 'Q': 'Q · Health',
            'R': 'R · Arts/Recreation', 'S': 'S · Other Services'
        }
        nace = df.groupby('NACE_Section')['Scaler_2024'].agg(['mean','count']).reset_index()
        nace = nace[nace['count'] >= 5].sort_values('mean', ascending=False)
        nace.columns = ['NACE Section', 'Scale Rate', 'Count']
        nace['Label'] = nace['NACE Section'].map(nace_labels).fillna(nace['NACE Section'])
        fig3 = px.bar(nace, x='Label', y='Scale Rate',
                     title='Scaling Rate by Industry Sector (NACE)',
                     color='Scale Rate', color_continuous_scale='Oranges',
                     text=nace['Scale Rate'].apply(lambda x: f"{x:.1%}"),
                     hover_data=['Count'])
        fig3.update_traces(textposition='outside')
        fig3.update_xaxes(tickangle=35)
        st.plotly_chart(fig3, use_container_width=True)

    if 'Company_Age' in df.columns and 'Scaler_2024' in df.columns:
        fig4 = px.box(df[df['Scaler_2024'].isin([0,1])],
                      x=df['Scaler_2024'].map({0:'Non-Scaler', 1:'Scaler'}),
                      y='Company_Age',
                      title='Company Age: Scalers vs Non-Scalers',
                      color=df['Scaler_2024'].map({0:'Non-Scaler', 1:'Scaler'}),
                      color_discrete_map={'Scaler': '#2196F3', 'Non-Scaler': '#E0E0E0'})
        st.plotly_chart(fig4, use_container_width=True)

# ── Tab 3: Data Explorer ──────────────────────────────────────────────────────
with tab3:
    st.subheader("🔍 Filter & Explore Companies")

    c1, c2, c3 = st.columns(3)
    scaler_filter = c1.selectbox("Scaler Status", ["All", "Scaler ✅", "Non-Scaler"])
    legal_opts = sorted(df['Legal_Form'].dropna().unique()) if 'Legal_Form' in df.columns else []
    legal_filter = c2.multiselect("Legal Form", options=legal_opts)
    b2b_opts = ['B2B', 'B2C', 'Both'] if 'B2B_or_B2C' in df.columns else []
    b2b_filter = c3.multiselect("Business Model", options=b2b_opts)

    filtered = df.copy()
    if scaler_filter == "Scaler ✅" and 'Scaler_2024' in df.columns:
        filtered = filtered[filtered['Scaler_2024'] == 1]
    elif scaler_filter == "Non-Scaler" and 'Scaler_2024' in df.columns:
        filtered = filtered[filtered['Scaler_2024'] == 0]
    if legal_filter:
        filtered = filtered[filtered['Legal_Form'].isin(legal_filter)]
    if b2b_filter:
        filtered = filtered[filtered['B2B_or_B2C'].isin(b2b_filter)]

    st.caption(f"Showing **{len(filtered)}** companies")

    display_cols = [
        'Company name Latin alphabet', 'Legal_Form', 'B2B_or_B2C',
        'Industry', 'Scaler_2024', 'Number of employees 2024',
        'Company_Age', 'Company_Description'
    ]
    display_cols = [c for c in display_cols if c in filtered.columns]
    st.dataframe(filtered[display_cols].reset_index(drop=True), use_container_width=True, height=500)

    csv = filtered[display_cols].to_csv(index=False)
    st.download_button("⬇️ Download filtered data", csv, "bremen_filtered.csv", "text/csv")
