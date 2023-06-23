from django.urls import path
from . import views

app_name = 'RS'
urlpatterns = [
    path("", views.index, name="index"),
    path('user/<int:user_id>/', views.user_profile, name='check_user_profile'),
    path('all_books/<int:page_no>/', views.show_all_books, name='show_all_books'),
    path('one_book/<int:book_id>/', views.show_one_book, name='show_one_book'),
    path('registration/', views.registration, name='registration'),
    path('authorization/', views.authorization, name='authorization'),
    path('all_authors/<int:page_no>/', views.show_all_authors, name='show_all_authors'),
    path('one_author/<int:author_id>/', views.show_one_author, name='show_one_author'),
    path('serach_books/<int:page_no>/', views.search_books, name='search_books'),
    path('serach_authors/<int:page_no>/', views.search_authors, name='search_authors')
]

handler404 = 'RecommendSystem.views.error_404'
