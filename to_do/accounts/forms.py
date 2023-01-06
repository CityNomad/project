from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length = 200, required = True, validators=[validate_email])

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['last_name'] == '':
            if cleaned_data['first_name'] == '':
                raise forms.ValidationError("Fill in one of the lines - first name or last name")
            return cleaned_data
        return cleaned_data

        # last_name = self.cleaned_data['last_name']
        # print(last_name)
        # first_name = self.cleaned_data['first_name']
        # print(first_name)
        # if last_name == '':
        #     if first_name == '':
        #         raise forms.ValidationError("Заполните одно из полей - Имя или Фамилию")
        #     return self.cleaned_data
        # return self.cleaned_data

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']