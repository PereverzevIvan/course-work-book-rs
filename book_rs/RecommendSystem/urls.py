from django.urls import path, include
from . import views

app_name = 'RS'
urlpatterns = [
    path("", views.index, name="index"),
    path('all_books/<int:page_no>/', views.show_all_books, name='show_all_books'),
    path('one_book/<int:book_id>/', views.show_one_book, name='show_one_book'),
    path('all_authors/<int:page_no>/', views.show_all_authors, name='show_all_authors'),
    path('one_author/<int:author_id>/', views.show_one_author, name='show_one_author'),
    path('serach_books/<int:page_no>/', views.search_books, name='search_books'),
    path('serach_authors/<int:page_no>/', views.search_authors, name='search_authors'),
    path('favorite/<int:page_no>/', views.show_favorites_of_user, name="favorite"),
    path('add_favorite/<int:book_id>/', views.add_favorite, name="add_favorite"),
    path('delete_favorite/<int:book_id>/', views.delete_favorite, name="delete_favorite"),
    path('add_comment/<int:book_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]

handler404 = 'RecommendSystem.views.error_404'
