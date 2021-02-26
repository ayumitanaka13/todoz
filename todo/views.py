from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo

# Create your views here.
def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return  render(request, 'todo/signupuser.html', { 'form':UserCreationForm() })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(
                    request,
                    'todo/signupuser.html',
                    {
                        'form': UserCreationForm(),
                        'error': 'That user name has already taken.'
                    }
                )
        else:
            return render(request, 'todo/signupuser.html', { 'form':UserCreationForm(), 'error': 'Password did not match' })
    

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', { 'form': AuthenticationForm() })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(
                request,
                'todo/loginuser.html',
                { 
                    'form': AuthenticationForm(),
                    'error': 'Username and password are incorrect.'
                }
            )
        else:
            login(request, user)
            return redirect('currenttodos')

def currenttodos(request):
    todos = Todo.objects.all()
    return render(request, 'todo/currenttodos.html', { 'todos':todos })

def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', { 'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            request,
            'todo/createtodo.html',
            {
                'form': TodoForm(),
                'error': 'Error!'
            }
