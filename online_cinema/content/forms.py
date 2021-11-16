from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Повторите пароль"}))

    class Meta:
        model = User
        fields = ("username",)
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Логин"})
        }

    def password_check(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password_repeat"]:
            raise forms.ValidationError("Пароль не совпадает")
        return cd["password_repeat"]


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Логин"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}))
