from django.urls import path
from library_app.api import views

urlpatterns = [
    
    path('user_list/', views.UsersList.as_view(), name= 'user-list'),    
    path('user/<int:pk>/', views.SpecificUser.as_view(), name= 'specific_user'),  
      
    path('book_list/', views.BookList.as_view(), name= 'book-list'),    
    path('book_details/<int:pk>', views.BookDetails.as_view(), name= 'book-details'),  
    
    path('author_list/', views.AuthorList.as_view(), name= 'author-list'),
    path('authors/<int:pk>/create_book_for_author/', views.CreateBoolForAuthor.as_view(), name='create-book-for-author'),
    path('author_books_details/<int:pk>', views.AuthorBooksDetailView.as_view(), name= 'author-books-details'),
    
    path('BookBorrows_list/', views.BookBorrowsList.as_view(), name= 'BookBorrows-list'),
    path('specific_user_BookBorrows/<int:pk>', views.SpecificUserBookBorrows.as_view(), name= 'specific-user-BookBorrows'),
    path('update_book_borrow/<int:pk>', views.BookBorrowsUpdateStatus.as_view(), name= 'update-book-borrow'),    
    
    path('create_book/', views.CreateNewBook.as_view(), name= 'Create-New-Book'), 
    
]