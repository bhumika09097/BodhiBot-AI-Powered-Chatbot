# 🤖 BodhiBot — AI-Powered Chatbot

BodhiBot is an AI-powered chatbot web application built using **Python, Flask, and the Groq API**. It provides an interactive chat experience with AI-generated responses, user authentication, and conversation history management.

🌐 **Live Demo:** [Try BodhiBot](https://BhumikaRathour09097.pythonanywhere.com)

💻 **GitHub Repository:** [BodhiBot AI-Powered Chatbot](https://github.com/bhumika09097/BodhiBot-AI-Powered-Chatbot)

---

## ✨ Features

* 🤖 **AI-Powered Chat:** Get intelligent conversational responses using the Groq API.
* 🔐 **User Authentication:** Sign up, log in, and log out.
* 💬 **Interactive Chat Interface:** Send messages and receive AI-generated replies.
* 🗂️ **Conversation History:** Save and access previous conversations.
* 🆕 **New Chat:** Start a new conversation whenever needed.
* 💾 **Database Integration:** Store users, conversations, and messages using SQLite.
* 🎨 **Responsive Interface:** Frontend built with HTML, CSS, and JavaScript.

---

## 🛠️ Tech Stack

| Technology       | Purpose                         |
| ---------------- | ------------------------------- |
| Python           | Backend programming             |
| Flask            | Web framework                   |
| Groq API         | AI-generated responses          |
| Flask-SQLAlchemy | Database integration            |
| SQLite           | Data storage                    |
| HTML5            | Page structure                  |
| CSS3             | Styling and layout              |
| JavaScript       | Frontend interactivity          |
| python-dotenv    | Environment variable management |

---

## 📁 Project Structure

```text
BodhiBot/
│
├── app.py
├── requirements.txt
├── .env
│
├── static/
│   ├── images/
│   │   └── logo.png
│   ├── login.css
│   ├── sign-up.css
│   ├── script.js
│   └── style.css
│
└── templates/
    ├── index.html
    ├── login.html
    └── signup.html
```

---

## 🚀 Getting Started

Follow these steps to run BodhiBot on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/bhumika09097/BodhiBot-AI-Powered-Chatbot.git
```

### 2. Navigate to the Project Directory

```bash
cd BodhiBot-AI-Powered-Chatbot
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory and add the following:

```env
API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key
```

Get your API key from the [Groq Console](https://console.groq.com/keys).

Replace the placeholder values with your own credentials.

**Security note:** Never upload your `.env` file or expose your API key in a public repository.

### 6. Run the Application

```bash
python app.py
```

Open the local URL displayed in your terminal, usually:

```text
http://127.0.0.1:5000
```

---

## 🧠 AI Model

BodhiBot currently uses the following model through the Groq API:

```text
openai/gpt-oss-120b
```

The model is configured in `app.py`. Model availability depends on the API provider and your account access.

---

## 🌐 Deployment

BodhiBot is deployed using **PythonAnywhere**.

The deployment requires:

* A compatible Python environment.
* Installation of the required dependencies.
* Correct WSGI configuration.
* Properly configured API and Flask secret-key environment variables.
* Reloading the web application after configuration changes.

**Live Website:** https://BhumikaRathour09097.pythonanywhere.com

---

## 🔒 Security

* Keep API keys private.
* Never commit `.env` to GitHub.
* Use a strong, private Flask `SECRET_KEY`.
* Do not publish database files containing real user information.

---

## 🔮 Future Enhancements

* Streaming AI responses.
* Improved error handling and loading indicators.
* Options to rename and delete conversations.
* Further mobile responsiveness and accessibility improvements.
* Additional chatbot personalization features.

---

## 👩‍💻 Author

**Bhumika Rathour**

* GitHub Profile: [@bhumika09097](https://github.com/bhumika09097)
* Project Repository: [BodhiBot AI-Powered Chatbot](https://github.com/bhumika09097/BodhiBot-AI-Powered-Chatbot)
* Live Demo: [BodhiBot](https://BhumikaRathour09097.pythonanywhere.com)

---

⭐ If you find this project interesting, consider giving the repository a star!
