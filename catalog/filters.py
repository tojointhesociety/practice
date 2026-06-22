import django_filters
from .models import Book, Genre


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name="title", lookup_expr="icontains", label="Название содержит"
    )
    author = django_filters.CharFilter(
        field_name="author", lookup_expr="icontains", label="Автор содержит"
    )
    genre = django_filters.ModelChoiceFilter(queryset=Genre.objects.all(), label="Жанр")

    class Meta:
        model = Book
        fields = ["title", "author", "genre"]
