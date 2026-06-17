from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("librarian/", views.librarian_page, name="librarian_page"),
    path("guest/", views.guest_page, name="guest_page"),
]
