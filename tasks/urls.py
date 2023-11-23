from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import TaskModelViewSet


router = DefaultRouter()
router.register(r'tasks', TaskModelViewSet)

urlpatterns = router.urls
