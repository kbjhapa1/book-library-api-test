from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("csrf/", views.csrf, name="csrf"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("me/", views.me, name="me"),
    path("books/", views.BookListCreateView.as_view(), name="book-list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
]