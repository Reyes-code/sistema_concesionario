from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from .models import Venta
from .forms import VentaForm

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

@login_required
def home_view(request):
    ventas = Venta.objects.all()  # Obtener todas las ventas
    return render(request, 'usuarios/home.html', {'ventas': ventas})

@login_required
@permission_required('usuarios.change_venta', raise_exception=True)
def editar_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirige a la página de inicio después de editar
    else:
        form = VentaForm(instance=venta)
    return render(request, 'usuarios/editar_venta.html', {'form': form})
