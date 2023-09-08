from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    todolist = models.ForeignKey(TodoList, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=250)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_checked = models.BooleanField(default=False)