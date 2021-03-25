from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Book, Autor, BookInstance, Genre
from django.views import generic
#Requiere login para vistas basadas en funciones
from django.contrib.auth.decorators import login_required
#Requiere login para vistas basadas en clases
from django.contrib.auth.mixins import LoginRequiredMixin
#permisos para vistas basadas en funciones
from django.contrib.auth.decorators import permission_required
#Permisos para vistas basadas en clases
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import RenewBookForm
import datetime

# Create your views here.

#@login_required
#@permission_required('catalog.can_mark_returned')
#@permission_required('catalog.can_edit')
def index(request):
    #Función vista para la página inicio del sitio.
    
    #Genera Contadores de algunos de los objetos principales
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    #Libros disponibles (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='d').count()
    num_authors = Autor.objects.count() #El 'all()' está implícito por defecto
    
    #Número de géneros
    num_genres = Genre.objects.count()
    
    #Libros con una palabra
    num_books_specified = Book.objects.filter(titulo__contains='the').count()
    
    # Numero de visitas a esta view, como está contado en la variable de sesión.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    #Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request, 'index.html',
        context={'num_books':num_books, 'num_instances':num_instances, 'num_instances_available':num_instances_available, 'num_authors':num_authors, 'num_genres':num_genres, 'num_books_specified':num_books_specified, 'num_visits':num_visits,}
    )

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

'''
class BookListView(generic.ListView):
    model = Book
    #Tu propio nombre para la lista como una plantilla variable
    #context_object_name = 'book_list'
    #Obtiene 5 libros que contengan el titulo "war"
    #queryset = Book.objects.filter(titulo__icontains='the')[:5]
    #Especifica el nombre de plantilla o localización
    #template_name = 'books/my_arbitrary_template_name_list.html'
    
    
    #Obtiene 5 libros que contengan el titulo "war"
    def get_queryset(self):
        return Book.objects.filter(title__icontains='war')[:5]
    
    def get_context_data(self, **kwargs):
        # Primero llama a la implementación base para conseguir un contexto
        context = super(BookListView, self).get_context_data(**kwargs)
        # Obtiene el blog del id y lo añade al contexto 
        context['some_data'] = 'This is just some data'
        return context
'''

class BookListView(generic.ListView):
    model = Book
    paginate_by = 3
    
class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Autor

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Autor
    
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    #permission_required = 'catalog.can_mark_returned'
    # Or multiple permissions
    #permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    # Note that 'catalog.can_edit' is just an example
    # the catalog application doesn't have such permission!

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='p').order_by('due_back')
 
class LoanedBooksByUserStaffListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_staff.html'
    paginate_by = 5
    
    permission_required = 'catalog.can_mark_returned'
    # Or multiple permissions
    #permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    # Note that 'catalog.can_edit' is just an example
    # the catalog application doesn't have such permission!

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='p').order_by('due_back')

#AUTOR
class AuthorCreate(CreateView):
    model = Autor
    fields = '__all__'
    initial={'fecha_muerte':'05/01/2018',}

class AuthorUpdate(UpdateView):
    model = Autor
    fields = ['nombre','apellido','fecha_nacimiento','fecha_muerte']

class AuthorDelete(DeleteView):
    model = Autor
    success_url = reverse_lazy('authors')
    
#BOOK
class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    
class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')