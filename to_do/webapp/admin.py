from django.contrib import admin

# Register your models here.

from webapp.models import Task, Type, Status, Project


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'status']
    list_display_links = ['summary']
    list_filter = ['status']
    search_fields = ['summary']
    readonly_fields = ['created_at', 'updated_at']
    fields = ['summary', 'description', 'status', 'types', 'created_at', 'updated_at']


admin.site.register(Task, TaskAdmin)


class TypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['title']
    list_filter = ['title']
    search_fields = ['title']
    fields = ['title']


admin.site.register(Type, TypeAdmin)


class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['title']
    list_filter = ['title']
    search_fields = ['title']
    fields = ['title']


admin.site.register(Status, StatusAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'start_date']
    list_display_links = ['title']
    list_filter = ['title']
    search_fields = ['title', 'start_date']
    fields = ['title', 'description', 'start_date', 'finish_date']


admin.site.register(Project, ProjectAdmin)