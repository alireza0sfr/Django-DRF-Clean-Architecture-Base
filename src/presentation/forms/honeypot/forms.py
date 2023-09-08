from django import forms
from domain.apps.honeypot.models import Honeypot


class LoginForm(forms.ModelForm):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

    class Meta:
        model = Honeypot
        fields = ["username", "password"]
