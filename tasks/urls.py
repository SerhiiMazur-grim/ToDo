from django.urls import path
from . import views


urlpatterns = [
    path('task/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/status-to-done/', views.TaskIsDoneView.as_view(), name='task_done'),
    path('task/<int:pk>/status-to-in-progress/', views.TaskToInProgressView.as_view(), name='task_to_in_progress'),
    path('task/<int:pk>/delete-task/', views.TaskDeleteView.as_view(), name='task_delete'),
]