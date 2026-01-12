from django.urls import path
from . import views

app_name = 'cases'

urlpatterns = [
    path('', views.cases_home, name='home'),
    path('case/<int:pk>/', views.case_detail, name='case_detail'),
    path('case/<int:pk>/submit/', views.submit_analysis, name='submit_analysis'),
]

