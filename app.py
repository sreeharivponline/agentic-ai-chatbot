# app.py

import streamlit as st
import os
import time # For simulating thinking time
from dotenv import load_dotenv
load_dotenv()
from agent import Agent
from tools.report_tool import generate_report # For displaying the agent's internal report

st.set_page_config(page_title="🧠 Agentic Chatbot", layout="centered")
st.title("🧠 Agentic Chatbot with PDF + Web + Memory")

# --- Initialization ---
# Initialize Agent and memory history on first run or if session state is cleared
if "agent" not in st.session_state:
    st.session_state.agent = Agent()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] # Stores (query, answer, sources) tuples
# --- FIX START ---
if "last_uploaded_file_id" not in st.session_state:
    st.session_state.last_uploaded_file_id = None # Initialize to None or an empty string
# --- FIX END ---

# Ensure GROQ_API_KEY is set
if not os.getenv("GROQ_API_KEY"):
    st.warning("🚨 GROQ_API_KEY environment variable not set. Please set it to use the chatbot.")
    st.stop() # Stop the app if API key is missing

# --- PDF Upload Section ---
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

# Condition to load PDF only if a new file is uploaded or if no file was loaded before
if uploaded_file and (st.session_state.last_uploaded_file_id is None or st.session_state.last_uploaded_file_id != uploaded_file.file_id):
    # Save the file to a temporary location
    temp_pdf_path = "document.pdf"
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_file.read())
    
    # Store file_id to prevent re-uploading the same file on subsequent runs
    st.session_state.last_uploaded_file_id = uploaded_file.file_id

    with st.spinner(f"Loading '{uploaded_file.name}' into memory..."):
        try:
            st.session_state.agent.load_pdf(temp_pdf_path)
            st.success(f"✅ PDF '{uploaded_file.name}' loaded into memory!")
            # Optional: Clean up the temporary file if you want to
            # os.remove(temp_pdf_path) # Be cautious with this if agent needs to re-read
        except Exception as e:
            st.error(f"❌ Failed to load PDF: {e}")
            # If loading fails, clear the last_uploaded_file_id so user can retry
            st.session_state.last_uploaded_file_id = None 
    st.rerun() # Rerun to update the state and display success/error message

# ... (rest of your app.py code remains the same) ...

# Display full chat history in a continuous manner
for i, (q, a, s) in enumerate(st.session_state.chat_history):
    with st.chat_message("user"):
        st.write(q)
    with st.chat_message("assistant"):
        st.write(a)
        if s:
            st.markdown("**Sources:**")
            for src in s:
                st.markdown(f"- {src}")

query = st.chat_input("Ask a question (e.g., 'What is X?', 'web search for: Y'):")
if query:
    st.session_state.chat_history.append((query, "Thinking...", None)) 

    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            time.sleep(0.5)
            answer, sources = st.session_state.agent.ask(query) 
            st.session_state.chat_history[-1] = (query, answer, sources)

    st.rerun()

st.markdown("---")
if st.button("Generate Agent Activity Report"):
    if "agent" in st.session_state and st.session_state.agent.memory:
        report_content = generate_report(st.session_state.agent.memory)
        st.subheader("Agent's Internal Activity Report")
        st.markdown(report_content)
    else:
        st.warning("No agent or memory found to generate a report.")