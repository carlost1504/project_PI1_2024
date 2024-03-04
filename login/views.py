from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        print('enviado por GET')
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        print(request.POST)
        print('obteniendo datos')
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Formulario inválido. Inténtelo de nuevo.'
                })


def tasks(request):
    return render(request,'tasks.html')

def signin(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tasks')
            else:
                return render(request, 'signin.html', {'form': form, 'error': 'Usuario y/o contraseña inválidos'})
        else:
            return render(request, 'signin.html', {'form': form})
    
        
    