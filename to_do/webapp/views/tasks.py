from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from webapp.forms import TaskForm, SearchForm
from webapp.models import Task, Project
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Create your views here.

class TaskView(TemplateView):
    template_name = "tasks/task_view.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get("pk")
        task = get_object_or_404(Task, pk=pk)
        kwargs["task"] = task
        return super().get_context_data(**kwargs)


class CreateTask(PermissionRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = "tasks/create_task.html"
    permission_required = 'webapp.add_task'

    def has_permission(self):
        return super().has_permission()

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        task = form.save(commit=False)
        task.project = project
        task.user = self.request.user
        task.save()
        return redirect('webapp:task_view', pk=project.pk)


class UpdateTask(PermissionRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    context_object_name = 'task'
    template_name = 'tasks/update_task.html'
    permission_required = 'webapp.change_task'

    def get_success_url(self):
        return reverse('webapp:task_view', kwargs={'pk': self.object.pk})


class DeleteTask(PermissionRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete_task.html'
    context_object_name = 'task'
    success_url = reverse_lazy('webapp:home')
    permission_required = 'webapp.delete_task'

    def has_permission(self):
        return super().has_permission()
