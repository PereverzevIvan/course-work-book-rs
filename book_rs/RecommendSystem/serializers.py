from rest_framework import serializers
from .models import Book, Genre, Author, Comment, Favorite
from django.contrib.auth.models import User
from rest_framework.validators import UniqueTogetherValidator


# Основной задачей Serializer является представление
# данных, имеющихся в БД, в понятном браузеру формате -
# в формате файла JSON
class BooksSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ("pk", "book_name", "author", "genre", "year", "annotation")

    def get_author(self, book):
        return book.author.firstname


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("pk", "genre_name")
        validators = [
            UniqueTogetherValidator(queryset=Genre.objects.all(), fields=["genre_name"])
        ]


class AuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("pk", "lastname", "firstname", "patronymic", "description")


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("pk", "author", "book", "text", "created_at")


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ("pk", "user", "book")
