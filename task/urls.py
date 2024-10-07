from django.urls import path

from task.apps import TaskConfig
from task.views import (
    TaskCreateAPIView,
    TaskListAPIView,
    TaskRetrieveAPIView,
    TaskUpdateAPIView,
    TaskDestroyAPIView,
    TasksPublicListAPIView,
)

app_name = TaskConfig.name

urlpatterns = [
    path('public/', TasksPublicListAPIView.as_view(), name='tasks_public_list'),
    path("tasks/", TaskListAPIView.as_view(), name="tasks_list"),
    path("tasks/<int:pk>", TaskRetrieveAPIView.as_view(), name="tasks_retrieve"),
    path("tasks/create/", TaskCreateAPIView.as_view(), name="tasks_create"),
    path("tasks/<int:pk>/delete", TaskDestroyAPIView.as_view(), name="tasks_delete"),
    path("tasks/<int:pk>/update", TaskUpdateAPIView.as_view(), name="tasks_update"),
]
