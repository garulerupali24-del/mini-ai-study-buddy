"""
Mini AI Study Buddy 🤖
Internship Project - 2026
Features:
- AI Tutor (with conversation memory + reset option)
- Notes Summarizer
- Flashcards
- Quiz with scoring + progress tracking
- Study Workspace (AI + Notes side-by-side)
"""

import streamlit as st
# Feature Modules
from modules.chat import chat_interface
from modules.summarizer import summarizer
from modules.flashcards import flashcards
from modules.quiz import quiz
from modules.workspace import study_workspace


# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Mini AI Study Buddy",
    page_icon="🤖",
    layout="wide"
)


# -------------------------------------------------
# Session Initialization
# -------------------------------------------------
def init_session():
    defaults = {
        "quiz_taken": 0,
        "total_score": 0,
        "chat_history": [],          # AI Tutor memory
        "workspace_notes": "",
        "workspace_history": []      # Workspace AI memory
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session()


# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.title("🤖 Mini AI Study Buddy")
st.sidebar.markdown("AI-powered learning assistant")
st.sidebar.divider()

feature = st.sidebar.radio(
    "Navigate",
    [
        "AI Tutor",
        "Summarizer",
        "Flashcards",
        "Quiz",
        "Study Workspace",
        "Progress"
    ]
)

# -------------------------------------------------
# AI Tutor Reset Button (Only when selected)
# -------------------------------------------------
if feature == "AI Tutor":
    st.sidebar.divider()
    st.sidebar.subheader("⚙ AI Tutor Settings")

    if st.sidebar.button("🔄 Reset Conversation"):
        st.session_state.chat_history = []
        st.sidebar.success("Conversation reset!")


# -------------------------------------------------
# Progress Stats (Always Visible)
# -------------------------------------------------
st.sidebar.divider()
st.sidebar.subheader("📊 Performance")

st.sidebar.write(f"Quizzes Taken: {st.session_state.quiz_taken}")

if st.session_state.quiz_taken > 0:
    avg_score = st.session_state.total_score / st.session_state.quiz_taken
    st.sidebar.write(f"Average Score: {avg_score:.2f}")
else:
    st.sidebar.write("Average Score: 0")


# -------------------------------------------------
# Main Title
# -------------------------------------------------
st.title("🤖 Mini AI Study Buddy")
st.caption("Explain concepts • Summarize notes • Practice • Write notes")
st.divider()


# -------------------------------------------------
# Feature Routing
# -------------------------------------------------
features = {
    "AI Tutor": chat_interface,
    "Summarizer": summarizer,
    "Flashcards": flashcards,
    "Quiz": quiz,
    "Study Workspace": study_workspace
}

try:
    if feature in features:
        with st.spinner("Loading feature..."):
            features[feature]()

    elif feature == "Progress":
        st.header("📊 Learning Progress")

        st.write(f"Total Quizzes Taken: {st.session_state.quiz_taken}")

        if st.session_state.quiz_taken > 0:
            avg_score = st.session_state.total_score / st.session_state.quiz_taken
            st.success(f"Average Score: {avg_score:.2f}")
        else:
            st.info("Take a quiz to see your performance statistics.")

except Exception:
    st.error("Something went wrong. Please try again.")


# -------------------------------------------------
# Footer
# -------------------------------------------------
st.divider()
st.caption("Built using Streamlit + Groq LLM | AI & ML Internship Project 2026")