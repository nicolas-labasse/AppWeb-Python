from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Materia(models.Model):
    posicion = models.IntegerField()
    description = models.TextField()
    fecha = models.DateField()
    anio = models.CharField(max_length=20)



class Integrantes(models.Model):
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True)

    def __str__(self):
        return self.nombre


class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    tema = models.CharField(max_length=100)
    descripcion = models.TextField()
    disertantes = models.CharField(max_length=100)
    precio = models.IntegerField()
    precio_dolar = models.IntegerField(null=True, blank=True)
    propaganda = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='imagenes/')
    fecha_creacion = models.DateField(auto_now_add=True, null=True)
    lugar_inicio = models.CharField(max_length=100, blank=True, null=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    hora_inicio = models.TimeField(null=True, blank=True)

    def __str__(self):
        return  self.id.__str__() + " - " + self.nombre


class Lugar(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField(null=True, blank=True)
    hora = models.TimeField(null=True, blank=True)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Inscripcion(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    comprobante = models.FileField(upload_to='imagenes/', blank=True, null=True)
    fk_evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        return  self.nombre

