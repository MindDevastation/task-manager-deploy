from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from home.forms import WorkerUpdateForm
from home.models import Task, Worker


def index(request):
    if request.user.is_authenticated:
        priority = request.GET.get("priority")
        if request.user.is_staff:
            tasks = Task.objects.filter(priority=priority)
        else:
            tasks = Task.objects.filter(assignees=request.user).filter(priority=priority)

        workers = Worker.objects.all()
    else:
        tasks = Task.objects.none()
        workers = Worker.objects.none()

    context = {
        "tasks": tasks,
        "workers": workers,
    }

    return render(request, "pages/dashboard.html", context=context)


class TaskListView(ListView):
    model = Task
    template_name = "pages/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Task.objects.filter(assignees=self.request.user)

            search_query = self.request.GET.get("search", "")
            status_filter = self.request.GET.get("status", "")

            if search_query:
                queryset = queryset.filter(name__icontains=search_query)

            if status_filter in ["completed", "in_progress"]:
                queryset = queryset.filter(is_completed=(status_filter == "completed"))

            return queryset
        else:
            return Task.objects.none()


class TaskCreateView(CreateView):
    model = Task
    fields = ["name", "description", "deadline", "is_completed", "priority", "task_type", "assignees"]
    template_name = "pages/task_form.html"
    success_url = reverse_lazy("home-app:task-list")


class TaskUpdateView(UpdateView):
    model = Task
    fields = ["name", "description", "deadline", "is_completed", "priority", "task_type", "assignees"]
    template_name = "pages/task_form.html"
    success_url = reverse_lazy("home-app:task-list")


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "pages/task_confirm_delete.html"
    success_url = reverse_lazy("home-app:manager:task-list")


class TaskDetailView(DetailView):
    model = Task
    template_name = "pages/task_detail.html"
    context_object_name = "task"


class WorkerDetailView(DetailView):
    model = Worker
    template_name = "pages/worker_detail.html"
    context_object_name = "worker"


class TaskToggleStatusView(View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = not task.is_completed
        task.save()
        return HttpResponseRedirect(reverse("home-app:task-detail", args=[pk]))

def workers_list(request):
    workers = Worker.objects.all()
    context = {
        "workers": workers
    }
    return render(request, "pages/workers_list.html", context)

@login_required
def worker_update(request):
    worker = request.user
    if request.method == "POST":
        form = WorkerUpdateForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            return redirect("home-app:index")
    else:
        form = WorkerUpdateForm(instance=worker)

    context = {
        "form": form
    }
    return render(request, "pages/worker_update.html", context)
