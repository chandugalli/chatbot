# 🤖 AI Chat App (Django + Groq API)

A full-stack AI chatbot web application built with **Django** and powered by **Groq API (LLM)**.
Users can register, login, and chat with an AI assistant (Chitty-style personality).

---

## 🚀 Features

* 🔐 User Authentication (Login / Register / Logout)
* 🤖 AI Chat System (Groq API - Llama model)
* 💬 Conversation History (stored in database)
* 🎨 Terminal-style UI (Matrix theme)
* ⚡ Fast and lightweight Django backend

---

## 📁 Project Structure

```
search_engine/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── main/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── apps.py
│   ├── templates/
│   │   └── main/
│   │       ├── base.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── chat.html
│   │       └── search.html
```

---

## ⚙️ Installation & Setup

### 🔹 1. Clone the repository

```bash
git clone https://github.com/chandugalli/ai-chat-app.git
cd ai-chat-app
```

---

### 🔹 2. Create Virtual Environment (macOS / Linux)

```bash
python3 -m venv venv
```

### 🔹 Activate Virtual Environment

```bash
source venv/bin/activate
```

👉 You should see:

```
(venv) your-name %
```

---

### 🔹 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 🔹 4. Create `.env` file

```bash
touch .env
```

Add your Groq API key:

```
GROQ_API_KEY=your_api_key_here
```

---

### 🔹 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

👉 This will create the SQLite database automatically.

---

### 🔹 6. Run Development Server

```bash
python manage.py runserver
```

---

### 🌐 Open in browser

```
http://127.0.0.1:8000/
```

---

## 🧠 How It Works

* User sends message from frontend
* Django backend processes request
* Sends request to Groq API
* Receives AI response
* Stores conversation in database
* Displays response in chat UI

---

## 🔐 Environment Variables

| Variable     | Description       |
| ------------ | ----------------- |
| GROQ_API_KEY | Your Groq API key |

---

## 🚫 .gitignore

Make sure you don’t push sensitive files:

```
venv/
__pycache__/
db.sqlite3
.env
*.pyc
```

---

## 🛠️ Tech Stack

* Python (Django)
* HTML, CSS (Tailwind + custom styles)
* Groq API (LLM)
* SQLite (Database)

---

## 🚀 Future Improvements

* ⚡ Streaming AI responses (like ChatGPT)
* 🎨 Better UI animations
* 🌍 Deploy to cloud (Render / Railway)
* 📊 Admin dashboard for analytics

---

## 💡 Author

**Chandu Kumar**
AI Developer | Building AI Products 🚀

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
