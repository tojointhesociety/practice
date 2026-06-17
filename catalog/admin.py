from django.contrib import admin
from .models import Genre, Book, Invoice, BookCopy


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "genre", "year")
    list_filter = ("genre", "year")
    search_fields = ("title", "author")


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("number", "supplier", "date")


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ("inventory_number", "book", "status", "invoice")
    list_filter = ("status",)
