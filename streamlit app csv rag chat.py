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

st.set_page_config(page_title="Bremen Companies Chat", layout="wide")
st.title("Bremen Companies — AI Chat")

# --- Sidebar: API Key ---
st.sidebar.header("Configuration")

# Pre-fill from groq.txt if available
default_key = ""
if os.path.exists("groq.txt"):
    with open("groq.txt") as f:
        default_key = f.readline().strip()

api_key = st.sidebar.text_input(
    "Groq API Key",
    value=default_key,
    type="password",
    placeholder="Enter your Groq API key..."
)

st.sidebar.caption("Key is pre-filled from groq.txt")

# --- Load data and build chain only when key is present ---
if not api_key:
    st.warning("Please enter your Groq API key in the sidebar to start.")
    st.stop()

os.environ["GROQ_API_KEY"] = api_key

@st.cache_resource
def build_chain():
    df = pd.read_excel("df_agent_progress.xlsx").fillna("Not found")

    docs = []
    for _, row in df.iterrows():
        content = "\n".join([f"{col}: {row[col]}" for col in df.columns])
        docs.append(Document(page_content=content))

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key)

    template = """Answer the question based only on the following context about Bremen companies:

{context}

Question: {question}
"""
    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain, len(df)

chain, num_companies = build_chain()
st.sidebar.success(f"{num_companies} companies loaded")

# --- Chat interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if question := st.chat_input("Ask anything about Bremen companies..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = chain.invoke(question)
        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
