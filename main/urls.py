from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login_page'),
    path('register/', views.register_page, name='register'),
    path('auth/google/', views.google_auth_view, name='google_auth'),
    path('chat/', views.chat_view, name='chat'),
    path('logout/', views.logout_view, name='logout'),
]
