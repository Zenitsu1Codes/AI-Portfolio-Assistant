# 🤖 AI Portfolio Assistant

An intelligent AI chatbot that acts as a **personal portfolio assistant**, answering questions about your skills, experience, projects, and career. The assistant uses your resume and personal summary as context, allowing recruiters and potential clients to interact with you naturally.

The project is powered by **Groq's Llama 3.3**, features **function/tool calling**, and automatically records leads and unknown questions through **ntfy notifications**.

---

# ✨ Features

* 🤖 AI-powered portfolio chatbot
* 📄 Reads information directly from your resume (PDF)
* 📝 Uses a personal summary to answer questions naturally
* 💬 Interactive chat interface built with Gradio
* 🧠 Maintains conversation history
* 🛠 Uses LLM Function Calling (Tool Calling)
* 📧 Automatically records visitor contact information
* 🔔 Sends real-time notifications using ntfy.sh
* ❓ Records unanswered questions for future improvements
* ⚡ Fast inference using Groq's Llama 3.3 model

---

# 🛠 Tech Stack

* Python
* Groq API
* Llama 3.3 70B Versatile
* Gradio
* PyPDF
* Python Dotenv
* Requests
* JSON

---

# 📂 Project Structure

```text
AI-Portfolio-Assistant/
│
├── app.py
├── assistant.ipynb
├── requirements.txt
├── README.md
└── me/
    ├── Harsh Asarsa.pdf
    └── summary.txt
```

---

# 🧠 Architecture

```text
                User
                  │
                  ▼
        Gradio Chat Interface
                  │
                  ▼
        Portfolio AI Assistant
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
 Resume + Summary      Groq LLM
        │                   │
        └─────────┬─────────┘
                  ▼
         Function Calling
        ┌─────────┴──────────┐
        ▼                    ▼
 Record User Details   Record Unknown Question
        │                    │
        └─────────┬──────────┘
                  ▼
           ntfy Push Notification
```

---

# 🚀 Features in Detail

### 📄 Resume-Aware Responses

The assistant reads your resume PDF and personal summary to answer questions about:

* Education
* Technical Skills
* Experience
* Projects
* Certifications
* Career Goals

---

### 📧 Lead Collection

If a visitor wants to contact you, the AI automatically:

* asks for their email
* stores their details
* records conversation notes
* sends a notification using ntfy

---

### ❓ Unknown Question Tracking

Whenever the AI cannot confidently answer a question, it automatically records it so you can improve the assistant over time.

---

### 🔔 Instant Notifications

Every lead or unknown question is pushed instantly through **ntfy.sh**, allowing you to monitor interactions in real time.

---

# ⚙️ Installation

Clone the repository.

```bash
git clone https://github.com/Zenitsu1Codes/ai-portfolio-assistant.git

cd ai-portfolio-assistant
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_api_key
```

You can also customize the ntfy topic inside `app.py` to receive notifications on your own channel.

---

# ▶️ Run

```bash
python app.py
```

A local Gradio interface will open in your browser.

---

# 💬 Example Questions

* Tell me about yourself.
* What projects have you worked on?
* What programming languages do you know?
* Can I hire you?
* How can I contact you?
* Tell me about your AI projects.

---

# 🧠 Function Calling Workflow

```text
User Question
      │
      ▼
Groq LLM
      │
      ▼
Need Tool?
      │
 ┌────┴────┐
 │         │
 ▼         ▼
Record Lead
Unknown Question
 │         │
 └────┬────┘
      ▼
ntfy Notification
```

---

# 📚 Learning Outcomes

This project demonstrates:

* AI Chatbots
* Function Calling
* Tool Integration
* Resume Parsing
* Prompt Engineering
* Context Injection
* Gradio Applications
* Notification Systems
* LLM-powered Portfolio Websites

---

# 🔮 Future Improvements

* Memory for returning users
* Voice interaction
* Multi-language support
* RAG using a vector database
* Web deployment
* Email integration
* Analytics dashboard
* Admin panel
* Resume upload from UI
* Streaming responses

---

# 👨‍💻 Author

**Harsh Asarsa**

AI • Python • Machine Learning • Agentic AI • Automation

If you found this project helpful, consider giving it a ⭐ on GitHub.
:::

---

This README presents the project professionally for GitHub and emphasizes the AI engineering concepts it demonstrates, including **LLM function calling**, **context-aware responses**, **resume parsing**, and **lead automation**.
