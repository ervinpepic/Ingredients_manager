from django.urls import path

from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.article_list_view),
    path('articles/', views.article_search_view, name='search'),
    path('create', views.article_create_view, name='create'),
    path('<slug:slug>/', views.article_detail_view, name='detail'),
]