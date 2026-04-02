import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key'

DEBUG = True

ALLOWED_HOSTS = ['*']

# ✅ CSRF FIX (Railway domain)
CSRF_TRUSTED_ORIGINS = [
    "https://chatbot-production-9718.up.railway.app"
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


# ✅ Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',   # ✅ required
    'django.contrib.staticfiles',

    'main',
]


# ✅ Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',  # ✅ required
]


ROOT_URLCONF = 'config.urls'


# ✅ Templates (FIXED HERE 🔥)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',   # ✅ add
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',  # ✅ FIX
            ],
        },
    },
]


WSGI_APPLICATION = 'config.wsgi.application'


# ✅ Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ✅ Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# ✅ Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'