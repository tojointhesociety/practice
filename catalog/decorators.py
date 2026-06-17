from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test


def is_librarian(user):
    return user.groups.filter(name="Librarians").exists()


def is_guest(user):
    return user.groups.filter(name="Guests").exists()


librarian_required = user_passes_test(is_librarian, login_url="/login/")

guest_required = user_passes_test(is_guest, login_url="/login/")
