from django.contrib.admin.decorators import register
from catalog.models import Autor, Book, BookInstance, Genre, Language
from django.contrib import admin
from .models import Autor, Genre, Book, BookInstance, Language

# Register your models here.
#admin.site.register(Book)
#admin.site.register(Autor)
admin.site.register(Genre)
admin.site.register(Language)
#admin.site.register(BookInstance)

#Listas encadenadas
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    
class BooksInline(admin.TabularInline):
    model = Book
    
#Define la class Admin
class AutorAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'fecha_nacimiento', 'fecha_muerte')
    fields = ['nombre', 'apellido', ('fecha_nacimiento', 'fecha_muerte')]
    inlines = [BooksInline]

#Registra la clase Admin con el modelo asociado
admin.site.register(Autor, AutorAdmin)

#Registra las clases Admin para Book ysabdi el decorador
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'display_genre')
    inlines = [BooksInstanceInline]

#Registra la clase Admin para BookInstance usando el decorador
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('libro', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    
    fieldsets = (
        (None, {
            'fields': ('libro', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

