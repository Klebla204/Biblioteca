from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import timedelta, date
from django.utils import timezone

class CustomUser(AbstractUser):
    ROLE_CHOICES =(
        ('Admin', 'Administrador'),
        ('Bibliotecario', 'Bibliotecario'),
        ('Estudiante', 'Estudiante'),
    )
    role= models.CharField(max_length=20, choices=ROLE_CHOICES, default='Estudiante')
    

class Libro(models.Model):
    titulo= models.CharField(max_length=200)
    autor=models.CharField(max_length=100)
    isbn=models.CharField(max_length=13, unique=True)
    descripcion=models.CharField(max_length=600, null=True, blank=True)
    cant_total=models.PositiveIntegerField()
    cant_disponible= models.PositiveIntegerField()
    fecha_publicacion= models.DateField(null=True, blank=True)
    categoria= models.CharField(max_length=100, blank=True)
    sede= models.ForeignKey('Sede',on_delete=models.CASCADE, related_name='libros', null=True, blank=True)
    
    def __str__(self):
        return f"{self.titulo}({self.autor})"
        
class Sede(models.Model):
    nombre=models.CharField(max_length=100, unique=True)
    telefono=models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.nombre
    
    
class Solicitud(models.Model):
    estudiante= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="solicitudes")
    libro= models.ForeignKey('Libro', on_delete=models.CASCADE, related_name="solicitudes")
    sede= models.ForeignKey('Sede', on_delete= models.CASCADE)
    fecha_solicitud= models.DateField(auto_now_add=True)
    fecha_expiracion= models.DateField(default=date.today()+timedelta(days=3))
    expirada= models.BooleanField(default=False)
    
    def check_expiracion(self):
        if date.today()> self.fecha_expiracion and not self.expirada:
            self.expirada=True
            self.libro.cant_disponible +=1
            self.libro.save()
            self.save()
            
            
class Prestamo(models.Model):
    estudiante= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="prestamos")
    libro= models.ForeignKey('Libro', on_delete=models.CASCADE, related_name="prestamos")
    sede= models.ForeignKey('Sede', on_delete=models.CASCADE)
    fecha_inicio= models.DateField(default=timezone.now)
    fecha_fin= models.DateField()
    activo= models.BooleanField(default=True)
    
    def finalizar(self):
        self.activo=False
        self.libro.cant_disponible +=1
        self.libro.save()
        self.save()
        def __str__(self):
            return f"{self.libro.titulo} -> {self.estudiante.username}"
        