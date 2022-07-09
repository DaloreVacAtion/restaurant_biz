from django.contrib.auth.forms import UserCreationForm

from .models import User
from django import forms


class MyUserCreationForm(UserCreationForm):  # Это в админке
    password1 = forms.CharField(widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False)
    name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'name', 'password1', 'password2']

    # def __init__(self, *args, **kwargs):
    #     self.fields['password1'].required = False
    #     self.fields['password2'].required = False
    #     self.fields['name'].required = False
    #     self.fields['password1'].widget.attrs['autocomplete'] = 'off'
    #     self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        print(self.cleaned_data)
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        return password2

    def save(self, commit=True):
        user = super().save()
        if bool(self.cleaned_data["password1"]):
            user.is_superuser = True
            user.is_staff = True
        user.save()
        return user
