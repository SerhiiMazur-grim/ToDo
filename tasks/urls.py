from rest_framework.routers import DefaultRouter

from .views import TaskModelViewSet


router = DefaultRouter()
router.register(r'tasks', TaskModelViewSet)

urlpatterns = router.urls
