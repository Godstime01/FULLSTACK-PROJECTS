from rest_framework import serializers
from .models import Todo
from django.contrib.auth import get_user_model

USER = get_user_model()

class TodoSerializers(serializers.ModelSerializer):
  class Meta:
    model = Todo
    fields = ("id", "todo", "completed", "date_created")
    
    
class UserSerializers(serializers.ModelSerializer):
  class Meta:
    model = USER
    fields = ('username', 'email', 'password')
    extra_kwargs = {
      "write_only": ("password")
    }