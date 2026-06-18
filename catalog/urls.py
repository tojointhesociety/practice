from django.urls import path
from . import views

urlpatterns = [
    path(
        "", views.BookListView.as_view(), name="book_list"
    ),  # главная теперь = список книг
    path("book/<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
    path("librarian/", views.librarian_page, name="librarian_page"),
    path("guest/", views.guest_page, name="guest_page"),
]
