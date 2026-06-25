from django.urls import path
from . import views

urlpatterns = [
    path("", views.BookListView.as_view(), name="book_list"),
    path("book/<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
    path("book/create/", views.BookCreateView.as_view(), name="book_create"),
    path("librarian/", views.librarian_page, name="librarian_page"),
    path("guest/", views.guest_page, name="guest_page"),
    path("invoices", views.InvoiceListView.as_view(), name="invoice_list"),
    path("invoice/<int:pk>/", views.InvoiceDetailView.as_view(), name="invoice_detail"),
    path("my-books/", views.my_books, name="my_books"),
    path("issue/<int:pk>/", views.issue_book, name="issue_book"),
    path("invoice/<int:pk>/pdf/", views.invoice_pdf, name="invoice_pdf"),
    path("book/<int:pk>/modal/", views.book_detail_modal, name="book_detail_modal"),
]
