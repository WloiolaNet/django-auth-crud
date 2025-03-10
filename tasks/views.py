
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_protect
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def signup(request):
    if request.method == 'GET':
         return render(request,'signup.html',{
        'form': UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #registro de usuario
            try:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('tasks')
            except IntegrityError:
                return render(request,'signup.html',{
                'form': UserCreationForm,
                "error" : 'O nome de usuário já existe!'
                })
        else:
             return render(request,'signup.html',{
                'form': UserCreationForm,
                "error" : 'A senha não corresponde!'
                })
@login_required          
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    # Verifica se a última ação foi completar uma tarefa
    # title = "Tasks Completed" if request.session.get('last_action') == 'complete' else "Tasks Pending"
    # Após carregar a página, reseta a sessão para evitar que fique sempre como "Tasks Completed"
    # request.session['last_action'] = None  
    # return render(request,'tasks.html',{'tasks': tasks, 'title': title})
    return render(request,'tasks.html',{'tasks': tasks,'title': "Tarefas pendentes"})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'tasks.html',{'tasks': tasks,'title': "Tarefas concluídas"})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request,'create_task.html',{
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit= False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'create_task.html',{'form': TaskForm, 'error':'Forneça dados válidos!'})
        
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task= get_object_or_404(Task,pk=task_id)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html',{'task': task, 'form': form})
    else:
        try:
            task= get_object_or_404(Task,pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html',{'task': task, 'form': form,
            'error': "Erro ao atualizar a tarefa!"})

@login_required        
def complete_task(request, task_id):
    task= get_object_or_404(Task,pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        # Salvar na sessão que a última ação foi completar uma tarefa
        request.session['last_action'] = 'complete'
        return redirect('tasks')   
 
    
@login_required    
def delete_task(request, task_id):
    task= get_object_or_404(Task,pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method =='GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'signin.html',{
                'form': AuthenticationForm,
                'error': 'Nome de usuário ou senha estão incorretos!'
            })
        else:
            login(request,user)
            return redirect('tasks')


       