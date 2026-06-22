from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Book, BookCopy, Invoice
from .decorators import librarian_required, guest_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import date
from .forms import BookCreateForm
from django.utils.decorators import method_decorator
from .decorators import librarian_required
from .filters import BookFilter
from django_filters.views import FilterView


def home(request):
    return render(request, "home.html")


class BookListView(FilterView):
    model = Book
    template_name = "book_list.html"
    context_object_name = "books"
    paginate_by = 10
    filterset_class = BookFilter

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["book_list_partial.html"]
        return [self.template_name]


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


@method_decorator(librarian_required, name="dispatch")
class BookCreateView(CreateView):
    model = Book
    form_class = BookCreateForm
    template_name = "book_create.html"
    success_url = reverse_lazy("book_list")

    def form_valid(self, form):

        book = form.save()

        today = date.today()
        year = str(today.year)
        last_invoice = (
            Invoice.objects.filter(number__startswith=f"НК-{year}-")
            .order_by("-number")
            .first()
        )
        if last_invoice:
            last_num = int(last_invoice.number.split("-")[-1])
            new_invoice_num = last_num + 1
        else:
            new_invoice_num = 1
        invoice_number = f"НК-{year}-{new_invoice_num:03d}"
        invoice = Invoice.objects.create(
            supplier="Основной поставщик", number=invoice_number, date=today
        )

        copies_count = form.cleaned_data["copies_count"]
        copies = []
        for i in range(copies_count):
            copy = BookCopy(book=book, invoice=invoice)
            copy.save()
            copies.append(copy)

        messages.success(
            self.request,
            f"Добавлена книга «{book.title}» и {copies_count} экз. Накладная №{invoice_number}",
        )
        return super().form_valid(form)


@method_decorator(librarian_required, name="dispatch")
class InvoiceListView(ListView):
    model = Invoice
    template_name = "invoice_list.html"
    context_object_name = "invoices"


@method_decorator(librarian_required, name="dispatch")
class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = "invoice_detail.html"
    context_object_name = "invoice"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["copies"] = self.object.copies.all()
        return context
