from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('Hello, World!')
    
def show_books(request):
    return HttpResponse('СТраница простомтра книг')