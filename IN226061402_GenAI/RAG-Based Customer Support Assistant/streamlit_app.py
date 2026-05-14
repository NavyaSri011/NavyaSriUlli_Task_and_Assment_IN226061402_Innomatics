import tempfile
import streamlit as st

from langchain_classic.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Customer Support Assistant",
    page_icon="🤖",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

.stApp {
    background-color: #0f172a;
    color: white;
}

h1, h2, h3 {
    color: #38bdf8;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

.stChatMessage {
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =========================
# SIDEBAR
# =========================
with st.sidebar:

    st.title("🤖 AI Assistant")

    st.markdown("""
    ### Features

    ✅ Dynamic PDF Upload  
    ✅ AI Chatbot  
    ✅ Chat History  
    ✅ ChromaDB Vector Store  
    ✅ LM Studio Integration  
    ✅ Qwen 2.5 Support  
    """)

    st.markdown("---")

    # Clear Chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")

    # Chat History
    st.subheader("🕘 Chat History")

    if len(st.session_state.chat_history) == 0:
        st.write("No chats yet")

    else:
        for i, chat in enumerate(
            st.session_state.chat_history[-10:], 1
        ):
            st.write(f"{i}. {chat}")

# =========================
# MAIN TITLE
# =========================
st.title("🚀 AI-Powered Enterprise Knowledge Assistant")

st.write("Ask questions from your uploaded PDF")

# =========================
# PDF UPLOAD
# =========================
uploaded_file = st.file_uploader(
    "Upload a PDF",
    type="pdf"
)

# =========================
# PROCESS PDF
# =========================
if uploaded_file is not None:

    with st.spinner("Processing PDF..."):

        # Save uploaded PDF temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp_file:

            tmp_file.write(uploaded_file.read())

            temp_pdf_path = tmp_file.name

        # =========================
        # LOAD PDF
        # =========================
        loader = PyPDFLoader(temp_pdf_path)

        documents = loader.load()

        # =========================
        # SPLIT TEXT
        # =========================
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = text_splitter.split_documents(documents)

        # =========================
        # EMBEDDINGS
        # =========================
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # =========================
        # CREATE CHROMADB
        # =========================
        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings
        )

        retriever = vectordb.as_retriever(
            search_kwargs={"k": 3}
        )

        # =========================
        # LM STUDIO MODEL
        # =========================
        llm = ChatOpenAI(
            base_url="http://localhost:1234/v1",
            api_key="lm-studio",
            model="qwen2.5",
            temperature=0.3
        )

        # =========================
        # QA CHAIN
        # =========================
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever
        )

    st.success("✅ PDF Processed Successfully!")

    # =========================
    # DISPLAY OLD MESSAGES
    # =========================
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # =========================
    # CHAT INPUT
    # =========================
    user_query = st.chat_input(
        "Ask a question from the uploaded PDF"
    )

    # =========================
    # HANDLE USER QUERY
    # =========================
    if user_query:

        # Save User Message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_query
            }
        )

        # Save Chat History
        st.session_state.chat_history.append(user_query)

        # Display User Message
        with st.chat_message("user"):
            st.markdown(user_query)

        # Generate Response
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:
                    response = qa_chain.run(user_query)

                except Exception as e:
                    response = f"Error: {str(e)}"

                st.markdown(response)

        # Save Assistant Response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

else:

    st.info("📄 Please upload a PDF to begin.")