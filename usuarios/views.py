from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from .models import Venta
from .forms import VentaForm
import requests
from django.http import HttpResponse
from django.shortcuts import render


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


import requests
#from django.http import HttpResponse


""" def consumir_api(request):
    url ="https://newsapi.org/v2/everything?q=Apple&from=2024-12-23&sortBy=popularity"
    headers = {"Authorization": "2156358b44154dbcb8b3948072e668eb"}
    error = None
    try:
        response = requests.get(url, headers=headers)
        data = response.json() if response.status_code == 200 else {}
    except requests.exceptions as e:
        error = {"error": e}

    #return data["articles"][0].keys()
    titles = [article["title"] for article in data["articles"] if "title" in article]

    return render(request, "usuarios/api.html", {"titles": titles, "error": error})
 """

def cars_api(request):
    cars = []  
    if request.method == "POST":
        mod = request.POST.get("model")  # Obtener el modelo desde el formulario
        url = "https://api.api-ninjas.com/v1/cars?limit=25&model={}".format(mod)
        headers = {"X-Api-Key": "84TFyrGxurQwhjxgvyxG7w==dSKCoid10pCNRDA3"}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                cars = response.json()
                cars = [
                    {'make': car['make'], 'model':car['model'], 'year' : car['year']} for car in cars
                ] 
            else:
                cars = [f"Error: HTTP {response.status_code}"]
        except requests.exceptions.RequestException as e:
            cars = [f"Error: {str(e)}"]

    return render(request, 'usuarios/api.html', {'cars': cars})