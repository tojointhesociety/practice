from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Book, BookCopy
from .decorators import librarian_required, guest_required


def home(request):
    return render(request, "home.html")


class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
    context_object_name = "books"
    paginate_by = 10


class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        copies = self.object.copies.all()

        if not self.request.user.groups.filter(name="Librarians").exists():
            copies = copies.filter(status="available")
        context["copies"] = copies
        return context


@librarian_required
def librarian_page(request):
    return render(request, "librarian_page.html")


@guest_required
def guest_page(request):
    return render(request, "guest_page.html")
