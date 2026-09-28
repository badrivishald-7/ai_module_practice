"""app.py - Streamlit chatbot that compares Basic vs Engineered prompts."""
 
import streamlit as st
 
from helpers import ask
from prompts import BASIC_SYSTEM_PROMPT, ENGINEERED_SYSTEM_PROMPT
 
MAX_HISTORY_MESSAGES = 8
 
st.set_page_config(page_title="Module 3: Adding Memory")
st.title("Module 3: Adding Memory")
 
if "messages" not in st.session_state:
    st.session_state.messages = []
 
mode = st.sidebar.radio("Choose Mode", ["Basic Mode", "Engineered Mode"])
st.sidebar.caption(
    "Basic Mode: plain prompt, free-form answers. "
    "Engineered Mode: analyst role, few-shot example, fixed format, guard rule."
)
 
if st.sidebar.button("Clear chat"):
    st.session_state.messages = []
 
# NEW: a checkbox that fakes a broken API call, so we can safely
# demo what happens when something goes wrong.
simulate_failure = st.sidebar.checkbox("Simulate API failure (for demo)")
 
if mode == "Basic Mode":
    system_prompt = BASIC_SYSTEM_PROMPT
else:
    system_prompt = ENGINEERED_SYSTEM_PROMPT
 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
 
total_messages = len(st.session_state.messages)
sent_messages = min(total_messages, MAX_HISTORY_MESSAGES)
st.sidebar.metric("Messages stored", total_messages)
st.sidebar.metric("Messages sent to model", sent_messages)
 
user_input = st.chat_input("Ask a question...")
 
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
 
    history_to_send = st.session_state.messages[-MAX_HISTORY_MESSAGES:]
 
    with st.chat_message("assistant"):
        try:
            if simulate_failure:
                raise RuntimeError("Simulated failure for demo purposes")
            reply = ask(history_to_send, system_prompt)
        except Exception:
            reply = "Sorry, something went wrong on my end. Please try again."
        st.markdown(reply)
 
    st.session_state.messages.append({"role": "assistant", "content": reply})