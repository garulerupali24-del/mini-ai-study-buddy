import streamlit as st
from utils.groq_client import get_client


def study_workspace():
    st.header("Study Workspace")

    # Initialize session state safely
    if "workspace_notes" not in st.session_state:
        st.session_state.workspace_notes = ""

    if "workspace_history" not in st.session_state:
        st.session_state.workspace_history = []

    col1, col2 = st.columns(2)

    # -------------------------------------------------
    # LEFT SIDE — AI Assistant
    # -------------------------------------------------
    with col1:
        st.subheader("AI Assistant")

        client = get_client()

        # Display chat history
        for msg in st.session_state.workspace_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("Ask something while studying...")

        if user_input:
            st.session_state.workspace_history.append(
                {"role": "user", "content": user_input}
            )

            with st.chat_message("user"):
                st.markdown(user_input)

            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.workspace_history,
                    temperature=0.3,
                    max_tokens=400
                )

            reply = response.choices[0].message.content

            st.session_state.workspace_history.append(
                {"role": "assistant", "content": reply}
            )

            with st.chat_message("assistant"):
                st.markdown(reply)

    # -------------------------------------------------
    # RIGHT SIDE — Notes Section
    # -------------------------------------------------
    with col2:
        st.subheader("📝 My Notes")

        # Buttons aligned to right
        btn_col1, btn_col2 = st.columns([3, 1])

        with btn_col2:
            if st.button("🗑 Clear Notes"):
                st.session_state.workspace_notes = ""
                st.rerun()

        notes = st.text_area(
            "Write your notes here:",
            value=st.session_state.workspace_notes,
            height=400
        )

        st.session_state.workspace_notes = notes

        st.download_button(
            label="⬇ Download Notes",
            data=notes,
            file_name="study_notes.txt",
            mime="text/plain"
        )