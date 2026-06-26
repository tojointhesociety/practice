from django import forms
from .models import Book


class BookCreateForm(forms.ModelForm):
    copies_count = forms.IntegerField(
        min_value=1,
        max_value=100,
        initial=1,
        label="Количество экземпляров",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
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
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "author": forms.TextInput(attrs={"class": "form-control"}),
            "isbn": forms.TextInput(attrs={"class": "form-control"}),
            "genre": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "publisher": forms.TextInput(attrs={"class": "form-control"}),
            "year": forms.NumberInput(attrs={"class": "form-control"}),
        }
