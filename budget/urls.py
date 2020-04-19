from django.urls import path 
from . import views


urlpatterns = [
    path('', views.budget_list, name='list'),
    path('add/', views.budget_add, name='add'),
    path('<slug:budget_slug>/', views.budget_detail, name='detail'),
]