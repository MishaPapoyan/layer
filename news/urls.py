from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_home, name='home'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
]

