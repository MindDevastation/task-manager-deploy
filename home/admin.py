from .models import Task, TaskType, Position

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Worker, Position


class WorkerAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "position",
        "is_staff",
        "is_active",
    )

    list_filter = ("is_staff", "is_active", "position")

    search_fields = ("username", "first_name", "last_name", "email")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "position")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "email",
                    "position",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )

    ordering = ("username",)


admin.site.register(Worker, WorkerAdmin)

admin.site.register(Task)
admin.site.register(TaskType)
admin.site.register(Position)
