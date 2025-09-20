from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Repeat password")

    class Meta:
        model = User
        fields = ("username",)

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords did not happen")
        return password2


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Incorrect username or password")
            cleaned_data["user"] = user
        return cleaned_data
