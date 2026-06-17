from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .decorators import librarian_required, guest_required


def home(request):
    return render(request, "home.html")


@librarian_required
def librarian_page(request):
    return render(request, "librarian_page.html")


@guest_required
def guest_page(request):
    return render(request, "guest_page.html")
