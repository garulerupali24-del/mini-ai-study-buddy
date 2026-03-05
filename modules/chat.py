import streamlit as st
from utils.groq_client import get_client


def chat_interface():
    st.header("AI Tutor")

    # Initialize session memory
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    client = get_client()

    # Show previous messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask your question...")

    if user_input:

        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",

                    
                    temperature=0.5,
                    max_tokens=1500,

                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful AI tutor. Always provide complete and well-structured answers."
                        }
                    ] + st.session_state.chat_history
                )

                reply = response.choices[0].message.content
                st.markdown(reply)

        st.session_state.chat_history.append(
            {"role": "assistant", "content": reply}
        )
