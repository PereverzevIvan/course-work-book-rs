from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from os import sep

# Классы моделей для базы данных
class Genre(models.Model):
    genre_name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.genre_name}'


class Author(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    patronymic = models.CharField(max_length=200)
    image = models.ImageField(upload_to=f'images/authors/', default='images/authors/default.png')
    description =  models.TextField(null=True)

    def __str__(self):
        return f'{self.lastname} {self.firstname} {self.patronymic}'


class Book(models.Model):
    ''' Класс, описывающий структуру и поведение модели книги '''
    book_name = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    image = models.ImageField(upload_to=f'images/book_faces/', default='images/book_faces/default.png')
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    year = models.IntegerField()
    rating = models.IntegerField(default=0)
    annotation = models.TextField(null=True)

    def get_author(self):
        author = Author.objects.get(pk=self.author.pk)
        return f'{author.lastname} {author.firstname}'

    def __str__(self):
        return f'{self.book_name}'


class Comment(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateField(null=True, auto_now_add=True)
    rating = models.IntegerField(default=0)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


class BlackList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


# Классы для корректного отображения моделей в админке
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'genre_name')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'patronymic')

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'book_name', 'author', 'genre', 'year', 'rating')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_id', 'book_id', 'text', 'rating', 'created_at')

class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'book_id')

class BlackListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'book_id')


# Классы для работы с моделями (Maganers)
