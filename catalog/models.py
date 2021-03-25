from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


import uuid  # Se requiere para las instancias de libros únicos

# CREATE YOUR MODELS HERE.
# Modelo Genre
class Genre(models.Model):
    # Modelo que representa un género literario
    nombre = models.CharField(
        max_length=200, help_text="Ingrese el género al que pertenece el libro")

    def __str__(self):
        # Cadena que representa a la instancia particular del modelo
        return self.nombre

# Modelo Language
class Language(models.Model):
    language = models.CharField(max_length=200)

    def __str__(self):
        return self.language

# Modelo Book
class Book(models.Model):
    # Modelo que representa un libro pero no un ejemplar específico
    titulo = models.CharField(max_length=200)

    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True)
    # ForeignKey ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros
    # 'Autor' es un string en lugar de un objeto, porque la clase Autor aún no ha sido declarada

    descripcion = models.TextField(
        max_length=1000, help_text="Ingrese una breve descripción del libro")

    isbn = models.CharField(
        'ISBN', max_length=13, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genero = models.ManyToManyField(
        Genre, help_text="Seleccione un genero para este libro")
    # ManyToManyField porque un género puede contener muchos libros y un libro puede cubrir varios géneros
    # La clase Genre ya ha sido definida, por eso se puede especificar el objeto

    languaje = models.ManyToManyField(
        Language, help_text="Selecciona el lenguaje para este libro")
    #languaje = models.CharField(Language, max_length=200, help_text="Selecciona el lenguaje para este libro")

    def __str__(self):
        # String que representa el objeto Book
        return self.titulo

    def get_absolute_url(self):
        # Devuelve el URL a una instancia particular de Book
        # return reverse('book_detail', args=[str(self.id)])
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        # Crea una cadena para los generos. Es requerida para mostrar los generos en Admin.
        return ','.join([genre.nombre for genre in self.genero.all()[:3]])

    '''
    def display_language(self):
        #Crea una cadena para los generos. Es requerida para mostrar los generos en Admin.
        return ','.join([lang.language for lang in self.language.all()[:3]])
    '''

    display_genre.short_description = 'Genre'
    #display_language.short_description = 'Language'

# Modelo BookInstance
class BookInstance(models.Model):
    # Modelo que representa una copia específica de un libro (Puede ser prestado por la biblioteca)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca")

    libro = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)

    imprint = models.CharField(max_length=200)

    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Mantenimiento'),
        ('p', 'Prestamo'),
        ('d', 'Disponible'),
        ('r', 'Reservado'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text='Disponibilidad del libro')

    class Meta:
        ordering = ["due_back"]
        
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        # String para representar el objeto del modelo
        return '%s (%s)' % (self.id, self.libro.titulo)
    
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

# Modelo Autor
class Autor(models.Model):
    # Modelo que representa un autor
    nombre = models.CharField(max_length=100)

    apellido = models.CharField(max_length=100)

    fecha_nacimiento = models.DateField(null=True, blank=True)

    fecha_muerte = models.DateField('died', null=True, blank=True)

    def get_absolute_url(self):
        # Retorna la URL para acceder a una instancia particular de un autor
        return reverse('autor-detail', args=[str(self.id)])

    def __str__(self):
        # String para representar el Objeto Modelo
        return '%s, %s' % (self.apellido, self.nombre)

    class Meta:
        ordering = ['apellido']
