from django.urls import path
from .views import login_view, home_view, editar_venta
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', login_view, name='login'),  # Asegúrate de que esta ruta sea correcta
    path('home/', home_view, name='home'),  # Redirige correctamente a home
    path('editar-venta/<int:venta_id>/', editar_venta, name='editar_venta'),  # Ruta para editar venta
    path('', LogoutView.as_view(next_page='login'), name='logout'),  # Ruta para logout
]
