from django.contrib import admin

# Register your models here.
from . import models as m

admin.site.register(m.Author, m.AuthorAdmin)
admin.site.register(m.Genre, m.GenreAdmin)
admin.site.register(m.Comment, m.CommentAdmin)
admin.site.register(m.Book, m.BookAdmin)
admin.site.register(m.Favorite, m.FavoritesAdmin)
admin.site.register(m.BlackList, m.BlackListAdmin)
admin.site.register(m.Like, m.LikeAdmin)
admin.site.register(m.Dislike, m.DislikeAdmin)
