from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
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
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse


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
        is_librarian = self.request.user.groups.filter(name="Librarians").exists()
        if not is_librarian:
            copies = copies.filter(status="available")
        context["copies"] = copies
        context["is_librarian"] = is_librarian  # <-- добавляем переменную
        return context


@librarian_required
def issue_book(request, pk):
    copy = get_object_or_404(BookCopy, pk=pk)
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        if user_id:
            user = get_object_or_404(User, pk=user_id)
            copy.borrowed_by = user
            copy.status = "issued"
            copy.issued_date = date.today()
            copy.save()
            messages.success(
                request,
                f"Книга {copy.inventory_number} выдана пользователю {user.username}",
            )
            return redirect("book_detail", pk=copy.book.pk)
    guests = User.objects.filter(groups__name="Guests")
    return render(request, "issue_book.html", {"copy": copy, "guests": guests})


@librarian_required
def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    copies = invoice.copies.all()
    template = get_template("invoice_pdf.html")
    html = template.render({"invoice": invoice, "copies": copies})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="invoice_{invoice.number}.pdf"'
    )
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Ошибка генерации PDF", status=500)
    return response


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


@login_required
@guest_required
def my_books(request):
    copies = BookCopy.objects.filter(
        borrowed_by=request.user, status="issued"
    ).order_by("-issued_date")
    return render(request, "my_books.html", {"copies": copies})


def book_detail_modal(request, pk):
    book = get_object_or_404(Book, pk=pk)
    copies = book.copies.all()
    if not request.user.groups.filter(name="Librarians").exists():
        copies = copies.filter(status="available")
    return render(request, "book_detail_modal.html", {"book": book, "copies": copies})
