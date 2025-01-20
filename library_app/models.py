from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')    
    is_librarian = models.BooleanField(default=False)
    
    
class Author(models.Model):
    author_name = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    
    def __str__(self):
        return self.author_name


class Book(models.Model):
    book_name = models.CharField(max_length=255)    
    author = models.ForeignKey(Author, on_delete= models.CASCADE, related_name='books')
    description = models.TextField(blank=True)
    
    
    def __str__(self):
        return self.book_name + " | " + str(self.author)
    
    
class BookBorrows(models.Model):
    
    user = models.ForeignKey(UserProfile, on_delete= models.CASCADE, related_name='borrow_users')
    book = models.ForeignKey(Book, on_delete= models.CASCADE, related_name='book_borrows')
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True)
    status = models.CharField(
        max_length=10,
        choices=[("pending", "Pending"), ("approved", "Approved"), ("denied", "Denied")],
        default="pending"
    )
    
    
    def __str__(self):
        return self.user.user.username + "|" + self.book.book_name + "|" + self.status
         
    


