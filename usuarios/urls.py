from django.urls import path
from .views import login_view, home_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', login_view, name='login'),  # Asegúrate de que esta ruta sea correcta
    path('home/', home_view, name='home'),  # Redirige correctamente a home
    path('login/', LogoutView.as_view(next_page='login'), name='logout'),  # Ruta para logout
]
