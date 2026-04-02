from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login_page'),
    path('register/', views.register_page, name='register'),
    path('auth/google/', views.google_auth_view, name='google_auth'),
    path('chat/new/', views.new_chat_view, name='new_chat'),
    path('chat/session/<int:session_id>/delete/', views.delete_session_view, name='delete_session'),
    path('chat/', views.chat_view, name='chat'),
    path('logout/', views.logout_view, name='logout'),
]
