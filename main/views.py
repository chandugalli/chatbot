from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import requests
import os

# temporary chat storage
chat_history = []


# ✅ LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('search')
        else:
            return render(request, 'main/login.html', {
                "error": "Invalid username or password"
            })

    return render(request, 'main/login.html')


# ✅ REGISTER
def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'main/register.html', {
                "error": "Username already exists"
            })

        user = User.objects.create_user(username=username, password=password)
        user.save()

        return redirect('login')

    return render(request, 'main/register.html')


# ✅ CHAT / SEARCH PAGE (GROQ AI FINAL)
@login_required
def search_page(request):
    global chat_history

    if request.method == "POST":
        user_input = request.POST.get('query')

        try:
            api_key = os.getenv("GROQ_API_KEY")

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "user", "content": user_input}
                    ]
                }
            )

            data = response.json()

            if "choices" in data:
                ai_response = data["choices"][0]["message"]["content"]
            else:
                ai_response = f"API Error: {data}"

        except Exception as e:
            ai_response = f"Error: {str(e)}"

        chat_history.append({
            "message": user_input,
            "response": ai_response
        })

    return render(request, 'main/search.html', {
        "chats": chat_history
    })


# ✅ LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')