from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Venta



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige a la página de inicio
        else:
            return render(request, 'usuarios/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'usuarios/login.html')

def home_view(request):
    return render(request, 'usuarios/home.html')  # Asegúrate de crear este template

@login_required
def home_view(request):
    ventas = Venta.objects.all()  # Obtener todas las ventas
    return render(request, 'usuarios/home.html', {'ventas': ventas})

