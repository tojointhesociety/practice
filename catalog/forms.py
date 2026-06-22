from django import forms
from .models import Book


class BookCreateForm(forms.ModelForm):

    copies_count = forms.IntegerField(
        min_value=1, max_value=100, initial=1, label="Количество экземпляров"
    )

    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "isbn",
            "genre",
            "description",
            "publisher",
            "year",
        ]
