from django.contrib import admin
from library_app.models import Book, Author, BookBorrows, UserProfile

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(BookBorrows)
admin.site.register(UserProfile)