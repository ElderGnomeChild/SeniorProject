#todo/serializers.py

from rest_framework import serializers
from .models import Todo, Subtask, CanvasTodo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'completed', 'due')



class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ('id', 'title', 'description', 'completed', 'parent')

class CanvasTodoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CanvasTodo
        fields = ('id', 'title', 'description', 'completed', 'due', 'link', 'assignment_id', 'course_id')