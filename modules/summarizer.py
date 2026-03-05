import streamlit as st
from utils.groq_client import get_client


def summarizer():
    st.header("📝 Notes Summarizer")

    st.write("Paste your notes below and generate a concise summary.")

    # Input Area
    user_text = st.text_area(
        "Enter your notes:",
        height=300,
        placeholder="Paste your study notes here..."
    )

    # Summary Length Option
    summary_type = st.selectbox(
        "Select summary style:",
        ["Short Summary", "Detailed Summary", "Bullet Points"]
    )

    if st.button("✨ Generate Summary"):
        if not user_text.strip():
            st.warning("Please enter some text to summarize.")
            return

        client = get_client()

        # Prompt Engineering
        if summary_type == "Short Summary":
            prompt = f"Summarize the following text in a short and clear paragraph:\n\n{user_text}"
        elif summary_type == "Detailed Summary":
            prompt = f"Provide a detailed and well-structured summary of the following text:\n\n{user_text}"
        else:
            prompt = f"Summarize the following text into clear bullet points for quick revision:\n\n{user_text}"

        try:
            with st.spinner("Generating summary..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are an academic study assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=500
                )

            summary = response.choices[0].message.content

            st.subheader("📄 Summary Output")
            st.write(summary)

            # Download Option
            st.download_button(
                label="⬇ Download Summary",
                data=summary,
                file_name="summary.txt",
                mime="text/plain"
            )

        except Exception:
            st.error("Something went wrong while generating the summary.")