from django.db import models
from webapp.validate import validate_title, validate_description
from django.urls import reverse


# Create your models here.

class Task(models.Model):
    summary = models.CharField(max_length=50, null=False, blank=False, verbose_name="Title",
                               validators=[validate_title])
    description = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Description",
                                   validators=[validate_description])
    status = models.ForeignKey("webapp.Status", on_delete=models.PROTECT, related_name="tasks_statuses",
                               verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")
    types = models.ManyToManyField("webapp.Type", related_name="tasks", blank=True)
    project = models.ForeignKey('webapp.Project', on_delete=models.CASCADE, related_name='tasks_project',
                                verbose_name="Project", default=1)

    def __str__(self):
        return f"{self.id}. {self.summary}: {self.status}"

    def get_absolute_url(self):
        return reverse("webapp:task_view", kwargs={"pk": self.pk})

    class Meta:
        db_table = "tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class Type(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Type")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "types"
        verbose_name = "Тип"
        verbose_name_plural = "Типы"


class Status(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Status")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "statuses"
        verbose_name = "Status"
        verbose_name_plural = "Statuses"


class Project(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Project title")
    description = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Description")
    start_date = models.DateField(auto_created=False, verbose_name="Started at")
    finish_date = models.DateField(auto_created=False, blank=True, null=True, verbose_name="Finished at")
    users = models.ManyToManyField("auth.User", related_name='projects', default=1)

    def __str__(self):
        return f"{self.title}:{self.start_date}"

    def get_absolute_url(self):
        return reverse("webapp:project_view", kwargs={"pk": self.pk})

    class Meta:
        db_table = "projects"
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        permissions = [
            ('add_project_user', 'Add project user')
        ]
