# from django.contrib.auth import get_user_model
# from rest_framework import status
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.response import Response

# from .serializers import TaskSerializer
# from .models import Task
# from users.permissions import IsOwner, IsOwnerOrAdmin


# User = get_user_model()


# class TaskModelViewSet(ModelViewSet):
#     """
#     A ViewSet for managing Task model operations.

#     Permissions:
#     - `list`: Available to owners or admin users.
#     - Other actions: Available to owners only.
    
#     This view allows listing tasks based on the query parameters provided:
#     - `done`: Filters tasks by their completion status (e.g., done=true/false).
#     - `owner`: Filters tasks by owner (if the requesting user is a superuser).
#     """
    
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = [IsOwner]
    
#     def get_permissions(self):
#         if self.action == 'list':
#             return [IsOwnerOrAdmin()]
#         return super().get_permissions()
    
#     def list(self, request, *args, **kwargs):
#         done_param = request.query_params.get('done', None)
#         owner_param = request.query_params.get('owner', None)
                
#         if request.user.is_superuser:
#             queryset = self.queryset
#             if owner_param is not None:
#                 queryset = queryset.filter(owner=owner_param)
            
#         else:
#             queryset = self.queryset.filter(owner=request.user)
        
#         if done_param is not None:
#             done_param = str(done_param.capitalize())
#             queryset = queryset.filter(done=done_param)
        
#         serializer = self.serializer_class(queryset, many=True)
#         return Response(serializer.data, status.HTTP_200_OK)
