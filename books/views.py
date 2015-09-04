import re
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from books.forms import BookForm
from .models import Book, Author, Genre
from .forms import BookForm, AuthorForm, GenreForm, BookFormUpdate
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import UserProfile

class BookList(ListView):
    model = Book
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BookList, self).dispatch(*args, **kwargs)
        
    def get_queryset(self):
        curruser = UserProfile.objects.get(user=self.request.user)
        author = self.kwargs['author']
        if author == '':
            self.queryset = Book.objects.filter(user=curruser)
            return self.queryset
        else:
            self.queryset = Book.objects.all().filter(user=curruser).filter(author__title__iexact=author)
            return self.queryset
            
    def get_context_data(self, **kwargs):
        context = super(BookList, self).get_context_data(**kwargs)
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context
        
class BookCreate(CreateView):
    model = Book
    form_class = BookForm
    
class BookUpdate(UpdateView):
    model = Book
    form_class = BookForm
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BookUpdate, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(BookUpdate, self).get_context_data(**kwargs)
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context

class BookDetail(DetailView):
    model = Book

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BookDetail, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(BookDetail, self).get_context_data(**kwargs)
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('list')
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BookDelete, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(BookDelete, self).get_context_data(**kwargs)
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context

class BookByGenre(ListView):
    model = Book
    
    queryset = Book.objects.all()
    def get_queryset(self):
        genre = self.kwargs['genre']
        pieces = genre.split('/') 
        
        queries = [Q(genre__title__iexact=value) for value in pieces]
        query = queries.pop()
        for item in queries:
            query |= item
        curruser = UserProfile.objects.filter(user=self.request.user) 
        allbooks = Book.objects.filter(user=curruser).filter(query).distinct().order_by('genre__title')
        self.queryset = allbooks 
        return allbooks
    
    def get_context_data(self, **kwargs):
        context = super(BookByGenre, self).get_context_data(**kwargs)
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context

class MyView(TemplateView):
    author_form_class = AuthorForm
    genre_form_class = GenreForm
    book_form_class = BookForm
    template_name = "books/book_hybrid.html"
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MyView, self).dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        kwargs.setdefault("createauthor_form", self.author_form_class())
        kwargs.setdefault("creategenre_form", self.genre_form_class())
        kwargs.setdefault("createbook_form", self.book_form_class())
        kwargs.setdefault('curruser', UserProfile.objects.get(user=self.request.user))
        return super(MyView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form_args = {
            'data': self.request.POST,
        }
        
        if "btn_createauthor" in request.POST['form']: 
            form = self.author_form_class(**form_args)
            if not form.is_valid():
                response_dict = {}
                response_dict['status'] = 0
                response_dict['message'] = form.errors.as_ul()
                return HttpResponse(json.dumps(response_dict, cls=DjangoJSONEncoder))
            else:
                form.save()
                data = Author.objects.all()
                response_dict = {'status': 1}
                response_dict['message'] = list(data.values('id','title'))
                return HttpResponse(json.dumps(response_dict, cls=DjangoJSONEncoder))
        elif "btn_creategenre" in request.POST['form']: 
            form = self.genre_form_class(**form_args)
            if not form.is_valid():
                response_dict = {}
                response_dict['status'] = 0
                response_dict['message'] = form.errors.as_ul()
                return HttpResponse(json.dumps(response_dict, cls=DjangoJSONEncoder))
            else:
                form.save() 
                data = Genre.objects.all() 
                response_dict = {'status': 1}
                response_dict['message'] = list(data.values('id','title'))
                return HttpResponse(json.dumps(response_dict, cls=DjangoJSONEncoder)) 
        elif "btn_createbook" in request.POST['form']:
            form = self.book_form_class(**form_args)
            if not form.is_valid():
                response_dict = {}
                response_dict['status'] = 0
                response_dict['message'] = form.errors.as_ul()
                return HttpResponse(json.dumps(response_dict, cls=DjangoJSONEncoder))
            else:
                try:
                    curruser = UserProfile.objects.get(user=self.request.user)
                    obj = form.save(commit=False)
                    obj.user = curruser 
                    obj.save() 
                    
                except Exception, e:
                    print("errors" + str(e))
                response = {'status': 1, 'message':'ok'}
                return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder)) 
            
        return super(MyView, self).get(request)