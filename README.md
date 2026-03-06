# Mini AI Study Buddy 🤖

Mini AI Study Buddy is an AI-powered learning assistant designed to help students understand complex concepts, summarize study notes, generate flashcards, and practice quizzes for more effective self-study.

The application integrates multiple AI-driven tools into a single platform to support **interactive and personalized learning**.

This project was developed as part of the **Artificial Intelligence and Machine Learning Internship Program conducted by Edunet Foundation in collaboration with AICTE**.

---

## 🌐 Live Demo

Try the application here:
https://mini-ai-study-buddy-t6cwcribqpy58gqebtzd6s.streamlit.app/



---

##  Features

*  **AI Tutor** – Ask questions and receive AI-powered explanations
*  **Notes Summarizer** – Convert long notes into concise summaries
*  **Flashcards Generator** – Automatically generate flashcards for revision
*  **Quiz Generator** – Generate quizzes to test knowledge
*  **Study Workspace** – AI assistant with note-taking functionality
*  **Progress Tracker** – Track quiz attempts and average scores

---

## 🛠️ Technology Stack

* Python
* Streamlit
* Groq API (LLaMA Language Model)
* PyPDF2

---

## 📂 Project Structure

```
mini-ai-study-buddy
│
├── app.py
│   Main Streamlit application
│
├── modules
│   ├── chat.py
│   ├── summarizer.py
│   ├── flashcards.py
│   ├── quiz.py
│   └── workspace.py
│
├── utils
│   └── groq_client.py
│
├── screenshots
│   ├── ai_tutor.png
│   ├── summarizer.png
│   ├── flashcards.png
│   ├── quiz.png
│   ├── workspace.png
│   └── progress.png
│
├── presentation
│   └── Mini_AI_Study_Buddy_Presentation.pptx
│
├── requirements.txt
└── README.md
```

---

## 📸 Screenshots

### AI Tutor Interface

![AI Tutor](screenshots/ai_tutor.png)

### Notes Summarizer

![Summarizer](screenshots/summarizer.png)

### Flashcards Module

![Flashcards](screenshots/flashcards.png)

### Quiz Module

![Quiz](screenshots/quiz.png)

### Study Workspace

![Workspace](screenshots/workspace.png)

### Learning Progress Dashboard

![Progress](screenshots/progress.png)

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/garulerupali24-del/mini-ai-study-buddy.git
```

### 2. Navigate to the project directory

```bash
cd mini-ai-study-buddy
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

---

## 🔑 Groq API Key Setup

This application uses the **Groq API** to access the LLaMA language model.

### 1. Get a Groq API Key

1. Go to: https://console.groq.com
2. Sign in or create an account.
3. Generate a new API key.

### 2. Set the API Key as an Environment Variable

#### On Windows

```bash
setx GROQ_API_KEY "your_api_key_here"
```

#### On Mac/Linux

```bash
export GROQ_API_KEY="your_api_key_here"
```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will automatically use the API key from the environment variable.

---

# 📊 Project Presentation

Download the project presentation:

[Mini AI Study Buddy – An AI-Powered Learning Assistant](presentation/Mini_AI_Study_Buddy_An_AI_Powered_Learning_Assistant.pptx)

---

# 🎯 Project Objective

The objective of this project is to build an **AI-powered learning assistant** that helps students:

* Understand complex academic concepts
* Summarize study materials efficiently
* Practice through quizzes and flashcards
* Improve overall learning efficiency during self-study

---

# 🚀 Future Scope

* Integration of an **AI avatar tutor** capable of explaining concepts with voice and emotional interaction
* **Voice-based AI assistant** for hands-free learning
* **Mobile application version** for improved accessibility
* **Personalized learning recommendations** based on student performance

---

## 👩‍💻 Author

**Rupali Dadasaheb Garule**
B.Tech – Computer Science and Engineering
MSS's College of Engineering and Technology, Jalna


🔗 GitHub: https://github.com/garulerupali24-del 

Internship Project – 2026


---


