from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_home, name='home'),
    path('room/<int:pk>/', views.chat_room, name='chat_room'),
    path('consultation/create/', views.create_consultation, name='create_consultation'),
    path('consultations/', views.consultations, name='consultations'),
    # Online chat widget API
    path('api/online-chat/', views.online_chat_api, name='online_chat_api'),
    path('admin/chat/', views.admin_chat_interface, name='admin_chat'),
    path('admin/chat/<str:session_id>/send/', views.admin_send_message, name='admin_send_message'),
    path('admin/chat/<str:session_id>/messages/', views.admin_get_messages, name='admin_get_messages'),
]

