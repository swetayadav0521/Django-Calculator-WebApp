from django.urls import path, include
from calculatorapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('remove/<int:pk>/', views.remove_history, name='remove'),
]