import streamlit as st
import os
import requests
from pathlib import Path

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="AI Onboarding Buddy",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Onboarding Buddy")
st.markdown("Ask questions about company documentation powered by Ollama")

# ============================================
# CHECK SYSTEM
# ============================================
def check_ollama():
    """Check if Ollama is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            return True, response.json().get('models', [])
    except:
        pass
    return False, []

# Check system status
is_running, models = check_ollama()

if not is_running:
    st.error("❌ Ollama is not running!")
    st.info("Please start Ollama first, then refresh this page")
    st.stop()

st.success(f"✓ Ollama is running")
if models:
    model_names = [m.get('name', 'Unknown') for m in models]
    st.info(f"✓ Available models: {', '.join(model_names[:3])}")

# ============================================
# LOAD DOCUMENTS
# ============================================
@st.cache_resource
def load_all_documents():
    """Load all documents from ProjectDetails folder"""
    docs_folder = Path("ProjectDetails")
    if not docs_folder.exists():
        return []
    
    documents = []
    
    # Load text files
    for txt_file in docs_folder.glob("*.txt"):
        try:
            with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                documents.append({
                    "name": txt_file.name,
                    "content": content
                })
        except:
            pass
    
    # Load PDF files
    for pdf_file in docs_folder.glob("*.pdf"):
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            if text.strip():
                documents.append({
                    "name": pdf_file.name,
                    "content": text
                })
        except:
            pass
    
    # Load Word documents
    for docx_file in docs_folder.glob("*.docx"):
        try:
            from docx import Document as DocxDocument
            doc = DocxDocument(docx_file)
            text = "\n".join([p.text for p in doc.paragraphs])
            if text.strip():
                documents.append({
                    "name": docx_file.name,
                    "content": text
                })
        except:
            pass
    
    return documents

# Load documents
documents = load_all_documents()

if not documents:
    st.warning("⚠️ No documents found in ProjectDetails/ folder")
    st.info("Please add PDF, TXT, or DOCX files to get started")
    st.stop()

st.markdown(f"---\n✓ Loaded {len(documents)} documents")

# ============================================
# SEARCH FUNCTIONALITY
# ============================================
def simple_search(query, documents, num_results=3):
    """Simple text-based search (no embeddings needed)"""
    query_lower = query.lower()
    query_words = set(query_lower.split())
    
    results = []
    for doc in documents:
        content_lower = doc["content"].lower()
        
        # Count matching words
        matches = sum(1 for word in query_words if word in content_lower)
        
        if matches > 0:
            # Extract a relevant snippet
            lines = doc["content"].split('\n')
            relevant_lines = [l for l in lines if any(word in l.lower() for word in query_words)]
            snippet = ' '.join(relevant_lines[:3])[:300]
            
            results.append({
                "file": doc["name"],
                "snippet": snippet,
                "score": matches,
                "full_content": doc["content"]
            })
    
    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:num_results]

# ============================================
# CHAT INTERFACE
# ============================================
st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask me about your documentation...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Search for relevant documents
    search_results = simple_search(user_input, documents)
    
    if not search_results:
        response = "I couldn't find relevant information in the documentation. Please try rephrasing your question or ask about something else."
        sources_text = ""
    else:
        # Prepare context
        context = "\n\n".join([
            f"From {r['file']}:\n{r['snippet']}"
            for r in search_results
        ])
        
        # Try to use Ollama to generate answer
        try:
            with st.spinner("🤔 Thinking..."):
                prompt = f"""Based on the following documentation excerpts, answer the user's question.

Documentation:
{context}

Question: {user_input}

Answer only based on the provided documentation. If the answer is not in the documentation, say so."""

                ollama_response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "gemma3:1b",
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=30
                )
                
                if ollama_response.status_code == 200:
                    response = ollama_response.json().get("response", "No response generated").strip()
                else:
                    response = f"Here's what I found in your documentation:\n\n{context}"
                    
        except Exception as e:
            response = f"Here's what I found in your documentation:\n\n{context}"
        
        # Add sources
        sources = "\n".join([f"- 📄 {r['file']}" for r in search_results])
        sources_text = f"\n\n**📎 Sources:**\n{sources}"
    
    # Display assistant message
    full_response = response + sources_text if sources_text else response
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    with st.chat_message("assistant"):
        st.markdown(full_response)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.caption("AI Onboarding Buddy powered by Ollama • All data stays local")