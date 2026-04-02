from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .models import Conversation
import requests


def login_page(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user:
            login(request, user)
            return redirect("search")

        return render(request, "main/login.html", {"error": "Invalid credentials"})

    return render(request, "main/login.html")


def register_page(request):
    if request.method == "POST":
        if User.objects.filter(username=request.POST.get("username")).exists():
            return render(request, "main/register.html", {"error": "User exists"})

        User.objects.create_user(
            username=request.POST.get("username"),
            email=request.POST.get("email"),
            password=request.POST.get("password")
        )

        return redirect("login")

    return render(request, "main/register.html")


def search_page(request):
    if not request.user.is_authenticated:
        return redirect("login")

    chats = Conversation.objects.filter(user=request.user)

    if request.method == "POST":
        query = request.POST.get("query")

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [{"role": "user", "content": query}]
                }
            )

            ai = response.json()["choices"][0]["message"]["content"]

        except:
            ai = "AI Error"

        Conversation.objects.create(
            user=request.user,
            message=query,
            response=ai
        )

        return redirect("search")

    return render(request, "main/chat.html", {"chats": chats})


def logout_page(request):
    logout(request)
    return redirect("login")