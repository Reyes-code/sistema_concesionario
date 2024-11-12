from django import forms
from .models import Venta

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['carro', 'moto', 'empleado', 'sucursal', 'fecha', 'cantidad_ventas']
