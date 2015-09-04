from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import ListView, DetailView
from books.models import Book, Author, Genre
from books import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^add/$', views.MyView.as_view(), name="book_add"),
    url(r'^genre/(?P<genre>.*)$', views.BookByGenre.as_view(), name='book_listgenre'),
    url(r'^listall/$', ListView.as_view(model=Book), name='list'),
    url(r'^list/(?P<author>.*)$', views.BookList.as_view(), name='books_list'),
    url(r'^book/(?P<pk>\d+)$', views.BookDetail.as_view(),  name='detail'),
    url(r'^book/(?P<pk>\d+)/edit/$', views.BookUpdate.as_view(), name='book_update'),
    url(r'^book/(?P<pk>\d+)/delete/$', views.BookDelete.as_view(), name='book_delete'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
)