from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from os import sep
from simple_history.models import HistoricalRecords



# Классы моделей для базы данных
class Genre(models.Model):
    genre_name = models.CharField(max_length=200, verbose_name="Название")
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.genre_name}'
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Author(models.Model):
    firstname = models.CharField(max_length=200, verbose_name='Имя')
    lastname = models.CharField(max_length=200, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=200, verbose_name='Отчество')
    image = models.ImageField(upload_to=f'images/authors/', default='images/authors/default.png', verbose_name='Фотография')
    description =  models.TextField(null=True, verbose_name='Описание')
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.lastname} {self.firstname} {self.patronymic}'
    
    class Meta:
        verbose_name = "Автора"
        verbose_name_plural = "Авторы"


class Book(models.Model):
    ''' Класс, описывающий структуру и поведение модели книги '''
    book_name = models.CharField(max_length=200, verbose_name='Название')
    author = models.ForeignKey(Author, on_delete=models.PROTECT, verbose_name='Автор')
    image = models.ImageField(upload_to=f'images/book_faces/', default='images/book_faces/default.png', verbose_name='Изображение обложки')
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, verbose_name='Жанр')
    year = models.IntegerField(verbose_name='Год издания')
    rating = models.IntegerField(default=0,  verbose_name='Рейтинг')
    annotation = models.TextField(null=True, verbose_name='Описание')
    history = HistoricalRecords()

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
    
    class Meta:
        verbose_name = "Книгу"
        verbose_name_plural = "Книги"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    text = models.TextField(verbose_name='Содержание')
    created_at = models.DateField(null=True, auto_now_add=True, verbose_name='Дата написания')

    def __str__(self):
        return f'Комментарий пользователя ({self.author_id}) к книге ({self.book_id})'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')

    def get_book(self):
        return Book.objects.get(pk=self.book.id)

    def __str__(self):
        return f'User: {self.user}\nBook: {self.book}'
    
    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Список любимых книг"


class BlackList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')

    def get_book(self):
        return Book.objects.get(pk=self.book.id)

    def __str__(self):
        return f'User: {self.user}\nBook: {self.book}'
    
    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Черный список"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')

    class Meta:
        verbose_name = "Дизлайк"
        verbose_name_plural = "Дизлайки"
