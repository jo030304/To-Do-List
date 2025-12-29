from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    CATEGORY_CHOICES = [
        ('todo', 'To Do'),
        ('end', 'End To Do'),
        ('not', 'Not End To Do'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='todo')
    deadline = models.DateField(null=True, blank=True)  # ← 추가!
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title