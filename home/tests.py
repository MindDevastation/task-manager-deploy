from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from home.models import Task, TaskType, Worker, Position
from home.forms import WorkerUpdateForm
from datetime import date


class PositionModelTest(TestCase):
    def test_position_creation(self):
        position = Position.objects.create(name="Developer")
        self.assertEqual(str(position), "Developer")


class WorkerModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Manager")
        self.worker = Worker.objects.create_user(
            username="worker1",
            password="password123",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            position=self.position,
        )

    def test_worker_str(self):
        self.assertEqual(str(self.worker), "John Doe (worker1)")


class TaskModelTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Bug Fix")
        self.task = Task.objects.create(
            name="Fix login issue",
            description="Users can't log in",
            deadline=date.today(),
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
        )

    def test_task_str(self):
        self.assertEqual(str(self.task), "Fix login issue")


class TaskViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.position = Position.objects.create(name="Tester")
        self.worker = Worker.objects.create_user(
            username="testuser", password="password123"
        )
        self.task_type = TaskType.objects.create(name="Feature")
        self.task = Task.objects.create(
            name="Create dashboard",
            description="Design and implement dashboard",
            deadline=date.today(),
            priority=Task.Priority.MEDIUM,
            task_type=self.task_type,
        )
        self.task.assignees.add(self.worker)

    def test_task_list_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("home-app:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create dashboard")

    def test_task_detail_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("home-app:task-detail", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Design and implement dashboard")

    def test_task_toggle_status_view(self):
        self.client.login(username="testuser", password="password123")
        self.client.post(reverse("home-app:task-detail", args=[self.task.id]))
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)


class WorkerUpdateFormTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create_user(
            username="worker2", password="password123"
        )

    def test_valid_form(self):
        form_data = {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "position": self.position.id,
        }
        form = WorkerUpdateForm(data=form_data, instance=self.worker)
        self.assertTrue(form.is_valid())


class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Worker.objects.create_user(
            username="testuser", password="password123", email="test@example.com"
        )

    def test_login(self):
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "password123"}
        )
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)

    def test_password_reset(self):
        response = self.client.post(
            reverse("password_reset"), {"email": "test@example.com"}
        )
        self.assertEqual(response.status_code, 302)

    def test_password_change(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            reverse("password_change"),
            {
                "old_password": "password123",
                "new_password1": "newpassword123",
                "new_password2": "newpassword123",
            },
        )
        self.assertEqual(response.status_code, 302)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Worker.objects.create_user(
            username="profileuser", password="password123"
        )

    def test_profile_view(self):
        self.client.login(username="profileuser", password="password123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
