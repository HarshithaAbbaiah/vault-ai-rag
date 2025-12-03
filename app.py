import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv


try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")


llm = ChatGroq(model_name="llama-3.3-70b-versatile", api_key=api_key)

st.set_page_config(page_title="VaultAI | Secure Enterprise RAG", page_icon="🔒", layout="wide")
st.title("🔒 VaultAI")
st.caption("Secure. Private. Local. | Powered by Llama 3.3 & Groq")

# Session State to keep the "Brain" alive
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

with st.sidebar:
    st.header("Knowledge Base")
    # Accept Multiple Files
    uploaded_files = st.file_uploader("Upload Company Documents", type="pdf", accept_multiple_files=True)
    
    if uploaded_files and st.button("Ingest Knowledge"):
        with st.spinner("Reading & Indexing..."):
            all_documents = []
            
            #  Loop through all uploaded files
            for uploaded_file in uploaded_files:
                temp_path = f"./temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Load each file
                loader = PyPDFLoader(temp_path)
                docs = loader.load()
                all_documents.extend(docs) # Add to the pile
                os.remove(temp_path)

            # Split everything into chunks
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            final_docs = splitter.split_documents(all_documents)
            
            # Create one giant Vector Database
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            st.session_state.vector_store = FAISS.from_documents(final_docs, embeddings)
            
            st.success(f"Brain Updated! {len(final_docs)} chunks indexed.")

# Chat Interface
question = st.text_input("Ask a question across all documents:")

if question:
    if st.session_state.vector_store:
        # Use the smart Llama 3.3 model
        llm = ChatGroq(model_name="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
        
        prompt = ChatPromptTemplate.from_template(
            """
            You are a corporate assistant. Answer the question based ONLY on the provided context.
            If the answer is not in the context, say "I don't find that information in the internal documents."
            
            <context>
            {context}
            </context>
            
            Question: {input}
            """
        )
        
        chain = create_retrieval_chain(
            st.session_state.vector_store.as_retriever(),
            create_stuff_documents_chain(llm, prompt)
        )
        
        response = chain.invoke({"input": question})
        st.write(response["answer"])
        
        # Show which document the answer came from
        with st.expander("View Sources"):
            for doc in response["context"]:
                st.write(f"📄 Source: {doc.metadata['source']}")
                st.write(doc.page_content)
                st.write("---")
    else:
        st.warning("Please upload documents to build the brain.")