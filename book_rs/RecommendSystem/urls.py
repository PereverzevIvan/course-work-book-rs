from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('books/', views.show_books, name='show_books')
]