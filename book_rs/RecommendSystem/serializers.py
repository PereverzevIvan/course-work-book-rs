from rest_framework import serializers
from .models import Book


# Основной задачей Serializer является представление
# данных, имеющихся в БД, в понятном браузеру формате -
# в формате файла JSON  
class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'pk',
            'book_name',
            'author',
            'genre',
            'year',
            'rating',
            'annotation')
        
    
    
