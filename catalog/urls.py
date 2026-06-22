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
]
