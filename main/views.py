from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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

        # check if user already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'main/register.html', {
                "error": "Username already exists"
            })

        # create new user
        user = User.objects.create_user(username=username, password=password)
        user.save()

        return redirect('login')

    return render(request, 'main/register.html')


# ✅ CHAT / SEARCH PAGE
@login_required
def search_page(request):
    global chat_history

    if request.method == "POST":
        user_input = request.POST.get('query')

        # dummy AI response (you can replace with OpenAI later)
        ai_response = f"You said: {user_input}"

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