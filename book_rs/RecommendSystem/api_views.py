from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book, Genre, Author, Comment
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BooksSerializer, GenresSerializer, AuthorsSerializer, CommentsSerializer, UserSerializer
from django.contrib.auth.models import User


# Класс ModelViewSet позволяет определить сразу весь набор функций 
# для какой-то определенной модели.
# А именно: 
#   1) Вывод всех записей 
#   2) Вывод какой-то конкретной записи по ее pk 
#   3) Добавление новой записи 
#   4) Изменение уже имеющейся записи 
#   5) Удаление уже имеющейся записи



class BooksViewSet(viewsets.ModelViewSet):
    ''' Представление для работы с моделью книг '''
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genre', 'year']
    search_fields = ['author__firstname', 'author__lastname', 'author__patronymic']
    ordering_fields = ['year', 'rating']

    @action(methods=['get'], detail=False)
    def genres(self, request):
        genres = Genre.objects.all()
        return Response({'genres': [{'pk': genre.pk, 'genre': genre.genre_name} for genre in genres]})
    

class GenresViewSet(viewsets.ModelViewSet):
    ''' Представление для работы с моделью жанров '''
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class AuthorsViewSet(viewsets.ModelViewSet):
    ''' Представление для работы с моделью авторов книг '''
    queryset = Author.objects.all()
    serializer_class = AuthorsSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    ''' Представление для работы с моделью комментариев к книгам '''
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]