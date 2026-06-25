import django_filters
from django import forms
from .models import Book, Genre

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название содержит',
        widget=forms.TextInput(attrs={'class': 'form-control filter-input'})
    )
    author = django_filters.CharFilter(
        field_name='author',
        lookup_expr='icontains',
        label='Автор содержит',
        widget=forms.TextInput(attrs={'class': 'form-control filter-input'})
    )
    genre = django_filters.ModelChoiceFilter(
        queryset=Genre.objects.all(),
        label='Жанр',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'genre']