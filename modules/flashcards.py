import streamlit as st
from utils.groq_client import get_client
from PyPDF2 import PdfReader


# -------------------------------------------------
# Initialize Session State
# -------------------------------------------------
def init_flashcard_session():
    defaults = {
        "flashcards": [],
        "current_card": 0,
        "show_answer": False
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# -------------------------------------------------
# Main Flashcards Function
# -------------------------------------------------
def flashcards():

    st.header("AI Flashcards")

    init_flashcard_session()

    # -------------------------------------------------
    # Input Section
    # -------------------------------------------------

    topic = st.text_area("Enter topic or paste study notes:")

    uploaded_pdf = st.file_uploader("Upload PDF (optional)", type="pdf")

    pdf_text = ""

    if uploaded_pdf:
        reader = PdfReader(uploaded_pdf)
        for page in reader.pages:
            pdf_text += page.extract_text() or ""

    content = pdf_text if uploaded_pdf else topic

    num_cards = st.selectbox(
        "Number of flashcards:",
        [3, 5, 7, 10],
        index=1  # Default 5
    )

    col_generate, col_reset = st.columns([2, 1])

    # -------------------------------------------------
    # Generate Flashcards
    # -------------------------------------------------
    with col_generate:
        if st.button("Generate Flashcards"):

            if not content.strip():
                st.warning("Please enter text or upload a PDF.")
                return

            client = get_client()

            prompt = f"""
Create exactly {num_cards} flashcards from the following content.

Return in this STRICT format:

Q: question
A: answer

Content:
{content}
"""

            with st.spinner("Generating flashcards..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": "You create concise, exam-focused flashcards."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

            output = response.choices[0].message.content

            # Parse Flashcards
            cards = []
            current_q = ""
            current_a = ""

            for line in output.split("\n"):
                if line.startswith("Q:"):
                    current_q = line.replace("Q:", "").strip()
                elif line.startswith("A:"):
                    current_a = line.replace("A:", "").strip()
                    if current_q and current_a:
                        cards.append({
                            "question": current_q,
                            "answer": current_a
                        })
                        current_q = ""
                        current_a = ""

            if cards:
                st.session_state.flashcards = cards
                st.session_state.current_card = 0
                st.session_state.show_answer = False
                st.success("Flashcards generated successfully!")
            else:
                st.error("Could not parse flashcards. Try again.")

    # -------------------------------------------------
    # Reset Flashcards
    # -------------------------------------------------
    with col_reset:
        if st.button("Reset"):
            st.session_state.flashcards = []
            st.session_state.current_card = 0
            st.session_state.show_answer = False
            st.info("Flashcards cleared.")

    st.divider()

    # -------------------------------------------------
    # Display Flashcards
    # -------------------------------------------------
    if st.session_state.flashcards:

        card = st.session_state.flashcards[st.session_state.current_card]
        flip_class = "flipped" if st.session_state.show_answer else ""

        st.markdown(f"""
        <style>
        .flashcard-container {{
            perspective: 1000px;
        }}

        .flashcard {{
            width: 100%;
            min-height: 240px;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.6s;
        }}

        .flashcard.flipped {{
            transform: rotateY(180deg);
        }}

        .flashcard-side {{
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px;
            border-radius: 20px;
            font-size: 22px;
            text-align: center;
            color: white;
            box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        }}

        .front {{
            background: linear-gradient(145deg, #1e293b, #0f172a);
        }}

        .back {{
            background: linear-gradient(145deg, #065f46, #064e3b);
            transform: rotateY(180deg);
        }}
        </style>

        <div class="flashcard-container">
            <div class="flashcard {flip_class}">
                <div class="flashcard-side front">
                    {card["question"]}
                </div>
                <div class="flashcard-side back">
                    {card["answer"]}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Flip Button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Flip"):
                st.session_state.show_answer = not st.session_state.show_answer

        st.markdown("<br>", unsafe_allow_html=True)

        # Navigation
        col_prev, col_count, col_next = st.columns([1, 2, 1])

        with col_prev:
            if st.button("⬅ Previous"):
                if st.session_state.current_card > 0:
                    st.session_state.current_card -= 1
                    st.session_state.show_answer = False

        with col_count:
            st.markdown(
                f"<p style='text-align:center;'>Card {st.session_state.current_card + 1} of {len(st.session_state.flashcards)}</p>",
                unsafe_allow_html=True
            )

        with col_next:
            if st.button("Next ➡"):
                if st.session_state.current_card < len(st.session_state.flashcards) - 1:
                    st.session_state.current_card += 1
                    st.session_state.show_answer = False