from rest_framework import serializers
from .models import Book, Genre, Author, Comment
from django.contrib.auth.models import User


# Основной задачей Serializer является представление
# данных, имеющихся в БД, в понятном браузеру формате -
# в формате файла JSON  
class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'pk',
            'book_name',
            'author',
            'genre',
            'year',
            'rating',
            'annotation')
        

class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('pk', 'genre_name')


class AuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('pk',
                  'lastname',
                  'firstname',
                  'patronymic',
                  'description')


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('pk',
                  'author',
                  'book',
                  'text',
                  'created_at')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']