from django import forms
from django.forms import widgets
from webapp.models import Task, Project
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ["summary", "description", "status", "types"]
        widgets = {
            "description": widgets.Textarea(attrs={"placeholder": "enter description"}),
            "types": widgets.CheckboxSelectMultiple,
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Search')


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ["title", "description", "start_date", "finish_date", "users"]
        widgets = {
            "description": widgets.Textarea(attrs={"placeholder": "enter description"}),
        }


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username']
        widgets = {
            "username": widgets.RadioSelect,
        }