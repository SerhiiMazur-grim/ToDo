from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (UserApiViewSet,
                    UserChangePasswordApiView,
                    TaskModelViewSet
                    )


router = DefaultRouter()
router.register(r'users', UserApiViewSet)
router.register(r'tasks', TaskModelViewSet)

urlpatterns = [
     path('users/<int:pk>/change-password/',
         UserChangePasswordApiView.as_view()),
]

urlpatterns += router.urls
