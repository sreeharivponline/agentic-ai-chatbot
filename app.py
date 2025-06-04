import streamlit as st
from agent import Agent # Assuming 'Agent' class is defined in agent.py

st.set_page_config(page_title="🧠 Agentic Chatbot", layout="centered")
st.title("🧠 Agentic Chatbot with PDF + Web + Memory")

# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

# Initialize Agent and memory history on first run
if "agent" not in st.session_state:
    st.session_state.agent = Agent()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# If file is uploaded, load into vectorstore
if uploaded_file:
    with open("document.pdf", "wb") as f:
        f.write(uploaded_file.read())
    st.session_state.agent.load_pdf("document.pdf")
    st.success("✅ PDF loaded into memory")

if st.session_state.chat_history:
    selected_q = st.selectbox("📝 Select a question to view its answer:", [f"{i+1}. {q}" for i, (q, a) in enumerate(st.session_state.chat_history)])
    index = int(selected_q.split(". ")[0]) - 1
    q, a = st.session_state.chat_history[index]
    st.markdown(f"**Q:** {q}")
    st.markdown(f"**A:** {a}")
    

### Chat Interface

# Display full chat history in a continuous manner
for i, (q, a) in enumerate(st.session_state.chat_history):
    with st.chat_message("user"):
        st.write(q)
    with st.chat_message("assistant"):
        st.write(a)

# Chat input at the bottom
query = st.chat_input("Ask a question:")
if query:
    # Add user query to chat history
    st.session_state.chat_history.append((query, "Thinking...")) # Temporary message

    # Display user query immediately
    with st.chat_message("user"):
        st.write(query)

    # Get agent's answer and update chat history
    # This part will re-run the script, so the "Thinking..." will be replaced
    answer = st.session_state.agent.ask(query)
    st.session_state.chat_history[-1] = (query, answer) # Update the last entry

    # Display agent's answer
    with st.chat_message("assistant"):
        st.write(answer)
        
if st.session_state.chat_history:
    selected_q = st.selectbox("📝 Select a question to view its answer:", [f"{i+1}. {q}" for i, (q, a, s) in enumerate(st.session_state.chat_history)])
    index = int(selected_q.split(". ")[0]) - 1
    q, a, s = st.session_state.chat_history[index]
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Agent:** {a}")
    if s:
        st.markdown("**Sources:**")
        for src in s:
            st.markdown(f"- {src}")
    # Rerun the app to update the chat display
    #st.experimental_rerun()