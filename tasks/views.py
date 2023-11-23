from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .serializers import TaskSerializer
from .models import Task
from users.permissions import IsOwner, IsOwnerOrAdmin


class TaskModelViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]
    
    def get_permissions(self):
        if self.action == 'list':
            return [IsOwnerOrAdmin()]
        return super().get_permissions()
    
    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.get_queryset()
        else:
            queryset = self.queryset.filter(owner=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
