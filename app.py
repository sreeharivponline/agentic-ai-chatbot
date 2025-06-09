# app.py

import streamlit as st
import os
import time  # For simulating thinking time
from dotenv import load_dotenv
load_dotenv()
from agent import Agent
from tools.report_tool import generate_report  # For displaying the agent's internal report

st.set_page_config(page_title="🧠 Agentic Chatbot", layout="centered")
st.title("🧠 Agentic Chatbot with PDF + Web + Memory")

# --- Initialization ---
# Initialize Agent and memory history on first run or if session state is cleared
if "agent" not in st.session_state:
    st.session_state.agent = Agent()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Stores (query, answer, sources) tuples

# Initialize to None to track the uploaded file identity (avoid reloads)
if "last_uploaded_file_id" not in st.session_state:
    st.session_state.last_uploaded_file_id = None

# Ensure GROQ_API_KEY is set
if not os.getenv("GROQ_API_KEY"):
    st.warning("🚨 GROQ_API_KEY environment variable not set. Please set it to use the chatbot.")
    st.stop()  # Stop the app if API key is missing

# --- PDF Upload Section ---
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

# Condition to load PDF only if a new file is uploaded or no PDF was loaded before
if uploaded_file:
    # Streamlit file uploader does NOT have 'file_id' property by default,
    # so let's uniquely identify the file by its name + size or use hash
    uploaded_file_id = f"{uploaded_file.name}_{uploaded_file.size}"

    if (st.session_state.last_uploaded_file_id is None
            or st.session_state.last_uploaded_file_id != uploaded_file_id):

        # Save the file to a temporary location
        temp_pdf_path = "document.pdf"
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.read())

        # Store file_id to prevent re-uploading the same file
        st.session_state.last_uploaded_file_id = uploaded_file_id

        with st.spinner(f"Loading '{uploaded_file.name}' into memory..."):
            try:
                st.session_state.agent.load_pdf(temp_pdf_path)
                st.success(f"✅ PDF '{uploaded_file.name}' loaded into memory!")
                # Optional: Remove temp file if not needed anymore
                # os.remove(temp_pdf_path)
            except Exception as e:
                st.error(f"❌ Failed to load PDF: {e}")
                st.session_state.last_uploaded_file_id = None  # Reset to allow retry
        #st.experimental_rerun()  # Rerun app to update state after PDF load

# --- Chat Interface ---

# Display full chat history continuously
for i, (q, a, s) in enumerate(st.session_state.chat_history):
    with st.chat_message("user"):
        st.write(q)
    with st.chat_message("assistant"):
        st.write(a)
        if s:
            st.markdown("**Sources:**")
            for src in s:
                st.markdown(f"- {src}")

# Input box for user query
query = st.chat_input("Ask a question (e.g., 'What is X?', 'web search for: Y'):")

if query:
    # Append placeholder while thinking
    st.session_state.chat_history.append((query, "Thinking...", None))

    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            time.sleep(0.5)  # Simulate short thinking delay
            answer, sources = st.session_state.agent.ask(query)
            # Update the last chat message with actual answer and sources
            st.session_state.chat_history[-1] = (query, answer, sources)
            st.write(answer)

    # Rerun to update UI with new response
    #st.experimental_rerun()

st.markdown("---")

# Button to generate the agent's internal activity report
if st.button("Generate Agent Activity Report"):
    if "agent" in st.session_state and st.session_state.agent.memory:
        report_content = generate_report(st.session_state.agent.memory)

        st.subheader("Agent's Internal Activity Report")
        st.markdown(report_content)
    else:
        st.warning("No agent or memory found to generate a report.")
