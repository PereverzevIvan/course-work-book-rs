from django.urls import path, include
from rest_framework import routers
from . import views, api_views

# В данном случае router нужен для того, чтобы автоматизировать процесс
# создания маршрутов для вызова методов зарегистрированных представлений.
#
# Например, при использовании класса DefaultRouter роутер создает
# три группы маршрутов для каждого зарегистрированного представления:
#   1) api/v1/<прейикс> - для получения списка записей и добавления новой
#   2) api/v1/<префикс>/pk - для получения/удаления/изменения конкретной записи
#   3) api/v1/ - для получения всех имеющихся в роутере маршрутов

router = routers.DefaultRouter()
router.register(r"books", api_views.BooksViewSet)
router.register(r"genres", api_views.GenresViewSet)
router.register(r"authors", api_views.AuthorsViewSet)
router.register(r"comments", api_views.CommentsViewSet)

app_name = "RS"
urlpatterns = [
    path("", views.index, name="index"),
    path("all_books/<int:page_no>/", views.show_all_books, name="show_all_books"),
    path("one_book/<int:book_id>/", views.show_one_book, name="show_one_book"),
    path("all_authors/<int:page_no>/", views.show_all_authors, name="show_all_authors"),
    path("one_author/<int:author_id>/", views.show_one_author, name="show_one_author"),
    path("serach_books/<int:page_no>/", views.search_books, name="search_books"),
    path("serach_authors/<int:page_no>/", views.search_authors, name="search_authors"),
    path("favorite/<int:page_no>/", views.show_favorites_of_user, name="favorite"),
    path("add_favorite/<int:book_id>/", views.add_favorite, name="add_favorite"),
    path(
        "delete_favorite/<int:book_id>/", views.delete_favorite, name="delete_favorite"
    ),
    path("black_list/<int:page_no>/", views.show_black_list, name="black_list"),
    path("add_black_list/<int:book_id>/", views.add_black_list, name="add_black_list"),
    path(
        "delete_black_list/<int:book_id>/",
        views.delete_black_list,
        name="delete_black_list",
    ),
    path("add_comment/<int:book_id>/", views.add_comment, name="add_comment"),
    path(
        "delete_comment/<int:comment_id>/", views.delete_comment, name="delete_comment"
    ),
    path(
        "books_of_author/<int:author_id>/<int:page_no>",
        views.show_author_books,
        name="books_of_author",
    ),
    path("like/<int:book_id>/", views.add_like, name="like"),
    path("dislike/<int:book_id>/", views.add_dislike, name="dislike"),
    path("api/v1/", include(router.urls)),
    path("api/v1/export", api_views.export_from_admin, name="export_from_admin"),
]

handler404 = "RecommendSystem.views.error_404"
