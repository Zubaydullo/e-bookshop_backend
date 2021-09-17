import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    price = django_filters.NumberFilter()
    book_type = django_filters.MultipleChoiceFilter()
    author = django_filters.CharFilter(field_name="author", lookup_expr="icontains")

    class Meta:
        model = Book
        fields = ['title', 'price', 'book_type', 'author']
