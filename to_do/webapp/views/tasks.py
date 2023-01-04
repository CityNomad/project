from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from webapp.forms import TaskForm, SearchForm
from webapp.models import Task, Project
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class IndexView(ListView):
    model = Task
    template_name = "tasks/index.html"
    context_object_name = "tasks"
    ordering = "-updated_at"
    paginate_by = 5

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.search_value = None
        self.form = None

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Task.objects.filter(
                Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return Task.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})  # search=dcsdvsdvsd
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class TaskView(TemplateView):
    template_name = "tasks/task_view.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get("pk")
        task = get_object_or_404(Task, pk=pk)
        kwargs["task"] = task
        return super().get_context_data(**kwargs)


class CreateTask(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = "tasks/create_task.html"

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        task = form.save(commit=False)
        task.project = project
        task.user = self.request.user
        task.save()
        return redirect('webapp:task_view', pk=project.pk)


class UpdateTask(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    context_object_name = 'task'
    template_name = 'tasks/update_task.html'

    def get_success_url(self):
        return reverse('webapp:task_view', kwargs={'pk': self.object.pk})


class DeleteTask(LoginRequiredMixin, DeleteView):
        model = Task
        template_name = 'tasks/delete_task.html'
        context_object_name = 'task'
        success_url = reverse_lazy('webapp:home')