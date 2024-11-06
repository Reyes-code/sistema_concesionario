from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Sucursal(models.Model):
    sucursal_id = models.AutoField(primary_key=True)  # Usamos AutoField para autoincrementar el ID
    nombre_sucursal = models.CharField(max_length=17)
    direccion = models.CharField(max_length=40)
    ciudad = models.CharField(max_length=40)
    cantidad_empleados = models.IntegerField()

    def __str__(self):
        return self.nombre_sucursal

class Empleado(models.Model):
    empleado_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=17)
    apellido = models.CharField(max_length=17)
    celular = models.CharField(max_length=10)
    ciudad_donde_reside = models.CharField(max_length=40)
    direccion_vivienda = models.CharField(max_length=40)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Carro(models.Model):
    vin_carro = models.CharField(max_length=17, primary_key=True)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    año = models.IntegerField()
    color = models.CharField(max_length=20)
    n_puertas = models.IntegerField()
    cantidad_disponible = models.IntegerField()
    transmision = models.CharField(max_length=20)
    peso = models.CharField(max_length=7)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.año})"

class Moto(models.Model):
    vin_moto = models.CharField(max_length=17, primary_key=True)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    año = models.IntegerField()
    color = models.CharField(max_length=20)
    cilindraje = models.IntegerField()
    cantidad_disponible = models.IntegerField()
    transmision = models.CharField(max_length=20)
    peso = models.CharField(max_length=7)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.año})"

class Venta(models.Model):
    venta_id = models.AutoField(primary_key=True)
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, null=True, blank=True, related_name='ventas')
    moto = models.ForeignKey(Moto, on_delete=models.CASCADE, null=True, blank=True, related_name='ventas')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    fecha = models.DateField()
    cantidad_ventas = models.IntegerField()

    def __str__(self):
        return f"Venta ID {self.venta_id} por {self.empleado} el {self.fecha}"

# Configuración de grupos y permisos
@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    # Crear grupos
    admin_group, created = Group.objects.get_or_create(name='Admin')
    employee_group, created = Group.objects.get_or_create(name='Empleado')
    viewer_group, created = Group.objects.get_or_create(name='Visualizador')

    # Obtener permisos para los grupos
    for model in [Sucursal, Empleado, Carro, Moto, Venta]:
        content_type = ContentType.objects.get_for_model(model)
        
        # Permisos de admin
        all_permissions = Permission.objects.filter(content_type=content_type)
        admin_group.permissions.add(*all_permissions)

        # Permisos de empleado (agregar y editar)
        employee_permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=[f'add_{model._meta.model_name}', f'change_{model._meta.model_name}']
        )
        employee_group.permissions.add(*employee_permissions)

        # Permisos de visualizador (solo ver)
        viewer_permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=[f'view_{model._meta.model_name}']
        )
        viewer_group.permissions.add(*viewer_permissions)

    # Crear usuarios y asignarles grupos si no existen
    if not User.objects.filter(username='adminuser').exists():
        admin_user = User.objects.create_user('adminuser', 'admin@example.com', 'password')
        admin_user.groups.add(admin_group)

    if not User.objects.filter(username='employeeuser').exists():
        employee_user = User.objects.create_user('employeeuser', 'employee@example.com', 'password')
        employee_user.groups.add(employee_group)

    if not User.objects.filter(username='vieweruser').exists():
        viewer_user = User.objects.create_user('vieweruser', 'viewer@example.com', 'password')
        viewer_user.groups.add(viewer_group)
