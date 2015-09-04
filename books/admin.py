from django.contrib import admin
from .models import Book, Author, Genre

class BookInline(admin.StackedInline): 
    model = Book
    fields = ('title',) 
    extra = 0
    
class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline,]
    model = Author

class GenreBookInline(admin.TabularInline): 
    model = Book.genre.through
    extra = 0
    
class GenreAdmin(admin.ModelAdmin):
    inlines = [GenreBookInline,]
    model = Genre

admin.site.register(Book)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Author, AuthorAdmin)