# from rest_framework.viewsets import ModelViewSet
# from rest_framework.views import APIView
# from rest_framework import permissions, status
# from rest_framework.response import Response
# from django.contrib.auth import get_user_model
# from django.utils.translation import gettext_lazy as _

# from .serializers import UserSerializer, UserChangePassworSerializer
# from .permissions import IsOwner, IsOwnerOrAdmin


# User = get_user_model()


# class UserApiViewSet(ModelViewSet):
#     """
#     A ViewSet to handle User creation, retrieval, update, and deletion.

#     Allows different actions based on permissions:
#     - `list`: Allows only admin users to list all Users.
#     - `create`: Allows anyone to create a new User.
#     - `retrieve`: Allows the owner or an admin user to retrieve a specific User.
#     - `destroy`: Allows the owner or an admin user to delete a specific User.
#     - `update`: Allows `PATCH` for partial updates but prohibits `PUT` for full updates.
#     """
    
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsOwner]
    
    
#     def get_permissions(self):
#         if self.action == 'list':
#             return [permissions.IsAdminUser()]
#         elif self.action == 'create':
#             return [permissions.AllowAny()]
#         elif self.action in ('retrieve', 'destroy'):
#             return [IsOwnerOrAdmin()]

#         return super().get_permissions()
    
    
#     def update(self, request, *args, **kwargs):
#         method_patch = kwargs.get('partial', False)
        
#         if not method_patch:
#             return Response({'detail': _('Method "PUT" Not Allowed')}, \
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED)

#         return super().update(request, *args, **kwargs)
    

# class UserChangePasswordApiView(APIView):
#     """
#     A view to update a User's password.

#     Allows a User to change their password using the PATCH method.
#     """
    
#     permission_classes = [IsOwner]

    
#     def get_object(self):
#         return User.objects.get(pk=self.kwargs['pk'])


#     def patch(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = UserChangePassworSerializer(instance, 
#                                                 data=request.data,
#                                                 context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'detail': _('The password has been changed')},
#                             status=status.HTTP_200_OK)
            
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
