from django.urls import path
from .views import login_view, home_view, editar_venta, cars_api
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', login_view, name='login'),  
    path('home/', home_view, name='home'),  
    path('editar-venta/<int:venta_id>/', editar_venta, name='editar_venta'), 
    path('', LogoutView.as_view(next_page='login'), name='logout'), 
    path('vehiculos/', cars_api, name='api')
]
