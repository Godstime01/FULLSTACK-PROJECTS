from django.db import models
from django.contrib.auth import get_user_model

USER = get_user_model()

class Todo(models.Model):
  todo = models.CharField(max_length = 100)
  completed = models.BooleanField(default = False)
  date_created = models.DateTimeField(auto_now_add = True)
  user = models.ForeignKey(USER, on_delete = models.CASCADE)
  
  def __str__(self): return self.todo
