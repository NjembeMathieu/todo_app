"""from django.urls import path
from . import views
app_name = 'todo_app'
urlpatterns = [
    path('', views.task_list, name='task_list'),
    #path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('todo', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:pk>/toggle/', views.task_toggle, name='task_toggle'),
]
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),  # URL: /todo/
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:pk>/toggle/', views.task_toggle, name='task_toggle'),
]