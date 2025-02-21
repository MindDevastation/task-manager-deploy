from django.urls import path

from . import views
from .views import (
    TaskCreateView,
    TaskDeleteView,
    TaskUpdateView,
    TaskListView,
    TaskDetailView,
    WorkerDetailView,
    TaskToggleStatusView,
)

urlpatterns = [
    path("", views.index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/add/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path(
        "tasks/<int:pk>/toggle-status/",
        TaskToggleStatusView.as_view(),
        name="task-toggle-status",
    ),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/", views.workers_list, name="workers-list"),
    path("worker/update/", views.worker_update, name="worker-update"),
]

app_name = "home-app"
