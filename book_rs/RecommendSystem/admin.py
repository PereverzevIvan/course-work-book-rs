from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from import_export import resources as export_resources, fields as export_fields
from import_export.admin import ExportMixin, ExportActionMixin, ImportExportModelAdmin

# Register your models here.
from .models import Book, Author, Comment, Genre, Favorite, BlackList, Dislike, Like

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

# Классы ресурсов для экспорта из админки
class BookResource(export_resources.ModelResource):
    book_name = export_fields.Field(attribute='book_name', column_name='Название')
    author  = export_fields.Field(attribute='author_id', column_name='Автор')
    genre = export_fields.Field(attribute='genre_id', column_name='Жанр')
    year = export_fields.Field(attribute='year', column_name='Год издания')
    rating = export_fields.Field(attribute='rating', column_name='Рейтинг')
    annotation = export_fields.Field(attribute='annotation', column_name='Аннотация')

    class Meta:
        model = Book
        fields = ('book_name', 'author', 'genre', 'year', 'rating', 'annotation')
        export_order = fields

    def dehydrate_author(self, book):
        author = Author.objects.get(pk=book.author_id)
        return author.__str__()
    
    def dehydrate_genre(self, book):
        genre = Genre.objects.get(pk=book.genre_id)
        return genre.__str__()

    def get_queryset(self):
        query = Book.objects.filter(year__gte=2000)
        return query

    



# Классы моделей-администраторов
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

class BookAdmin(ImportExportModelAdmin, ExportActionMixin, ExportMixin, admin.ModelAdmin):
    list_display = ('id', 'book_name', 'author', 'genre', 'year', 'get_photo')
    list_display_links = ('id', 'book_name')
    list_filter = ('genre', 'year')
    readonly_fields = ['rating']
    search_fields = ['book_name', 'author__firstname', 'author__lastname', 'author__patronymic']
    raw_id_fields = ['author']
    resource_class = BookResource

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


admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Favorite, FavoritesAdmin)
admin.site.register(BlackList, BlackListAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Dislike, DislikeAdmin)
