from django.urls import path

from .views import CreateUserView, UserLoginView, CustomLogoutView


urlpatterns = [
    path('user/create/', CreateUserView.as_view(), name='registration'),
    path('user/login/', UserLoginView.as_view(), name='login'),
    path('user/logout', CustomLogoutView.as_view(), name='logout')
]
