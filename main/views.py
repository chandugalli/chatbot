from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Conversation
import requests


# 🔐 LOGIN
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("search")
        else:
            return render(request, "main/login.html", {"error": "Invalid credentials"})

    return render(request, "main/login.html")


# 📝 REGISTER
def register_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "main/register.html", {"error": "User already exists"})

        User.objects.create_user(username=username, email=email, password=password)
        return redirect("login")

    return render(request, "main/register.html")


# 🤖 CHAT
def search_page(request):
    if not request.user.is_authenticated:
        return redirect("login")

    chats = Conversation.objects.filter(user=request.user)

    if request.method == "POST":
        query = request.POST.get("query")

        # 🧠 SYSTEM + USER MESSAGE
        messages = [
            {"role": "system", "content": settings.SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": messages,
                    "temperature": 0.7  # 🔥 more human-like
                }
            )

            ai_answer = response.json()["choices"][0]["message"]["content"]

        except Exception as e:
            print("Error:", e)
            ai_answer = "⚠️ Something went wrong"

        # 💾 SAVE
        Conversation.objects.create(
            user=request.user,
            message=query,
            response=ai_answer
        )

        return redirect("search")

    return render(request, "main/chat.html", {"chats": chats})


# 🚪 LOGOUT
def logout_page(request):
    logout(request)
    return redirect("login")