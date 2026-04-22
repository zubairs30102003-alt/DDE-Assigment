import streamlit as st
import pandas as pd
import os
from groq import Groq
import matplotlib.pyplot as plt
import plotly.express as px

# LangChain imports for RAG
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# =============================================================================
# WHU BRANDING - Custom CSS based on whu_brand_styler
# =============================================================================

# WHU Brand Colors
WHU_BLUE = "#2C4592"
WHU_LIGHT_BLUE = "#808FBE"
WHU_DARK_GRAY = "#515256"
WHU_MEDIUM_GRAY = "#A29795"
WHU_LIGHT_GRAY = "#C7C1BF"
WHU_VERY_LIGHT_GRAY = "#EEEBEA"
WHU_RED = "#E7331A"

st.set_page_config(
    page_title="WHU Fintech Explorer",
    page_icon="🏦",
    layout="wide"
)

# Apply WHU custom styling
st.markdown(f"""
<style>
    /* Import Arial font */
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap');
    
    /* Global font styling */
    html, body, [class*="css"] {{
        font-family: Arial, Helvetica, sans-serif;
    }}
    
    /* Header styling */
    .stApp > header {{
        background-color: {WHU_BLUE};
    }}
    
    /* Main title styling */
    h1 {{
        color: {WHU_BLUE} !important;
        font-family: Arial, Helvetica, sans-serif !important;
        font-weight: bold !important;
    }}
    
    h2, h3 {{
        color: {WHU_BLUE} !important;
        font-family: Arial, Helvetica, sans-serif !important;
    }}
    
    h4, h5, h6 {{
        color: {WHU_DARK_GRAY} !important;
        font-family: Arial, Helvetica, sans-serif !important;
    }}
    
    /* Primary button styling */
    .stButton > button[kind="primary"] {{
        background-color: {WHU_BLUE} !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        font-family: Arial, Helvetica, sans-serif !important;
        font-weight: 600 !important;
    }}
    
    .stButton > button[kind="primary"]:hover {{
        background-color: {WHU_LIGHT_BLUE} !important;
    }}
    
    /* Secondary button styling */
    .stButton > button {{
        border-color: {WHU_BLUE} !important;
        color: {WHU_BLUE} !important;
        font-family: Arial, Helvetica, sans-serif !important;
    }}
    
    /* Info box styling */
    .stAlert {{
        background-color: {WHU_VERY_LIGHT_GRAY} !important;
        border-left-color: {WHU_BLUE} !important;
    }}
    
    /* Success message styling */
    .stSuccess {{
        background-color: {WHU_VERY_LIGHT_GRAY} !important;
        border-left-color: {WHU_BLUE} !important;
    }}
    
    /* Expander styling */
    .streamlit-expanderHeader {{
        color: {WHU_BLUE} !important;
        font-family: Arial, Helvetica, sans-serif !important;
        font-weight: 600 !important;
    }}
    
    /* Text input styling */
    .stTextInput > div > div > input {{
        border-color: {WHU_LIGHT_GRAY} !important;
        font-family: Arial, Helvetica, sans-serif !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {WHU_BLUE} !important;
        box-shadow: 0 0 0 1px {WHU_BLUE} !important;
    }}
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {{
        color: {WHU_BLUE} !important;
        font-family: Arial, Helvetica, sans-serif !important;
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: {WHU_VERY_LIGHT_GRAY} !important;
    }}
    
    /* Link styling */
    a {{
        color: {WHU_RED} !important;
    }}
    
    /* Markdown text */
    .stMarkdown {{
        font-family: Arial, Helvetica, sans-serif !important;
    }}
    
    /* Divider styling */
    hr {{
        border-color: {WHU_LIGHT_GRAY} !important;
    }}
    
    /* Custom header bar */
    .whu-header {{
        background-color: {WHU_BLUE};
        padding: 1rem 2rem;
        margin: -1rem -1rem 1rem -1rem;
        color: white;
    }}
    
    .whu-header h1 {{
        color: white !important;
        margin: 0 !important;
    }}
    
    /* Agent cards */
    .agent-card {{
        background-color: {WHU_VERY_LIGHT_GRAY};
        border-left: 4px solid {WHU_BLUE};
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 4px 4px 0;
    }}
    
    /* Status indicator */
    .status-indicator {{
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }}
    
    .status-active {{
        background-color: {WHU_BLUE};
    }}
    
    .status-complete {{
        background-color: #28a745;
    }}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SETUP
# =============================================================================

# API Key input in sidebar
with st.sidebar:
    st.markdown(f"""
    <h3 style="color: {WHU_BLUE};">🔑 API Configuration</h3>
    """, unsafe_allow_html=True)
    
    groq_api_key = st.text_input(
        "Enter your Groq API Key:",
        type="password",
        placeholder="gsk_...",
        help="Get your free API key at https://console.groq.com/keys"
    )
    
    if groq_api_key:
        st.success("✅ API Key provided")
    else:
        st.warning("⚠️ Please enter your Groq API key to continue")
    
    st.markdown("---")
    st.markdown(f"""
    <p style="font-size: 0.8rem; color: {WHU_DARK_GRAY};">
        <strong>How to get an API key:</strong><br>
        1. Go to <a href="https://console.groq.com/keys" target="_blank">console.groq.com</a><br>
        2. Sign up or log in<br>
        3. Create a new API key<br>
        4. Paste it above
    </p>
    """, unsafe_allow_html=True)

# Check if API key is provided
if not groq_api_key:
    st.info("👈 Please enter your Groq API key in the sidebar to get started.")
    st.stop()

# Set API key
os.environ['GROQ_API_KEY'] = groq_api_key

# Initialize Groq client
client = Groq(api_key=groq_api_key)

# =============================================================================
# LOAD DATA AND SETUP AGENTS
# =============================================================================

@st.cache_resource
def setup_text_analysis_agent():
    """Setup RAG-based text analysis agent (like RAG wit excel.ipynb)"""
    loader = CSVLoader(r'fintechdf_categorized.csv', encoding="latin-1")
    docs = loader.load()
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    
    template = """Answer the question based only on the following context about fintech startups:

{context}

Question: {question}

Provide a detailed and helpful answer based on the context provided.
"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain

@st.cache_data
def setup_coding_agent_context():
    """Setup context for coding agent (like coding_agent.ipynb)"""
    df = pd.read_csv("fintechdf_categorized.csv", encoding="latin-1")
    
    columns_info = df.dtypes.to_string()
    sample_data = df.head(3).to_string()
    shape_info = f"Dataset has {df.shape[0]} rows and {df.shape[1]} columns"
    
    data_context = f"""
You have access to a fintech startup dataset with the following structure:

{shape_info}

Columns and their types:
{columns_info}

Sample data (first 3 rows):
{sample_data}

The dataset contains information about European fintech startups including:
- Basic info: ID, Name, Long description, HQ city, Launch year, Founders
- Funding: Total funding (EUR M), Last round
- Category flags (binary 0/1): digital_payments_processing, insurance_insurtech_underwriting, 
  blockchain_cryptocurrency_assets, lending_credit_financing, investment_wealth_trading,
  corporate_treasury_accounting, sustainability_carbon_climate, tax_legal_planning, mergers_acquisitions_advisory

When asked a question, generate Python pandas code that operates on the dataframe 'df' to answer it.
Return ONLY the executable Python code, no explanations. The code should end with storing the result in a variable called 'result'.
"""
    return data_context, df

@st.cache_data
def setup_visual_agent_context():
    """Setup context for visual agent (like visual_agent.ipynb)"""
    df = pd.read_csv("fintechdf_categorized.csv", encoding="latin-1")
    
    columns_info = df.dtypes.to_string()
    sample_data = df.head(3).to_string()
    shape_info = f"Dataset has {df.shape[0]} rows and {df.shape[1]} columns"
    
    visual_context = f"""
You are a data visualization expert. You have access to a fintech startup dataset loaded in a pandas DataFrame called 'df'.

{shape_info}

Columns and their types:
{columns_info}

Sample data (first 3 rows):
{sample_data}

The dataset contains information about European fintech startups including:
- Basic info: ID, Name, Long description, HQ city, Launch year, Founders
- Funding: Total funding (EUR M), Last round
- Category flags (binary 0/1): digital_payments_processing, insurance_insurtech_underwriting, 
  blockchain_cryptocurrency_assets, lending_credit_financing, investment_wealth_trading,
  corporate_treasury_accounting, sustainability_carbon_climate, tax_legal_planning, mergers_acquisitions_advisory

When asked to create a visualization, generate Python code that:
1. Uses plotly.express (imported as px) for interactive charts
2. Operates on the dataframe 'df'
3. Creates the requested chart with proper labels, titles, and formatting
4. Stores the figure in a variable called 'fig'

Return ONLY the executable Python code, no explanations.
"""
    return visual_context, df

# =============================================================================
# AGENT FUNCTIONS
# =============================================================================

def router_agent(question: str) -> str:
    """
    Router Agent: Analyzes the question and determines the best approach.
    Returns: 'text' for text analysis or 'code' for coding approach
    """
    router_prompt = """You are a routing agent that analyzes questions about a fintech startup dataset.

Your task is to determine the BEST approach to answer each question:

1. Use 'text' when the question:
   - Asks for qualitative descriptions or explanations
   - Seeks information about specific companies or founders
   - Requires understanding context, descriptions, or narrative information
   - Asks "who", "which company", "describe", "tell me about", "recommend"
   - Needs semantic understanding of text content

2. Use 'code' when the question:
   - Asks for quantitative analysis (averages, counts, sums, statistics)
   - Requires calculations, aggregations, or numerical comparisons
   - Asks "how many", "what is the average", "total", "percentage", "top N", "compare numbers"
   - Needs filtering and counting based on specific criteria
   - Involves mathematical operations on the data

3. Use 'visual' when the question:
   - Asks for a chart, graph, plot, or visualization
   - Uses words like "show me", "visualize", "plot", "chart", "graph", "pie chart", "bar chart", "histogram", "scatter plot"
   - Requests to see data distribution or trends visually
   - Asks for a visual representation of the data

Question: {question}

Respond with ONLY ONE WORD: either 'text', 'code', or 'visual'
"""
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": router_prompt.format(question=question)}
        ],
        temperature=0.1,
        max_tokens=10,
    )
    
    response = completion.choices[0].message.content.strip().lower()
    
    # Ensure we get a valid response
    if 'visual' in response:
        return 'visual'
    elif 'code' in response:
        return 'code'
    else:
        return 'text'

def text_analysis_agent(question: str, rag_chain) -> str:
    """
    Text Analysis Agent: Uses RAG to answer qualitative questions.
    Based on RAG wit excel.ipynb approach.
    """
    result = rag_chain.invoke(question)
    return result

def coding_agent(question: str, data_context: str, df: pd.DataFrame) -> tuple:
    """
    Coding Agent: Generates and executes pandas code for quantitative analysis.
    Based on coding_agent.ipynb approach.
    Returns: (result, generated_code)
    """
    # Generate code
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": data_context},
            {"role": "user", "content": question}
        ],
        temperature=0.1,
        max_tokens=1024,
    )
    
    generated_code = completion.choices[0].message.content
    
    # Clean the generated code
    code_to_run = generated_code
    if "```python" in code_to_run:
        code_to_run = code_to_run.split("```python")[1].split("```")[0]
    elif "```" in code_to_run:
        code_to_run = code_to_run.split("```")[1].split("```")[0]
    
    # Execute the code
    try:
        # Create a local namespace with df
        local_vars = {'df': df, 'pd': pd}
        exec(code_to_run, {}, local_vars)
        
        # Try to get result from local vars or capture printed output
        result = local_vars.get('result', 'Code executed successfully')
        
        # If no result variable, try to capture the last expression
        if result == 'Code executed successfully':
            import io
            import sys
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            exec(code_to_run, {'df': df, 'pd': pd})
            result = buffer.getvalue()
            sys.stdout = old_stdout
            
    except Exception as e:
        result = f"Error executing code: {str(e)}"
    
    return result, code_to_run

def visual_agent(question: str, visual_context: str, df: pd.DataFrame) -> tuple:
    """
    Visual Agent: Generates and executes visualization code.
    Based on visual_agent.ipynb approach.
    Returns: (fig, generated_code)
    """
    # Generate visualization code
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": visual_context},
            {"role": "user", "content": question}
        ],
        temperature=0.1,
        max_tokens=1024,
    )
    
    generated_code = completion.choices[0].message.content
    
    # Clean the generated code
    code_to_run = generated_code
    if "```python" in code_to_run:
        code_to_run = code_to_run.split("```python")[1].split("```")[0]
    elif "```" in code_to_run:
        code_to_run = code_to_run.split("```")[1].split("```")[0]
    
    # Execute the visualization code
    try:
        local_vars = {'df': df, 'pd': pd, 'px': px, 'plt': plt}
        exec(code_to_run, {}, local_vars)
        fig = local_vars.get('fig', None)
    except Exception as e:
        fig = None
        code_to_run = f"Error generating visualization: {str(e)}\n\nGenerated code:\n{code_to_run}"
    
    return fig, code_to_run

def editor_agent(question: str, answer: str, approach: str) -> str:
    """
    Editor Agent: Evaluates and refines the answer before presenting to user.
    """
    editor_prompt = """You are an editor agent that reviews and improves answers about fintech startups.

Original Question: {question}

Approach Used: {approach}

Draft Answer:
{answer}

Your task:
1. Evaluate if the answer properly addresses the question
2. Improve clarity and readability
3. Add any helpful context or formatting
4. Ensure the answer is professional and well-structured
5. If the answer contains errors or seems incomplete, note that

Provide the final polished answer:"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful editor that improves and polishes answers."},
            {"role": "user", "content": editor_prompt.format(
                question=question,
                approach=approach,
                answer=answer
            )}
        ],
        temperature=0.3,
        max_tokens=2048,
    )
    
    return completion.choices[0].message.content

# =============================================================================
# STREAMLIT APP
# =============================================================================

# WHU Header
st.markdown(f"""
<div style="background-color: {WHU_BLUE}; padding: 1.5rem 2rem; margin: -1rem -1rem 2rem -1rem; border-radius: 0; text-align: center;">
    <h1 style="color: white !important; margin: 0; font-size: 2.5rem;">WHU Fintech Explorer</h1>
    <p style="color: {WHU_LIGHT_BLUE}; margin: 0.5rem 0 0 0; font-size: 1.1rem;">Explore European Fintech Startups with AI-Powered Analysis</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
This application uses a team of AI agents to answer questions about European fintech startups.
""")

# Agent cards
st.markdown(f"""
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 1rem 0;">
    <div style="background: {WHU_VERY_LIGHT_GRAY}; border-left: 4px solid {WHU_BLUE}; padding: 1rem; border-radius: 0 4px 4px 0;">
        <strong style="color: {WHU_BLUE};">🔄 Router Agent</strong><br>
        <span style="color: {WHU_DARK_GRAY}; font-size: 0.9rem;">Analyzes your question</span>
    </div>
    <div style="background: {WHU_VERY_LIGHT_GRAY}; border-left: 4px solid {WHU_BLUE}; padding: 1rem; border-radius: 0 4px 4px 0;">
        <strong style="color: {WHU_BLUE};">📝 Text Agent</strong><br>
        <span style="color: {WHU_DARK_GRAY}; font-size: 0.9rem;">RAG for qualitative Q&A</span>
    </div>
    <div style="background: {WHU_VERY_LIGHT_GRAY}; border-left: 4px solid {WHU_BLUE}; padding: 1rem; border-radius: 0 4px 4px 0;">
        <strong style="color: {WHU_BLUE};">💻 Coding Agent</strong><br>
        <span style="color: {WHU_DARK_GRAY}; font-size: 0.9rem;">Pandas for quantitative analysis</span>
    </div>
    <div style="background: {WHU_VERY_LIGHT_GRAY}; border-left: 4px solid {WHU_BLUE}; padding: 1rem; border-radius: 0 4px 4px 0;">
        <strong style="color: {WHU_BLUE};">📊 Visual Agent</strong><br>
        <span style="color: {WHU_DARK_GRAY}; font-size: 0.9rem;">Charts & visualizations</span>
    </div>
    <div style="background: {WHU_VERY_LIGHT_GRAY}; border-left: 4px solid {WHU_BLUE}; padding: 1rem; border-radius: 0 4px 4px 0;">
        <strong style="color: {WHU_BLUE};">✏️ Editor Agent</strong><br>
        <span style="color: {WHU_DARK_GRAY}; font-size: 0.9rem;">Reviews & polishes answers</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize agents
with st.spinner("Setting up agents..."):
    rag_chain = setup_text_analysis_agent()
    data_context, df = setup_coding_agent_context()
    visual_context, _ = setup_visual_agent_context()

st.success("✅ All agents ready!")

# Show dataset info
with st.expander("📊 Dataset Overview"):
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.metric("Total Startups", df.shape[0])
    with col_info2:
        st.metric("Data Fields", df.shape[1])
    st.dataframe(df.head(), use_container_width=True)

# Example questions with WHU styling
st.markdown(f"""
<h3 style="color: {WHU_BLUE}; border-bottom: 2px solid {WHU_BLUE}; padding-bottom: 0.5rem; margin-top: 2rem;">
    💡 Example Questions
</h3>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div style="background: white; border: 1px solid {WHU_LIGHT_GRAY}; border-top: 3px solid {WHU_BLUE}; padding: 1rem; border-radius: 4px; height: 150px;">
        <strong style="color: {WHU_BLUE};">📝 Text Analysis</strong>
        <ul style="color: {WHU_DARK_GRAY}; font-size: 0.85rem; margin-top: 0.5rem; padding-left: 1.2rem;">
            <li>Who could be a good co-founder for a payments startup?</li>
            <li>Tell me about blockchain companies in Berlin</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div style="background: white; border: 1px solid {WHU_LIGHT_GRAY}; border-top: 3px solid {WHU_BLUE}; padding: 1rem; border-radius: 4px; height: 150px;">
        <strong style="color: {WHU_BLUE};">💻 Coding Analysis</strong>
        <ul style="color: {WHU_DARK_GRAY}; font-size: 0.85rem; margin-top: 0.5rem; padding-left: 1.2rem;">
            <li>What is the average funding raised?</li>
            <li>How many startups are in each category?</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div style="background: white; border: 1px solid {WHU_LIGHT_GRAY}; border-top: 3px solid {WHU_BLUE}; padding: 1rem; border-radius: 4px; height: 150px;">
        <strong style="color: {WHU_BLUE};">📊 Visual Analysis</strong>
        <ul style="color: {WHU_DARK_GRAY}; font-size: 0.85rem; margin-top: 0.5rem; padding-left: 1.2rem;">
            <li>Show me a pie chart of fintech categories</li>
            <li>Create a bar chart of top 10 cities</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# User input section with WHU styling
st.markdown(f"""
<div style="background: {WHU_VERY_LIGHT_GRAY}; padding: 1.5rem; border-radius: 8px; margin: 2rem 0 1rem 0;">
    <h4 style="color: {WHU_BLUE}; margin: 0 0 0.5rem 0;">🔍 Ask Your Question</h4>
</div>
""", unsafe_allow_html=True)

question = st.text_input("Enter your question about the fintech dataset:", label_visibility="collapsed", placeholder="e.g., What is the average funding raised by blockchain startups?")

if st.button("Get Answer", type="primary") and question:
    
    # Step 1: Router Agent
    with st.spinner("🔄 Router Agent analyzing question..."):
        approach = router_agent(question)
    
    st.info(f"**Router Decision:** Using **{approach.upper()}** approach")
    
    # Step 2: Execute appropriate agent
    fig = None
    if approach == 'text':
        with st.spinner("📝 Text Analysis Agent processing..."):
            raw_answer = text_analysis_agent(question, rag_chain)
            code_used = None
    elif approach == 'visual':
        with st.spinner("📊 Visual Agent generating visualization..."):
            fig, code_used = visual_agent(question, visual_context, df)
            raw_answer = "Visualization generated successfully" if fig else code_used
    else:
        with st.spinner("💻 Coding Agent generating and executing code..."):
            raw_answer, code_used = coding_agent(question, data_context, df)
    
    # Show intermediate result
    with st.expander("🔍 Raw Agent Output"):
        if fig:
            st.write("Visualization generated")
        else:
            st.write(raw_answer)
        if code_used:
            st.markdown("**Generated Code:**")
            st.code(code_used, language="python")
    
    # Step 3: Editor Agent (skip for visuals)
    if approach != 'visual':
        with st.spinner("✏️ Editor Agent reviewing answer..."):
            final_answer = editor_agent(question, str(raw_answer), approach)
    else:
        final_answer = "Here is your requested visualization:"
    
    # Display final answer with WHU styling
    st.markdown(f"""
    <div style="background: white; border: 2px solid {WHU_BLUE}; border-radius: 8px; padding: 1.5rem; margin-top: 1.5rem;">
        <h3 style="color: {WHU_BLUE}; margin: 0 0 1rem 0; border-bottom: 1px solid {WHU_LIGHT_GRAY}; padding-bottom: 0.5rem;">
            📋 Final Answer
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    st.markdown(final_answer)
    
    # Show agent workflow with WHU styling
    with st.expander("🔧 Agent Workflow Summary"):
        agent_names = {
            'text': 'Text Analysis Agent (RAG)',
            'code': 'Coding Agent (Pandas)',
            'visual': 'Visual Agent (Plotly)'
        }
        st.markdown(f"""
        <div style="background: {WHU_VERY_LIGHT_GRAY}; padding: 1rem; border-radius: 4px;">
            <p><strong style="color: {WHU_BLUE};">1. Question Received:</strong> {question}</p>
            <p><strong style="color: {WHU_BLUE};">2. Router Decision:</strong> {approach.upper()} approach</p>
            <p><strong style="color: {WHU_BLUE};">3. Agent Used:</strong> {agent_names.get(approach, 'Unknown Agent')}</p>
            <p><strong style="color: {WHU_BLUE};">4. Editor Agent:</strong> {'Skipped (visualization)' if approach == 'visual' else 'Reviewed and polished'}</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div style="background: {WHU_BLUE}; padding: 1rem 2rem; margin: 3rem -1rem -1rem -1rem; text-align: center;">
    <p style="color: white; margin: 0; font-size: 0.9rem;">
        WHU Fintech Explorer | WHU Otto Beisheim School of Management
    </p>
</div>
""", unsafe_allow_html=True)
