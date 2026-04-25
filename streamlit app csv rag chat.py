import streamlit as st
import os
import pandas as pd
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(page_title="Bremen Companies Explorer", layout="wide", page_icon="📊")

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("⚙️ Configuration")

try:
    default_key = st.secrets.get("GROQ_API_KEY", "")
except Exception:
    default_key = ""

key_source = "Streamlit secrets"
if not default_key and os.path.exists("groq.txt"):
    with open("groq.txt") as f:
        default_key = f.readline().strip()
    key_source = "groq.txt"

api_key = st.sidebar.text_input(
    "Groq API Key", value=default_key, type="password",
    placeholder="Enter your Groq API key..."
)
if default_key:
    st.sidebar.caption(f"Pre-filled from {key_source}")
else:
    st.sidebar.caption("Enter a key here or set GROQ_API_KEY in Streamlit secrets.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Key Findings")
st.sidebar.markdown("""
- **11.8%** of companies are Scalers
- **Top scaling sectors:** Hospitality (I), Education (P), Arts (R)
- **AG** legal form scales most (18.2%)
- **B2C** companies scale less (6.7% vs 12.2% B2B)
- **KG** legal form least likely to scale (3.2%)
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗂️ Dataset")

if not api_key:
    st.warning("⚠️ Please enter your Groq API key in the sidebar to start chatting.")
    st.stop()

os.environ["GROQ_API_KEY"] = api_key

# ── Load Data ─────────────────────────────────────────────────────────────────
def load_company_data():
    if os.path.exists("bremen_merged_final.csv"):
        return pd.read_csv("bremen_merged_final.csv").fillna("Not found")
    return pd.read_excel("df_agent_progress.xlsx", engine="openpyxl").fillna("Not found")

@st.cache_resource
def build_chain(api_key):
    df = load_company_data()

    docs = []
    for _, row in df.iterrows():
        content = "\n".join([f"{col}: {row[col]}" for col in df.columns])
        docs.append(Document(page_content=content))

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 8})

    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key)

    template = """You are an analyst for Bremen, Germany company data.
Answer questions using ONLY the context below. Be concise and specific.
If asked about statistics or findings, refer to actual numbers from the data.

Context:
{context}

Question: {question}

Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n---\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain, df

chain, df = build_chain(api_key)

# ── Sidebar stats ─────────────────────────────────────────────────────────────
st.sidebar.metric("Total Companies", len(df))
st.sidebar.metric("Scalers 2024", int(df['Scaler_2024'].sum()) if 'Scaler_2024' in df.columns else "—")
st.sidebar.metric("With Agent Data", int(df['Company_Description'].ne('Not found').sum()))

# ── Main UI ───────────────────────────────────────────────────────────────────
st.title("🏭 Bremen Companies — AI Explorer")
st.caption("Chat with the Bremen dataset · Data-Driven Entrepreneurship · WHU 2025")

# Tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Dashboard", "🔍 Data Explorer"])

# ── Tab 1: Chat ───────────────────────────────────────────────────────────────
with tab1:
    st.markdown("Ask anything about the Bremen companies — scaling factors, industries, legal forms, etc.")

    example_questions = [
        "Which industries have the highest scaling rate?",
        "What legal forms are most common among scalers?",
        "Are B2B or B2C companies more likely to scale?",
        "Tell me about the logistics companies in Bremen",
        "Which companies are in the technology sector?",
    ]

    st.markdown("**💡 Example questions:**")
    cols = st.columns(len(example_questions))
    for i, q in enumerate(example_questions):
        if cols[i].button(q, key=f"ex_{i}"):
            st.session_state.setdefault("messages", [])
            st.session_state.messages.append({"role": "user", "content": q})

    st.markdown("---")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if question := st.chat_input("Ask about Bremen companies..."):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching data..."):
                answer = chain.invoke(question)
            st.write(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

# ── Tab 2: Dashboard ──────────────────────────────────────────────────────────
with tab2:
    import plotly.express as px

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Companies", len(df))
    col2.metric("Scalers", f"{int(df['Scaler_2024'].sum())} ({df['Scaler_2024'].mean():.1%})" if 'Scaler_2024' in df.columns else "—")
    col3.metric("B2B Companies", int((df['B2B_or_B2C'] == 'B2B').sum()) if 'B2B_or_B2C' in df.columns else "—")
    col4.metric("GmbH Companies", int((df['Legal_Form'] == 'GmbH').sum()) if 'Legal_Form' in df.columns else "—")

    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        if 'Legal_Form' in df.columns and 'Scaler_2024' in df.columns:
            lf = df.groupby('Legal_Form')['Scaler_2024'].agg(['mean','count']).reset_index()
            lf = lf[lf['count'] >= 10].sort_values('mean', ascending=True)
            lf.columns = ['Legal Form', 'Scale Rate', 'Count']
            fig = px.bar(lf, x='Scale Rate', y='Legal Form', orientation='h',
                        title='Scaling Rate by Legal Form',
                        color='Scale Rate', color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        if 'B2B_or_B2C' in df.columns and 'Scaler_2024' in df.columns:
            b2b = df.groupby('B2B_or_B2C')['Scaler_2024'].agg(['mean','count']).reset_index()
            b2b.columns = ['Business Model', 'Scale Rate', 'Count']
            fig2 = px.bar(b2b, x='Business Model', y='Scale Rate',
                         title='Scaling Rate by Business Model',
                         color='Scale Rate', color_continuous_scale='Greens')
            st.plotly_chart(fig2, use_container_width=True)

    if 'NACE_Section' in df.columns and 'Scaler_2024' in df.columns:
        nace = df.groupby('NACE_Section')['Scaler_2024'].agg(['mean','count']).reset_index()
        nace = nace[nace['count'] >= 5].sort_values('mean', ascending=False)
        nace.columns = ['NACE Section', 'Scale Rate', 'Count']
        nace_labels = {
            'C': 'C - Manufacturing', 'F': 'F - Construction', 'G': 'G - Wholesale/Retail',
            'H': 'H - Transport', 'I': 'I - Hospitality', 'J': 'J - ICT',
            'K': 'K - Finance', 'L': 'L - Real Estate', 'M': 'M - Professional Services',
            'N': 'N - Admin Support', 'P': 'P - Education', 'Q': 'Q - Health',
            'R': 'R - Arts/Recreation', 'S': 'S - Other Services'
        }
        nace['Label'] = nace['NACE Section'].map(nace_labels).fillna(nace['NACE Section'])
        fig3 = px.bar(nace, x='Label', y='Scale Rate',
                     title='Scaling Rate by Industry Sector (NACE)',
                     color='Scale Rate', color_continuous_scale='Oranges')
        fig3.update_xaxes(tickangle=30)
        st.plotly_chart(fig3, use_container_width=True)

# ── Tab 3: Data Explorer ──────────────────────────────────────────────────────
with tab3:
    st.markdown("### Filter & Explore Companies")

    c1, c2, c3 = st.columns(3)
    scaler_filter = c1.selectbox("Scaler 2024", ["All", "Scaler", "Non-Scaler"])
    legal_filter = c2.multiselect("Legal Form", options=sorted(df['Legal_Form'].dropna().unique()) if 'Legal_Form' in df.columns else [])
    b2b_filter = c3.multiselect("B2B / B2C", options=sorted(df['B2B_or_B2C'].dropna().unique()) if 'B2B_or_B2C' in df.columns else [])

    filtered = df.copy()
    if scaler_filter == "Scaler" and 'Scaler_2024' in df.columns:
        filtered = filtered[filtered['Scaler_2024'] == 1]
    elif scaler_filter == "Non-Scaler" and 'Scaler_2024' in df.columns:
        filtered = filtered[filtered['Scaler_2024'] == 0]
    if legal_filter:
        filtered = filtered[filtered['Legal_Form'].isin(legal_filter)]
    if b2b_filter:
        filtered = filtered[filtered['B2B_or_B2C'].isin(b2b_filter)]

    st.caption(f"Showing {len(filtered)} companies")

    display_cols = ['Company name Latin alphabet', 'Legal_Form', 'B2B_or_B2C',
                    'Industry', 'Scaler_2024', 'Number of employees 2024', 'Company_Description']
    display_cols = [c for c in display_cols if c in filtered.columns]
    st.dataframe(filtered[display_cols].reset_index(drop=True), use_container_width=True)
