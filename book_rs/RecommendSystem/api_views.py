from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action
from .models import Book, Genre, Author, Comment, BlackList, Favorite
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BooksSerializer, GenresSerializer, AuthorsSerializer, CommentsSerializer, FavoritesSerializer
from django.contrib.auth.models import User
from .admin import BookResource
from django.http import HttpResponse
from django.db.models import Q


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
    queryset = Book.objects.select_related('author')
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genre', 'year', 'author']
    search_fields = ['book_name', 'annotation']
    ordering_fields = ['year']

    @action(methods=['get'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def favorite_books_for_user(self, request):
        user = request.user
        favorites = FavoritesSerializer(Favorite.objects.filter(user_id=user.id), many=True)
        return Response(favorites.data)
    
    @action(methods=['post', 'get'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def add_book_to_favorite(self, request, pk):
        answer = {'answer': []}
        user = request.user
        book = Book.objects.get(pk=pk)
        if book:
            if book.in_favorite():
                answer['answer'] += ['Книга уже добавлена в список любимых']
            else:
                if book.in_black_list():
                    BlackList.objects.get(user=user, book=book).delete()
                    answer['answer'] += ['Книга успешно удалена из черного списка']
                favorite = Favorite(user=user, book=book)
                favorite.save()
                answer['answer'] += ['Книга успешно добавлена в список любимых']
        else:
            answer['answer'] += ['Книга не добавлена в список любимых']
        return Response(answer)
        
    @action(methods=['delete', 'get'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def delete_book_from_favorite(self, request, pk):
        user = request.user
        favorite = Favorite.objects.get(user=user, book=pk)
        if not favorite:
            return Response({'answer': 'Книга не добавлена в список любимых'})
        favorite.delete()
        return Response({'answer': 'Книга успешно удалена из списка любимых'})
        

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

    @action(methods=['get'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def my_comments(self, request):
        user = request.user
        comments = Comment.objects.filter(Q(author=user) & ~Q(is_hide=True))
        return Response(CommentsSerializer(comments, many=True).data)
    
    @action(methods=['get'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def other_comments(self, request):
        user = request.user
        comments = Comment.objects.filter(~Q(author=user) & ~Q(is_hide=True) & (Q(created_at__lte='2023-06-26') | Q(created_at__lte='2023-06-27')))
        return Response(CommentsSerializer(comments, many=True).data)



def export_from_admin(request):
    book_resource = BookResource()
    data_set = book_resource.export()
    response = HttpResponse(data_set.json, content_type='application/json')

    return response