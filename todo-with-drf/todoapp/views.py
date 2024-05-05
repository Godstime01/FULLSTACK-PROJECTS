from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from .serializers import TodoSerializers, UserSerializers
from .models import Todo, USER


class TodoViewSet(viewsets.ModelViewSet):
  serializer_class = TodoSerializers
  
  def get_queryset(self, request):
    q = Todo.objects.filter(user = request.user)
    return q
    
    
class RegisterView(CreateAPIView):
  permission_classes = ()
  serializer_class = UserSerializers
  queryset = USER.objects.all()