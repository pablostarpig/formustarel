from django import forms
from django.contrib.auth.models import User

from .models import Ticket, Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'description']


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['name', 'status', 'team']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
