from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (UserApiViewSet,
                    UserUpdatePasswordApiView
                    )


router = DefaultRouter()
router.register(r'users', UserApiViewSet)

urlpatterns = [
     path('users/<int:pk>/change-password/',
         UserUpdatePasswordApiView.as_view()),
]

urlpatterns += router.urls
