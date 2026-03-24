from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("search/", views.search_page, name="search"),
    path("logout/", views.logout_page, name="logout"),
]