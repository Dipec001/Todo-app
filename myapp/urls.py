from django.urls import path
from . import views

app_name = 'todolist'

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('add_todo', views.add_todo, name='add_todo'),
    path('delete_session_todo/<int:index>/', views.delete_session_todo, name='delete_session_todo'),
    path('clear_session_todos', views.clear_session_todos, name='clear_session_todos'),
    path('profile', views.profile, name='profile'),
    path('manage_lists', views.manage_lists, name='manage_lists'),
    path('todolist/<int:todolist_id>', views.todolist_detail, name='todolist_detail'),
    path('create_todolist/', views.create_todolist, name='create_todolist'),
    path('delete_todo/<int:todolist_id>/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('update_todolist_title/<int:todolist_id>/', views.update_todolist_title, name='update_todolist_title'),
    path('delete_todolist/<int:todolist_id>/', views.delete_todolist, name='delete_todolist'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('update_todo/<int:todo_id>/', views.update_todo, name='update_todo'),
]