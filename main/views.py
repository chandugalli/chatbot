from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# ✅ Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('search')

    return render(request, 'main/login.html')


# ✅ Register page
def register_page(request):
    return render(request, 'main/register.html')


# ✅ Search / Chat page
def search_page(request):
    return render(request, 'main/search.html')


# ✅ Logout
def logout_view(request):
    logout(request)
    return redirect('login')