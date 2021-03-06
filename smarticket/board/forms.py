from django import forms
from django.contrib.auth.models import User

from .models import Ticket, Project, Comment


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'description']


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['name', 'status', 'team', 'type', 'priority', 'owner', 'description',
                  'project']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'date_joined']
