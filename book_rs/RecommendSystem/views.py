from django.shortcuts import render
from django.shortcuts import HttpResponse, get_object_or_404
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

    
def show_all_books(request):
    books_list = Book.objects.all()
    
    return render(request, 'show_all_books.html', {'books_list': books_list})


def show_one_book(request, book_id: int):
    book = get_object_or_404(Book, pk=book_id)

    return render(request, "show_one_book.html", {"book": book})


def user_profile(request, user_id: int):
    user = get_object_or_404(User, pk=user_id)

    return render(request, "user_profile.html", {"user": user})

def show_all_authors(request):
    authors_list = Author.objects.all()

    return render(request, 'show_all_authors.html', {'authors_list': authors_list})

def show_one_author(request, author_id: int):
    author = get_object_or_404(Author, pk=author_id)

    return render(request, 'show_one_author.html', {'author': author})

def registration():
    pass


def authorization():
    pass

def error_404(request, exception):
    data = {
        'exception': exception
    }
    return render(request,'404.html', data)