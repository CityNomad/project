from django.urls import path
from django.views.generic import TemplateView, RedirectView

from webapp.views import HomeView, TaskView, CreateTask, UpdateTask, DeleteTask, IndexView, ProjectView, CreateProject, UpdateProject, DeleteProject, AddUserProject, DeleteUserProject

app_name = "webapp"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('projects/', RedirectView.as_view(pattern_name="home")),
    path('projects/add/', CreateProject.as_view(), name="create_project"),
    path('project/<int:pk>/', ProjectView.as_view(), name="project_view"),
    path('task/<int:pk>/update/', UpdateTask.as_view(), name="update_task"),
    path('task/<int:pk>/', TaskView.as_view(), name="task_view"),
    path('task/<int:pk>/delete/', DeleteTask.as_view(), name="delete_task"),
    path('project/<int:pk>/task/add/', CreateTask.as_view(), name="create_task"),
    path('projects/<int:pk>/update/', UpdateProject.as_view(), name='update_project'),
    path('projects/<int:pk>/delete/', DeleteProject.as_view(), name='delete_project'),
    path('projects/<int:pk>/user/', AddUserProject.as_view(), name="add_user_project"),
    path('user/<int:pk>/delete', DeleteUserProject.as_view(), name="delete_user_project"),

]