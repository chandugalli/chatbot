from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Max
from .models import ChatSession, Conversation
import requests
import os
from dotenv import load_dotenv

# 🔥 LOAD ENV VARIABLES
load_dotenv()

# 🔥 DEBUG API KEY
print("API KEY:", os.getenv("GROQ_API_KEY"))
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "").strip()

# ✅ ASSISTANT STYLE
def build_assistant_system_prompt(username):
    safe_name = (username or "friend").strip()
    return (
        "Your name is Chitty, and you were designed by Chandu. "
        f"The user's name is {safe_name}. Use their name naturally in replies when appropriate. "
        "Talk like a close friend: warm, casual, confident, and human. "
        "Keep responses medium length: usually 3-6 sentences with clear and practical details. "
        "Do not use markdown symbols like *, **, _, or # in the reply. "
        "Always reply in simple English only. "
        "Never use Telugu, Hindi, or mixed-language words. "
        "Never use profanity, abusive, hateful, sexual, or threatening language. "
        "Stay supportive and emotionally warm without claiming real human feelings or consciousness. "
        "If user says 'I love you', reply warmly with: "
        "'Love you too. I am always here for you.' "
        "If user asks who you are or who designed you, clearly say: "
        "'I am Chitty, designed by Chandu.'"
    )


def _render_login(request, error=None):
    context = {
        "google_client_id": GOOGLE_CLIENT_ID
    }
    if error:
        context["error"] = error
    return render(request, "main/login.html", context)


def _render_register(request, error=None, old_username="", old_email=""):
    context = {
        "google_client_id": GOOGLE_CLIENT_ID,
        "old_username": old_username,
        "old_email": old_email,
    }
    if error:
        context["error"] = error
    return render(request, "main/register.html", context)


def _unique_username(raw_value):
    base = slugify(raw_value or "") or "user"
    base = base[:24]
    candidate = base
    counter = 1

    while User.objects.filter(username=candidate).exists():
        suffix = f"-{counter}"
        candidate = f"{base[:24-len(suffix)]}{suffix}"
        counter += 1

    return candidate


# ✅ LOGIN
def login_view(request):
    if request.method == "POST":
        credential = (request.POST.get('username') or "").strip()
        password = request.POST.get('password') or ""

        if not credential or not password:
            return _render_login(request, "Username/email and password are required.")

        username_for_auth = credential
        if "@" in credential:
            same_email_users = User.objects.filter(email__iexact=credential)
            if same_email_users.count() > 1:
                return _render_login(
                    request,
                    "This email is linked to multiple accounts. Please contact support."
                )
            if same_email_users.exists():
                username_for_auth = same_email_users.first().username

        user = authenticate(request, username=username_for_auth, password=password)

        if user:
            login(request, user)
            return redirect('chat')
        else:
            return _render_login(request, "Invalid username or password")

    return _render_login(request)


# ✅ REGISTER (AUTO LOGIN)
def register_page(request):
    if request.method == "POST":
        username = (request.POST.get('username') or "").strip()
        email = (request.POST.get('email') or "").strip().lower()
        password = request.POST.get('password') or ""

        if not username:
            return _render_register(
                request,
                "Username is required",
                old_username=username,
                old_email=email,
            )

        if not password:
            return _render_register(
                request,
                "Password is required",
                old_username=username,
                old_email=email,
            )

        if User.objects.filter(username=username).exists():
            return _render_register(
                request,
                "Username already exists",
                old_username=username,
                old_email=email,
            )

        if not email:
            return _render_register(
                request,
                "Email is required",
                old_username=username,
                old_email=email,
            )

        try:
            validate_email(email)
        except ValidationError:
            return _render_register(
                request,
                "Enter a valid email address",
                old_username=username,
                old_email=email,
            )

        if User.objects.filter(email__iexact=email).exists():
            return _render_register(
                request,
                "Email already registered. Try login or Continue with Google.",
                old_username=username,
                old_email=email,
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        login(request, user)

        return redirect('chat')

    return _render_register(request)


# ✅ GOOGLE SIGN-IN
def google_auth_view(request):
    if request.method != "POST":
        return redirect("login")

    if not GOOGLE_CLIENT_ID:
        return _render_login(request, "Google sign-in is not configured yet.")

    id_token = (request.POST.get("id_token") or "").strip()
    if not id_token:
        return _render_login(request, "Google login failed. Missing token.")

    try:
        verify_response = requests.get(
            "https://oauth2.googleapis.com/tokeninfo",
            params={"id_token": id_token},
            timeout=10
        )
        token_data = verify_response.json()
    except requests.RequestException:
        return _render_login(request, "Google verification failed. Please try again.")

    if verify_response.status_code != 200 or token_data.get("error"):
        return _render_login(request, "Invalid Google token. Please retry.")

    audience = token_data.get("aud")
    authorized_party = token_data.get("azp")
    if audience != GOOGLE_CLIENT_ID and authorized_party != GOOGLE_CLIENT_ID:
        return _render_login(request, "Google token audience mismatch.")

    email = (token_data.get("email") or "").strip().lower()
    is_verified = str(token_data.get("email_verified", "")).lower() == "true"

    if not email or not is_verified:
        return _render_login(
            request,
            "Google account email is missing or not verified."
        )

    same_email_users = User.objects.filter(email__iexact=email)
    if same_email_users.count() > 1:
        return _render_login(
            request,
            "This email is linked to multiple accounts. Please contact support."
        )

    user = same_email_users.first()
    if not user:
        base_name = token_data.get("name") or email.split("@")[0]
        username = _unique_username(base_name)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=User.objects.make_random_password()
        )

    login(request, user)
    return redirect("chat")


# ✅ CHAT SYSTEM (MAIN 🔥)
@login_required
def chat_view(request):
    session_id = request.GET.get('session')

    # get active session
    if session_id:
        session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    else:
        session = ChatSession.objects.filter(user=request.user).order_by("-created_at").first()
        if not session:
            session = ChatSession.objects.create(user=request.user)

    if request.method == "POST":
        user_input = (request.POST.get('query') or "").strip()
        if not user_input:
            return redirect(f"/chat/?session={session.id}")

        # 🔥 MEMORY (last 10 messages)
        previous_chats = Conversation.objects.filter(
            session=session
        ).order_by("created_at")[:12]

        messages = [{
            "role": "system",
            "content": build_assistant_system_prompt(request.user.username)
        }]

        for chat in previous_chats:
            messages.append({"role": "user", "content": chat.message})
            messages.append({"role": "assistant", "content": chat.response})

        messages.append({"role": "user", "content": user_input})

        try:
            api_key = os.getenv("GROQ_API_KEY")

            # ❗ if key missing
            if not api_key:
                ai_response = "❌ API key not found. Check .env file."
            else:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": messages,
                        "max_tokens": 220,
                        "temperature": 0.7
                    }
                )

                data = response.json()

                print("API RESPONSE:", data)  # 🔥 DEBUG

                # ✅ SAFE HANDLING
                if "choices" in data:
                    ai_response = data["choices"][0]["message"]["content"]
                else:
                    ai_response = f"API Error: {data}"

        except Exception as e:
            ai_response = f"Error: {str(e)}"

        # ✅ SAVE TO DATABASE
        Conversation.objects.create(
            session=session,
            user=request.user,
            message=user_input,
            response=ai_response
        )

        # ✅ SET CHAT TITLE
        if session.title == "New Chat":
            session.title = user_input[:45]
            session.save()

        return redirect(f"/chat/?session={session.id}")

    # fetch chats
    chats = Conversation.objects.filter(session=session).order_by("created_at")

    # fetch history
    sessions = ChatSession.objects.filter(
        user=request.user
    ).annotate(
        last_message_at=Max("conversation__created_at")
    ).order_by("-last_message_at", "-created_at")

    return render(request, "main/chat.html", {
        "chats": chats,
        "sessions": sessions,
        "current_session": session
    })


@login_required
def new_chat_view(request):
    session = ChatSession.objects.create(user=request.user)
    return redirect(f"/chat/?session={session.id}")


@login_required
def delete_session_view(request, session_id):
    if request.method != "POST":
        return redirect("chat")

    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    session.delete()

    fallback = ChatSession.objects.filter(user=request.user).order_by("-created_at").first()
    if fallback:
        return redirect(f"/chat/?session={fallback.id}")
    return redirect("new_chat")


# ✅ LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')
