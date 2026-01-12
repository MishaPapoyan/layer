from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_home, name='home'),
    path('room/<int:pk>/', views.chat_room, name='chat_room'),
    path('consultation/create/', views.create_consultation, name='create_consultation'),
    path('consultations/', views.consultations, name='consultations'),
]

