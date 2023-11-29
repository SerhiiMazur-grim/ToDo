from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .serializers import UserSerializer, UserChangePassworSerializer, TaskSerializer
from users.permissions import IsOwner, IsOwnerOrAdmin
from tasks.models import Task


User = get_user_model()


class UserApiViewSet(ModelViewSet):
    """
    A ViewSet to handle User creation, retrieval, update, and deletion.

    Allows different actions based on permissions:
    - `list`: Allows only admin users to list all Users.
    - `create`: Allows anyone to create a new User.
    - `retrieve`: Allows the owner or an admin user to retrieve a specific User.
    - `destroy`: Allows the owner or an admin user to delete a specific User.
    - `update`: Allows `PATCH` for partial updates but prohibits `PUT` for full updates.
    """
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner]
    
    
    def get_permissions(self):
        if self.action == 'list':
            return [permissions.IsAdminUser()]
        elif self.action == 'create':
            return [permissions.AllowAny()]
        elif self.action in ('retrieve', 'destroy'):
            return [IsOwnerOrAdmin()]

        return super().get_permissions()
    
    
    def update(self, request, *args, **kwargs):
        method_patch = kwargs.get('partial', False)
        
        if not method_patch:
            return Response({'detail': _('Method "PUT" Not Allowed')}, \
                status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().update(request, *args, **kwargs)
    

class UserChangePasswordApiView(APIView):
    """
    A view to update a User's password.

    Allows a User to change their password using the PATCH method.
    """
    
    permission_classes = [IsOwner]

    
    def get_object(self):
        return User.objects.get(pk=self.kwargs['pk'])


    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserChangePassworSerializer(instance, 
                                                data=request.data,
                                                context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': _('The password has been changed')},
                            status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskModelViewSet(ModelViewSet):
    """
    A ViewSet for managing Task model operations.

    Permissions:
    - `list`: Available to owners or admin users.
    - Other actions: Available to owners only.
    
    This view allows listing tasks based on the query parameters provided:
    - `done`: Filters tasks by their completion status (e.g., done=true/false).
    - `owner`: Filters tasks by owner (if the requesting user is a superuser).
    """
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]
    
    def get_permissions(self):
        if self.action == 'list':
            return [IsOwnerOrAdmin()]
        return super().get_permissions()
    
    def list(self, request, *args, **kwargs):
        done_param = request.query_params.get('done', None)
        owner_param = request.query_params.get('owner', None)
                
        if request.user.is_superuser:
            queryset = self.queryset
            if owner_param is not None:
                queryset = queryset.filter(owner=owner_param)
            
        else:
            queryset = self.queryset.filter(owner=request.user)
        
        if done_param is not None:
            done_param = str(done_param.capitalize())
            queryset = queryset.filter(done=done_param)
        
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
