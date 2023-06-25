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
    book_name = models.CharField(max_length=200, verbose_name='Название')
    author = models.ForeignKey(Author, on_delete=models.PROTECT, verbose_name='Автор')
    image = models.ImageField(upload_to=f'images/book_faces/', default='images/book_faces/default.png', verbose_name='Изображение обложки')
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, verbose_name='Жанр')
    year = models.IntegerField(verbose_name='Год издания')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    annotation = models.TextField(null=True, verbose_name='Описание')

    def get_author(self):
        author = Author.objects.get(pk=self.author.pk)
        return f'{author.firstname} {author.lastname}'
    
    def in_black_list(self, user_id:int):
        return bool(BlackList.objects.filter(user_id=user_id, book_id=self.id))
    
    def in_favorite(self, user_id:int):
        return bool(Favorite.objects.filter(user_id=user_id, book_id=self.id))
    
    def was_liked(self, user_id):
        return bool(Like.objects.filter(user_id=user_id, book_id=self.id))
    
    def was_disliked(self, user_id):
        return bool(Dislike.objects.filter(user_id=user_id, book_id=self.id))

    def __str__(self):
        return f'{self.book_name}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateField(null=True, auto_now_add=True)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def get_book(self):
        return Book.objects.get(pk=self.book.id)

    def __str__(self):
        return f'User: {self.user}\nBook: {self.book}'


class BlackList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def get_book(self):
        return Book.objects.get(pk=self.book.id)

    def __str__(self):
        return f'User: {self.user}\nBook: {self.book}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


# Классы для корректного отображения моделей в админке
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'genre_name')
    list_filter = ('id', 'genre_name')
    search_fields = ['genre_name']

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'patronymic')
    list_filter = ('id', 'firstname', 'lastname', 'patronymic')
    search_fields = ['firstname', 'lastname', 'patronymic']

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'book_name', 'author', 'genre', 'year', 'rating')
    list_filter = ('id', 'book_name', 'author', 'genre', 'year')
    search_fields = ['book_name']

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'book', 'created_at')
    list_filter = ('id', 'author', 'book', 'created_at')

class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book')
    list_filter = ('id', 'user')

class BlackListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book')
    list_filter = ('id', 'user')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book')
    list_filter = ('id', 'user')

class DislikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book')
    list_filter = ('id', 'user')
