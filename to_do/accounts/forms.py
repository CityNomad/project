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


class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(label="New password", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Repeat new password", widget=forms.PasswordInput, strip=False)
    old_password = forms.CharField(label="Previous password", strip=False, widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords are not equal!')
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Previous password is not correct!')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['password', 'password_confirm', 'old_password']