from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework import permissions, mixins, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .serializers import UserSerializer, UserUpdateSerializer, UserChangePassworSerializer
from .permissions import IsOwner, IsOwnerOrAdmin


User = get_user_model()


class UserApiCrtRetListDelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
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


class UserUpdateApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsOwner]
    
    def get_allowed_methods(self):
        return ['PATCH']
    
    def put(self, request, *args, **kwargs):
        return Response({'detail': _('Method "PUT" Not Allowed')},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserUpdatePasswordApiView(APIView):
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


    def put(self, request, *args, **kwargs):
        return Response({'detail': _('Method "PUT" Not Allowed')},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
