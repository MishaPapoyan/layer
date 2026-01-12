from django.urls import path
from . import views

app_name = 'education'

urlpatterns = [
    path('', views.education_home, name='home'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
]

