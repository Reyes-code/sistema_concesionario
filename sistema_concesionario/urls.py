from django.contrib import admin
from django.urls import path, include  # Agregar include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),  # Incluir las URLs de la app usuarios
]
