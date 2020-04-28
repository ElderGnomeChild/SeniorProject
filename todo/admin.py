# todo/admin.py

from django.contrib import admin
from .models import Todo, Subtask, CanvasTodo, CanvasUser

class TodoAdmin(admin.ModelAdmin):  
    list_display = ('title', 'description', 'completed', 'due', 'user') 

class SubtaskAdmin(admin.ModelAdmin):  
    list_display = ('title', 'description', 'completed', 'parent') 

class CanvasTodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'completed', 'due', 'link', 'assignment_id', 'course_id', 'user') 

class CanvasUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'canvasLinked', 'APIkey')

# Register your models here.
admin.site.register(Todo, TodoAdmin) 
admin.site.register(Subtask, SubtaskAdmin) 
admin.site.register(CanvasTodo, CanvasTodoAdmin)
admin.site.register(CanvasUser, CanvasUserAdmin)
