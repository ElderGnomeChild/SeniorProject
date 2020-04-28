from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=256)
    password = forms.CharField(label="Password", max_length=256)

class TaskForm(forms.Form):
    name = forms.CharField(label="Task Name", max_length=120)
    description = forms.CharField(label="Description", max_length=500, widget=forms.Textarea())
    due = forms.DateTimeField(input_formats=('%m/%d/%Y %I:%M %p',))

class SubtaskForm(forms.Form):
    name = forms.CharField(label="Subtask Name", max_length=120)
    description = forms.CharField(label="Description", max_length=500, widget=forms.Textarea())

class CanvasAPIForm(forms.Form):
    APIKey = forms.CharField(label="API Key", max_length=256)

class NewUserForm(UserCreationForm):
    # username = forms.CharField(label="Username", max_length=32)
    # password = forms.CharField(label="Password", max_length=50)
    # password_conf = forms.CharField(label="Confirm Password", max_length=50)
    first_name = forms.CharField(label="First Name", required = True, max_length=30)
    last_name = forms.CharField(label="Last Name", required = True, max_length=30)
    email = forms.EmailField(label="Email", required = False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name',)
