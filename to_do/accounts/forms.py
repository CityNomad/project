from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email

from accounts.models import Profile


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length = 200, required = True, validators=[validate_email])

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['last_name'] == '':
            if cleaned_data['first_name'] == '':
                raise forms.ValidationError("Fill in one of the lines - first name or last name")
            return cleaned_data
        return cleaned_data

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']


class UserChangeForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'First name', 'last_name': 'Last name', 'email': 'Email'}


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['git_profile', 'avatar', 'about']