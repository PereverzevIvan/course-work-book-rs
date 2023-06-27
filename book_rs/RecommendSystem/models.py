from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from os import sep
from django.utils.safestring import mark_safe


# Классы моделей для базы данных
class Genre(models.Model):
    genre_name = models.CharField(max_length=200, verbose_name="Название")

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


# Классы для корректного отображения моделей в админке
class BookInlines(admin.TabularInline):
    model = Book

    fields = ['book_name', 'image', 'genre', 'year', 'annotation']


class FavoriteInlines(admin.TabularInline):
    model = Favorite

    fields = ['user']
    readonly_fields = ['user']


class BlackListInlines(admin.TabularInline):
    model = BlackList

    fields = ['user']
    readonly_fields = ['user']


class LikeInlines(admin.TabularInline):
    model = Like

    fields = ['book']
    readonly_fields = ['book']


class DislikeInlines(admin.TabularInline):
    model = Dislike

    fields = ['book']
    readonly_fields = ['book']


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'genre_name')
    list_display_links = ('id', 'genre_name')
    search_fields = ['genre_name']

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_fio', 'get_photo')
    list_display_links = ('id', 'get_fio')
    search_fields = ['firstname', 'lastname', 'patronymic']

    inlines = [BookInlines]

    def get_fio(self, object):
        return f'{object.firstname} {object.lastname} {object.patronymic}'

    def get_photo(self, object):
        return mark_safe(f'<img src="/static/{object.image}" width=70>')
    
    get_photo.short_description = 'Фотография'
    get_fio.short_description = 'ФИО'

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'book_name', 'author', 'genre', 'year', 'get_photo')
    list_display_links = ('id', 'book_name')
    list_filter = ('genre', 'year')
    readonly_fields = ['rating']
    search_fields = ['book_name', 'author__firstname', 'author__lastname', 'author__patronymic']
    raw_id_fields = ['author']

    inlines = [FavoriteInlines]

    def get_photo(self, object):
        return mark_safe(f'<img src="/static/{object.image}" width=70>')
    
    get_photo.short_description = 'Обложка'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'book', 'created_at')
    fields = ['author', 'book', 'text', 'created_at']
    readonly_fields = ['author', 'book', 'created_at']
    list_filter = ['created_at']
    search_fields = ['text']
    date_hierarchy = "created_at"

class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book')
    readonly_fields = ['user', 'book']
    search_fields = ['user__username', 'book__book_name']

class BlackListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book')
    readonly_fields = ['user', 'book']
    search_fields = ['user__username', 'book__book_name']

class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book')
    readonly_fields = ['user', 'book']
    search_fields = ['user__username', 'book__book_name']

class DislikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book')
    readonly_fields = ['user', 'book']
    search_fields = ['user__username', 'book__book_name']
