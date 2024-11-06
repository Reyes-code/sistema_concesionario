from django.urls import path
from .views import login_view, home_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home_view, name='home'),  # Asegúrate de que esta ruta sea correcta
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Ruta para logout
]
