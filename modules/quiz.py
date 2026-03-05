import streamlit as st
from utils.groq_client import get_client
from PyPDF2 import PdfReader


# -------------------------------------------------
# Initialize Session State
# -------------------------------------------------
def init_session():
    defaults = {
        "quiz_questions": [],
        "quiz_score": 0,
        "quiz_submitted": False,
        "quiz_taken": 0,
        "total_score": 0,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# -------------------------------------------------
# Main Quiz Function
# -------------------------------------------------
def quiz():

    st.header("AI Quiz Generator")
    init_session()

    # -------------------------------------------------
    # INPUT SECTION
    # -------------------------------------------------
    topic = st.text_area("Enter topic or paste notes:")

    uploaded_pdf = st.file_uploader("Upload PDF (optional)", type="pdf")

    pdf_text = ""
    if uploaded_pdf:
        reader = PdfReader(uploaded_pdf)
        for page in reader.pages:
            pdf_text += page.extract_text() or ""

    content = pdf_text if uploaded_pdf else topic

    difficulty = st.selectbox(
        "Select Difficulty",
        ["Easy", "Medium", "Hard"],
        index=1
    )

    num_questions = st.selectbox(
        "Number of Questions",
        [5, 3, 7],
        index=0  # Default = 5
    )

    # -------------------------------------------------
    # GENERATE QUIZ
    # -------------------------------------------------
    if st.button("Generate Quiz"):

        if not content.strip():
            st.warning("Please enter notes or upload a PDF.")
            return

        client = get_client()

        prompt = f"""
Create {num_questions} {difficulty}-level multiple choice questions.

Format strictly as:

Q: Question text
A: Option A
B: Option B
C: Option C
D: Option D
Answer: Correct letter
Explanation: Short explanation

Content:
{content}
"""

        with st.spinner("Generating quiz..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You create clear exam-style MCQs with explanations."},
                    {"role": "user", "content": prompt}
                ]
            )

        output = response.choices[0].message.content

        # Clear previous answers
        for key in list(st.session_state.keys()):
            if key.startswith("question_"):
                del st.session_state[key]

        questions = []
        current_q = {}

        for line in output.split("\n"):
            line = line.strip()

            if line.startswith("Q:"):
                if current_q:
                    questions.append(current_q)
                current_q = {
                    "question": line.replace("Q:", "").strip(),
                    "options": {},
                    "answer": "",
                    "explanation": ""
                }

            elif line.startswith(("A:", "B:", "C:", "D:")):
                letter = line[0]
                current_q["options"][letter] = line[2:].strip()

            elif line.startswith("Answer:"):
                current_q["answer"] = line.replace("Answer:", "").strip()

            elif line.startswith("Explanation:"):
                current_q["explanation"] = line.replace("Explanation:", "").strip()

        if current_q:
            questions.append(current_q)

        if questions:
            st.session_state.quiz_questions = questions
            st.session_state.quiz_score = 0
            st.session_state.quiz_submitted = False
            st.success("Quiz generated successfully!")
        else:
            st.error("Failed to generate quiz. Try again.")

    st.divider()

    # -------------------------------------------------
    # DISPLAY QUESTIONS
    # -------------------------------------------------
    if st.session_state.quiz_questions:

        st.subheader("Answer the following questions:")

        for i, q in enumerate(st.session_state.quiz_questions):

            st.markdown(f"### {i+1}. {q['question']}")

            selected = st.radio(
                "",
                options=list(q["options"].keys()),
                format_func=lambda x, q=q: f"{x}. {q['options'][x]}",
                key=f"question_{i}",
                index=None  # No pre-selection
            )

            # Show result AFTER submission
            if st.session_state.quiz_submitted:

                correct = q["answer"]

                if selected == correct:
                    st.success("✅ Correct")
                else:
                    st.error(f"❌ Incorrect (Correct Answer: {correct})")

                st.info(f"📘 Explanation: {q['explanation']}")

            st.markdown("---")

        # -------------------------------------------------
        # SUBMIT BUTTON
        # -------------------------------------------------
        if not st.session_state.quiz_submitted:
            if st.button("Submit Quiz"):

                score = 0

                for i, q in enumerate(st.session_state.quiz_questions):
                    selected = st.session_state.get(f"question_{i}")
                    if selected == q["answer"]:
                        score += 1

                st.session_state.quiz_score = score
                st.session_state.quiz_submitted = True
                st.session_state.quiz_taken += 1
                st.session_state.total_score += score

                st.rerun()

        else:
            # -------------------------------------------------
            # SHOW FINAL SCORE
            # -------------------------------------------------
            total = len(st.session_state.quiz_questions)
            score = st.session_state.quiz_score

            st.subheader("🎉 Quiz Completed")
            st.write(f"Your Score: **{score} / {total}**")

            if st.button("Start New Quiz"):
                st.session_state.quiz_questions = []
                st.session_state.quiz_score = 0
                st.session_state.quiz_submitted = False
                st.rerun()