from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from library_app.models import Book, Author, BookBorrows, UserProfile
from library_app.api.serializers import UserSerializer, BookSerializer, AuthorSerializer, BookBorrowsSerializer


"""
This function is used to manage the list of users. 
It supports two operations:
1. GET: Retrieve a list of all existing users.
2. POST: Add a new user to the system.
"""

class UsersList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = UserProfile.objects.select_related('user').all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            
            user_data = serializer.validated_data['user']
            is_librarian = serializer.validated_data['is_librarian']
            
            if User.objects.filter(username=user_data['username']).exists():
                return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
           
            user = User.objects.create(
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            UserProfile.objects.create(user=user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    

"""
This function is used to retrieve and validate a specific user.
""" 
class SpecificUser(APIView):
    def get(self, request, pk):
        try:            
            users = UserProfile.objects.select_related('user').get(pk = pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(users)
        return Response(serializer.data, status=status.HTTP_200_OK)    


"""This function is used to manage the list of books."""
class BookList(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


"""
This function handles retrieving, updating, and deleting a book based on the provided pk.

- GET: Retrieves the details of a book identified by the primary key (pk).
- PUT: Updates the details of the book identified by the pk with the provided data.
- DELETE: Deletes the book identified by the pk from the database.

"""           
class BookDetails(APIView):  
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, pk): 
        book = self.get_object(pk)   
        serializer = BookSerializer(book) 
        return Response(serializer.data)
    
    def put(self, request, pk): 
        book = self.get_object(pk) 
        serializer = BookSerializer(book, data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        book = self.get_object(pk) 
        book.delete()
        return Response({'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)             
    

"""This function is used to manage the list of books."""           

class AuthorList(APIView): 
    def get(self,request):
            
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
       
        
"""
This function creates a new book for a specific author.

It accepts the primary key (pk) of an author to associate the book with that author.
If the author exists, a new book is created with the provided details. If the author 
does not exist, an error message is returned.
"""    

class CreateBoolForAuthor(APIView):
    def post(self, request, pk):        
        try:
            author = Author.objects.get(id=pk)
        except Author.DoesNotExist:
            return Response({'error': 'Author not found.'}, status=status.HTTP_404_NOT_FOUND)
    
        
        serializer = BookSerializer(data = request.data)
                
        if serializer.is_valid():
            
            Book.objects.create(
                book_name=serializer.validated_data['book_name'],
                description=serializer.validated_data.get('description', ''),
                author=author
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       
        
   
"""
This function retrieves, updates, or deletes books related to a specific author identified by the pk.

- GET: Retrieves a list of books associated with the author identified by pk.
- PUT: Updates a specific book by its ID for the author identified by pk. The book ID must be provided in the request data.
- DELETE: Deletes all books related to the author identified by pk.

"""    
class AuthorBooksDetailView(APIView):
    
    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, pk):
        author = self.get_object(pk)          
        books = Book.objects.filter(author=author) 
        serializer = BookSerializer(books,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        author = self.get_object(pk)   
        book_id = request.data.get('id')
        if not book_id:
            return Response(
                {'error': 'Book ID is required to update.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        books = Book.objects.get(id = book_id , author=author) 
        serializer = BookSerializer(books,data= request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        
    def delete(self, request, pk):
        author = self.get_object(pk) 
        books = Book.objects.filter(author=author)   
        books.delete()
        return Response({'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)        

    
"""This function is used to manage the list of book borrows."""    
class BookBorrowsList(APIView):
    def get(self, request):   
        bookborrows = BookBorrows.objects.all()
        serializer = BookBorrowsSerializer(bookborrows, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


"""This function is used to manage the list of specific book borrows user."""    
class SpecificUserBookBorrows(APIView):
    def get(self, request, pk):   

        user = UserProfile.objects.select_related('user').get(pk = pk)
        bookborrows = BookBorrows.objects.filter(user = user)
        serializer = BookBorrowsSerializer(bookborrows, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

"""
This function handles updating the status of a specific book borrow request.

- GET: Retrieves the details of a book borrow request by its primary key (pk).
- PUT: Updates the status of the book borrow request identified by pk.
       The new status should be provided in the request data, and it must be either 'approved' or 'denied'.

"""   
class BookBorrowsUpdateStatus(APIView):
    
    def get_object(self, pk):
        try:
            return BookBorrows.objects.get(pk=pk)
        except BookBorrows.DoesNotExist:
            raise Response({'error': 'BookBorrow not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
    def get(self,request, pk):         
    
        bookborrows = self.get_object(pk)
        serializer = BookBorrowsSerializer(bookborrows)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        
        bookborrows = self.get_object(pk)
        
        new_status = request.data.get('status')
        
        if new_status in ['approved', 'denied']:
            bookborrows.status = new_status
            bookborrows.save()
            return Response({'message': 'Book borrow status updated successfully'}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid status"}, status=400)



class CreateNewBook(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            author_name = request.data.get('author')
             # Check if the author exists
            author, created = Author.objects.get_or_create(
                author_name=author_name,
                defaults={'publication_year': request.data.get('publication_year', 0)}
            )
            
            if not created:
                return Response({'error': 'Author already exists'}, status=status.HTTP_400_BAD_REQUEST)
           
            book = Book.objects.create(
            book_name=serializer.validated_data.get('book_name'),
            description=serializer.validated_data.get('description', ''),
            author= author
            )     
            response_serializer = BookSerializer(book)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)