from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name="workers")
    groups = models.ManyToManyField(
        Group,
        related_name="worker_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="worker_set",
        blank=True
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "Low", "Low"
        MEDIUM = "Medium", "Medium"
        HIGH = "High", "High"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(Worker, related_name="tasks")

    def __str__(self):
        return self.name
