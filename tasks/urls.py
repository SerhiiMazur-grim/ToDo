from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import TaskModelViewSet, TaskListView


router = DefaultRouter()
router.register(r'tasks', TaskModelViewSet)

urlpatterns = [
    path('tasks/all/', TaskListView.as_view())
]


urlpatterns += router.urls
