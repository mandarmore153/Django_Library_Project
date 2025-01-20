from django.contrib.auth.models import User
from rest_framework import serializers
from library_app.models import Book, Author, BookBorrows, UserProfile


class UserSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    is_librarian = serializers.BooleanField()
    
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_librarian')    
        
        
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'author_name', 'publication_year']   
    
            
class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    
    class Meta:
        model = Book
        fields = ['id', 'book_name', 'description', 'author']
        
        
        
class BookBorrowsSerializer(serializers.ModelSerializer):
    
    user_name = serializers.CharField(source='user.username')  
    book_name = serializers.CharField(source='book.book_name')
    
    class Meta:
        model = BookBorrows
        fields = ['id', 'user_name', 'book_name', 'borrow_date', 'return_date', 'status']
    
    
    # below code returns the entire user and book data in bookborrow
    # user = UserSerializer()  
    # book = BookSerializer()
    # class Meta:
    #     model = BookBorrows
    #     fields = '__all__'
      
                