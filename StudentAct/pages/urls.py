from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('tasks/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/toggle/', views.task_toggle, name='task_toggle'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
]
