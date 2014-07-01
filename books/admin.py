from django.contrib import admin
from books.models import Publisher, Author, Book, Journal, Publication

class AuthorAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'email')

admin.site.register(Publisher)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book)
admin.site.register(Publication)
admin.site.register(Journal)
# Register your models here.
