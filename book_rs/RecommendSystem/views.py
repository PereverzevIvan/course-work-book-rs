from django.shortcuts import render
from django.shortcuts import HttpResponse, get_object_or_404, HttpResponsePermanentRedirect
from .models import *
from math import ceil
from django.contrib import auth
from django.urls import reverse

# Вспомогательные функции
def get_context_for_pagination(arr: list, page_no: int, cards_count: int):
    maybe_pages = ceil(len(arr) / cards_count)
    page_no = max(1, page_no)
    page_no = min(maybe_pages, page_no)
    next_page = page_no if page_no + 1 > maybe_pages else page_no + 1
    prev_page = page_no if page_no - 1 < 1 else page_no - 1

    context = {
        'page_no': page_no,
        'maybe_pages': maybe_pages,
        'next_page': next_page,
        'prev_page': prev_page,
        'all_objects': len(arr),
        'objects_list': arr[cards_count*(page_no-1):cards_count*page_no]
        }

    return context

# Функции представлений
def index(request):
    ''' Главная страница '''
    return render(request, 'index.html')

    
def show_all_books(request, page_no=1):
    ''' Просмтор всех имеющихся в БД книг '''
    books_list = list(Book.objects.all())
    context = get_context_for_pagination(books_list, page_no, 12)
    context['cur_url'] = 'RS:show_all_books'

    return render(request, 'show_all_books.html', context)


def show_one_book(request, book_id: int):
    ''' Просмотр профиля отдельной книги '''
    book = get_object_or_404(Book, pk=book_id)
    comments = Comment.objects.filter(book_id=book.id)

    return render(request, "show_one_book.html", {"book": book, 'comments': comments})


def user_profile(request, user_id: int):
    ''' Просмотр профиля авторизованного пользователя '''
    user = get_object_or_404(User, pk=user_id)

    return render(request, "user_profile.html", {"user": user})

def show_all_authors(request, page_no=1):
    ''' Просмотр всех авторов, имеющихся в БД '''
    authors_list = list(Author.objects.all())
    context = get_context_for_pagination(authors_list, page_no, 16)
    context['cur_url'] = 'RS:show_all_authors'

    return render(request, 'show_all_authors.html', context)

def show_one_author(request, author_id: int):
    ''' Просмотр профиля отдельного автора '''
    author = get_object_or_404(Author, pk=author_id)

    return render(request, 'show_one_author.html', {'author': author})

def search_books(request, page_no: int):
    ''' Просмотр страницы с найденными по запросу книгами '''
    text = request.GET.get('text')
    books = list(Book.objects.filter(book_name__iregex=text))
    context = get_context_for_pagination(books, page_no, 15)
    context['cur_url'] = 'RS:search_books'
    context['search_text'] = text

    return render(request, 'show_all_books.html', context)

def search_authors(request, page_no: int):
    ''' Просмотр страницы с найденными по запросу книгами '''
    text = request.GET.get('text')
    authors = list(Author.objects.filter(firstname__iregex=text) | Author.objects.filter(lastname__iregex=text) | Author.objects.filter(patronymic__iregex=text))
    context = get_context_for_pagination(authors, page_no, 16)
    context['cur_url'] = 'RS:search_authors'
    context['search_text'] = text

    return render(request, 'show_all_authors.html', context)


def show_favorites_of_user(request, user_id:int):
    user = request.user
    if user.is_authenticated:
        if user.id != user_id:
            return render(request, 'error.html', {'error_title': 'Ошибка доступа', 
                                                  'error_text': 'Вы не можете получить доступ к этому ресурсу'})
        
        books_id = list(Favorite.objects.filter(user_id=user_id))
        return HttpResponse(books_id)
    else:
        return render(request, 'error.html', {'error_title': 'Ошибка доступа', 
                                                  'error_text': 'Вы не можете получить доступ к этому ресурсу'})


def add_comment(request, book_id:int):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated and get_object_or_404(Book, pk=book_id):
            comment = Comment()
            comment.book_id = book_id
            comment.author_id = user.id
            comment.text = request.POST.get('comment-text')
            comment.save()
            return HttpResponsePermanentRedirect(reverse('RS:show_one_book', kwargs={'book_id': book_id}))
        else:
            return render(request, 'error.html', {'error_title': 'Ошибка добавления', 
                                                  'error_text': 'Не удалось добавить комментарий'})
    

def delete_comment(request, comment_id:int):
    comment = get_object_or_404(Comment, pk=comment_id)
    book_id = comment.book_id
    user = request.user

    if user.is_authenticated and comment.author_id == user.id:
        comment.delete()
        return HttpResponsePermanentRedirect(reverse('RS:show_one_book', kwargs={'book_id': book_id}))
    return render(request, 'error.html', {'error_title': 'Ошибка удаления', 
                                                  'error_text': 'Вы не можете удалить комментарий другого человека'})



def error_404(request, exception):
    data = {
        'exception': exception
    }
    return render(request,'404.html', data)