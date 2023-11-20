from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (UserApiCrtRetListDelViewSet,
                    UserUpdateApiView,
                    UserUpdatePasswordApiView
                    )


router = DefaultRouter()
router.register(r'users', UserApiCrtRetListDelViewSet)

urlpatterns = [
    path('users/<int:pk>/update/',
         UserUpdateApiView.as_view()),
    
    path('users/<int:pk>/update-password/',
         UserUpdatePasswordApiView.as_view()),
]

urlpatterns += router.urls
