from django.db import models
from django.contrib.auth.models import Permission, User
# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    type = models.CharField(max_length=10)
    status = models.CharField(max_length=50)
    priority = models.CharField(max_length=10)
    team = models.CharField(max_length=50)
    owner = models.CharField(max_length=50)


    def __str__(self):
        return self.name + ' - ' + self.status


class Comment(models.Model):
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    content = models.CharField(max_length=10000)
    comment_date = models.DateField(auto_now_add=True, blank=True)
    comment_time = models.TimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.user + ' - ' + self.content