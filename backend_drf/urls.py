from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework_simplejwt import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/tasks/?done=False', permanent=True), name='home_page'),
    
    path('', include('users.urls')),
    path('', include('tasks.urls')),
    path('api/', include('api.urls')),
    
    path('api/token/', views.TokenObtainPairView.as_view()),
    path('api/token/refresh/', views.TokenRefreshView.as_view()),
    path('api/token/verify/', views.TokenVerifyView.as_view()),
]
