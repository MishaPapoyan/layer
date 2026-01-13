from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('', views.application_generator, name='generator'),
    path('create/<int:app_type_id>/', views.create_application, name='create'),
    path('download/<int:pk>/', views.download_application, name='download'),
    path('my-applications/', views.my_applications, name='my_applications'),
]


