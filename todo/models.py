# todo/models.py

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    due = models.DateTimeField(default = timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Subtask(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    parent = models.ForeignKey(Todo, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class CanvasTodo(models.Model):
    # todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    due = models.DateTimeField(default = timezone.now)
    link = models.URLField()
    assignment_id = models.IntegerField()
    course_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class CanvasUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    canvasLinked = models.BooleanField(default = False)
    APIkey = models.CharField(max_length=150, default=None, null=True)
    img = models.CharField(max_length=200, default=None, null=True)
    name = models.CharField(max_length=200, default=None, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        CanvasUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.canvasuser.save()