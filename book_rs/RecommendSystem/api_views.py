from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book, Genre, Author
from .serializers import BooksSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters


# Класс ModelViewSet позволяет определить сразу весь набор функций 
# для какой-то определенной модели.
# А именно: 
#   1) Вывод всех записей 
#   2) Вывод какой-то конкретной записи по ее pk 
#   3) Добавление новой записи 
#   4) Изменение уже имеющейся записи 
#   5) Удаление уже имеющейся записи


class BookFilter(filters.FilterSet):
    genres = filters.CharFilter


class BooksViewSet(viewsets.ModelViewSet):
    ''' Представление для работы с моделью книг '''
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_fields = ['genre']

    @action(methods=['get'], detail=True)
    def genre(self, request, pk):
        book = Book.objects.get(pk=pk)
        genre = Genre.objects.get(pk=book.genre_id)
        return Response({'genre': genre.genre_name})
    
    @action(methods=['get'], detail=True)
    def author(self, request, pk):
        book = Book.objects.get(pk=pk)
        author = Author.objects.get(pk=book.genre_id)
        return Response({'author': author.__str__()})