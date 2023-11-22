from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/', include('users.urls')),
    path('api/', include('tasks.urls')),
    
    path('api/token/', views.TokenObtainPairView.as_view()),
    path('api/token/refresh/', views.TokenRefreshView.as_view()),
    path('api/token/verify/', views.TokenVerifyView.as_view()),
]
