from django.contrib import admin
from .models import Sucursal, Empleado, Carro, Moto, Venta


admin.site.register(Sucursal)
admin.site.register(Empleado)
admin.site.register(Carro)
admin.site.register(Moto)
admin.site.register(Venta)
