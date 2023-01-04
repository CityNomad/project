from django.db.models import Q
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from webapp.models import Project
from webapp.forms import SearchForm, ProjectForm, AddUsersInProjectForm
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from accounts.models import Profile
from accounts.forms import MyUserCreationForm


class HomeView(ListView):
    model = Project
    template_name = "projects/home.html"
    context_object_name = "projects"
    ordering = "id"
    paginate_by = 2


    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Project.objects.filter(
                Q(title__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return Project.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class ProjectView(DetailView):
    template_name = "projects/project_view.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.object.tasks_project.order_by("-created_at")
        return context


class CreateProject(PermissionRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = "projects/create_project.html"
    permission_required = 'webapp.add_project'

    def form_valid(self, form):
        user = self.request.user
        project = form.save(commit=False)
        form.instance.project = project
        project.save()
        project.users.add(user)
        return super().form_valid(form)


class UpdateProject(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'projects/update_project.html'
    form_class = ProjectForm
    context_object_name = 'project'
    permission_required = 'webapp.change_project'




class DeleteProject(PermissionRequiredMixin, DeleteView):
    model = Project
    context_object_name = 'project'
    template_name = 'projects/delete_project.html'
    success_url = reverse_lazy('webapp:home')
    permission_required = 'webapp.delete_project'

    def has_permission(self):
        return super().has_permission()


# class AddUserProject(PermissionRequiredMixin, CreateView):
#     form_class = MyUserCreationForm
#     template_name = "projects/add_user.html"
#     permission_required = 'webapp.add_project_user'
#
#     def has_permission(self):
#         return super().has_permission() or self.request.user in self.get_object().users.all()
#
#     def form_valid(self, form):
#         project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
#         user = form.save()
#         Profile.objects.create(user=user)
#         form.instance.project = project
#         project.users.add(user)
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse("webapp:project_view", kwargs={"pk": self.kwargs.get('pk')})

class AddUserProject(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = "projects/add_user.html"
    permission_required = "webapp.add_project_user"
    form_class = AddUsersInProjectForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["pk"] = self.request.user.pk
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.users.add(self.request.user)
        return response

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all()

    def get_success_url(self):
        return reverse("webapp:home")


class DeleteUserProject(PermissionRequiredMixin, DeleteView):
    model = User

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("webapp:home")
