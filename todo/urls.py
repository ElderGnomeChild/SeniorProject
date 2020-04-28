from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'todo'
urlpatterns = [
    path('<int:user_id>', views.index, name='index'),
    path('user', views.canvas_user, name='canvas_user'),
    path('log', views.log, name='log'),
    path('logout', views.out, name='out'),
    path('', views.home, name='home'),
    path('newtask', views.newtask, name='newtask'),
    path('task/<int:task_id>', views.task, name='task'),
    path('newsub/<int:task_id>', views.newsub, name='newsub'),
    path('canvas-link', views.canvas_link, name='link'),
    path('all/<int:user_id>', views.all, name='all'),
    path('complete/<int:task_id>', views.complete, name='complete'),
    path('undo/<int:task_id>', views.undo, name='undo'),
    path('complete-canvas/<int:task_id>', views.completecan, name='complete'),
    path('undo-canvas/<int:task_id>', views.undocan, name='undo'),
    path('complete/<int:task_id>/<int:sub_id>', views.completesub, name='complete'),
    path('undo/<int:task_id>/<int:sub_id>', views.undosub, name='undo'),
    path('unlink', views.unlink, name='unlink'),
    path('newuser', views.newuser, name='newuser'),
    path('error/<str:error_type>', views.error, name='error'),

]