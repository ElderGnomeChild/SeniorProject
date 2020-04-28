from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from rest_framework import viewsets
from .serializers import TodoSerializer, SubtaskSerializer, CanvasTodoSerializer
from .models import Todo, Subtask, CanvasTodo, User
from pip._vendor import requests
from .forms import LoginForm, TaskForm, SubtaskForm, CanvasAPIForm, NewUserForm                                                                                                                                        
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.

class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

class SubtaskView(viewsets.ModelViewSet):
    serializer_class = SubtaskSerializer
    queryset = Subtask.objects.all()

class CanvasTodoView(viewsets.ModelViewSet):
    serializer_class = CanvasTodoSerializer
    queryset = CanvasTodo.objects.all()

def newuser(request):
    message = ''
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()

            raw = form.cleaned_data['password1']
            
            # if p1 == p2:

            username = form.cleaned_data['username']
            
            user = authenticate(username=username, password=raw)
            
            login(request, user)

            return HttpResponseRedirect('/')

        else:
             message = 'Your passwords did not match.'   
        #     return HttpResponseRedirect('/error/pass')

    else:
        form = NewUserForm()

    return render(request, 'todo/newuser.html', {'form':form, 'message': message})


def error(request, error_type):
    if error_type == 'pass':
        message= 'Your passwords did not match.'
    elif error_type == 'login':
        message = 'Invalid username or password.'
    else: 
        message = 'How did you get here? You are not supposed to be here. Please leave now. There will be C O N S E Q U E N C E S.'
    return render(request, 'todo/error.html', {'message':message})


def log(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # print('if')
                login(request, user)
                logstring = '/' + str(user.id)
                return HttpResponseRedirect(redirect_to=logstring)

            else:
                # print('else')
                return HttpResponseRedirect(redirect_to='/error/login')


    else:
        form = LoginForm()

        return render(request, 'todo/login.html', {'form':form})

def out(request):
    logout(request)
    return(HttpResponseRedirect('/log'))

def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/log')

    else:
        returnstr = '/' + str(request.user.id)
        return HttpResponseRedirect(returnstr)

@login_required
def newtask(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            due = form.cleaned_data['due']

            t = Todo(title=name, description=description, due=due, user=user)
            t.save()
            return HttpResponseRedirect('/')

    else:
        form = TaskForm()
        return render(request, 'todo/newtask.html', {'form':form})

    return render(request, 'todo/newtask.html', {'form':form})

@login_required
def newsub(request, task_id):
    task = get_object_or_404(Todo, pk=task_id)
    if request.user == task.user:
        if request.method == 'POST':
            form = SubtaskForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                s = Subtask(title=name, description=description, parent=task)
                s.save()
                return HttpResponseRedirect('/task/' + str(task_id))
        else:
            form = SubtaskForm()
            return render(request, 'todo/newsub.html', {'form':form, 'task':task})
    else:
        current = request.user.id
        return HttpResponseRedirect('/' + str(current))


@login_required
def canvas_link(request):
    user = get_object_or_404(User, id=request.user.id)
    if request.method == 'POST':
        form = CanvasAPIForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data['APIKey']

            user.canvasuser.APIkey = key
            user.canvasuser.canvasLinked = True
            user.save()
            return HttpResponseRedirect('/user')

    else:
        form = CanvasAPIForm()
        return render(request, 'todo/canvas_link.html', {'form':form})


@login_required
def complete(request, task_id):
    task = get_object_or_404(Todo, id=task_id)
    if task.user == request.user:
        task.completed=True
        task.save()

    return HttpResponseRedirect('/')


@login_required
def completecan(request, task_id):
    task = get_object_or_404(CanvasTodo, id=task_id)
    if task.user == request.user:
        task.completed=True
        task.save()

    return HttpResponseRedirect('/')


@login_required
def completesub(request, task_id, sub_id):
    task = get_object_or_404(Todo, id=task_id)
    sub = get_object_or_404(Subtask, id=sub_id)
    
    if task.user == request.user:
        sub.completed=True
        sub.save()

    return HttpResponseRedirect('/task/'+str(task.id))


@login_required
def undo(request, task_id):
    task = get_object_or_404(Todo, id=task_id)
    if task.user == request.user:
        task.completed=False
        task.save()

    return HttpResponseRedirect('/')

@login_required
def undocan(request, task_id):
    task = get_object_or_404(CanvasTodo, id=task_id)
    if task.user == request.user:
        task.completed=False
        task.save()

    return HttpResponseRedirect('/')

@login_required
def undosub(request, task_id, sub_id):
    task = get_object_or_404(Todo, id=task_id)
    sub = get_object_or_404(Subtask, id=sub_id)
    
    if task.user == request.user:
        sub.completed=False
        sub.save()

    return HttpResponseRedirect('/task/'+str(task.id))





@login_required
def task(request, task_id):
    task = get_object_or_404(Todo, pk=task_id)
    if request.user == task.user:
        subs = Subtask.objects.filter(parent=task)
        return render(request, 'todo/task.html', {'task':task, 'subs':subs})
    else:
        current = request.user.id
        return HttpResponseRedirect('/' + str(current))


@login_required
def index(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # user = User.objects.get(id=user_id)
    if user == request.user:
        tasks = (Todo.objects.filter(user=user))
        tasks = tasks.filter(completed=False)
        tasks = tasks.order_by('due')
        # tasks.append(CanvasTodo.objects.filter(user=user))
        subtasks = Subtask.objects.all()
        show_all = False

        canvas = CanvasTodo.objects.filter(user=user)
        canvas = canvas.filter(completed=False)
        return render(request, 'todo/index.html', {'tasks': tasks, "subtasks":subtasks, "user":user, "show_all":show_all, "canvas":canvas,})

    else:
        current = request.user.id
        return HttpResponseRedirect('/' + str(current))

@login_required
def all(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # user = User.objects.get(id=user_id)
    if user == request.user:
        tasks = (Todo.objects.filter(user=user))
        
        tasks = tasks.order_by('due')
        # tasks.append(CanvasTodo.objects.filter(user=user))
        subtasks = Subtask.objects.all()
        show_all = True
        canvas = CanvasTodo.objects.filter(user=user)
        return render(request, 'todo/index.html', {'tasks': tasks, "subtasks":subtasks, "user":user, "show_all":show_all, "canvas":canvas,})

    else:
        current = request.user.id
        return HttpResponseRedirect('/' + str(current))
@login_required
def unlink(request):
    user = request.user
    for t in CanvasTodo.objects.filter(user=user):
        t.delete()
    user.canvasuser.canvasLinked = False
    user.save()
    return HttpResponseRedirect('/')


@login_required
def canvas_user(request):
    user = User.objects.get(id=request.user.id)
    if not user.canvasuser.canvasLinked:
        return HttpResponseRedirect('/canvas-link')

    access_token = user.canvasuser.APIkey

    getstring = "https://westminster.instructure.com/api/v1/users/self?access_token=" + access_token
    response = requests.get(getstring)
    data = response.json()

    for key in data.keys():
        if key == 'errors':
    # if data.keys().contains('errors'):
            user.canvasuser.canvasLinked = False
            user.save()
            return HttpResponseRedirect('/')
    name = data['name']
    img = data['avatar_url']

    user.canvasuser.name = name
    user.canvasuser.img = img
    user.save()
    # print("\n")
    # for i in data:
    #     print(i, data[i])
    # print("\n")

    todostring = "https://westminster.instructure.com/api/v1/users/self/todo?access_token=" + access_token
    tosponse = requests.get(todostring)
    todo = tosponse.json()

    # for key in todo.keys():
    #     if key == 'errors':
    #         user.canvasuser.canvasLinked = False
    #         user.save()
    #         return HttpResponseRedirect('/')
    assignments = []

    # print("\n")
    for i in todo:
        # print(i)
        # print("\n \n")
        assignments.append({'id': i['assignment']['id'], 'name':i['assignment']['name'], 'description':i['assignment']['description'], 'due': i['assignment']['due_at'], 'link':i['assignment']['html_url'], 'course':i['assignment']['course_id'] } )
        for j in i:
        # for x in i['assignment']:
            # print(x,": " ,i["assignment"][x], "\n")
            # print(x, j[x])
            
            pass
            # print(j, i[j],"\n")
            # print("\n")


    addedlist = []
    for item in CanvasTodo.objects.filter(user=user):
        addedlist.append(item.assignment_id)

    # print(addedlist)


    for assignment in assignments:
        a = CanvasTodo(
            title=assignment['name'], description=assignment['description'],
            due=assignment['due'], link=assignment['link'], assignment_id=assignment['id'],
            course_id=assignment['course'], user=user
        )
        # print("\n",a)
        if not addedlist.__contains__(a.assignment_id):
            a.save()
            # print(a)
            # pass

    return HttpResponseRedirect('/')
    # return render(request, 'todo/canvas_user.html', {'data':data, 'name':name, 'img':img, 'todo':todo, 'assignments':assignments})