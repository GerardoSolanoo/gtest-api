from django.db import models
from users.models import User

# Create your models here.
class Test(models.Model):
    nombre = models.CharField(max_length=255, null=False, unique=True)
    descripcion = models.TextField(null=True)
    autor = models.CharField(max_length=255, null=True)
    bibliografia = models.TextField(null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

class Dimension(models.Model):
    id_test = models.ForeignKey(Test, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255, null=False, unique=True)
    descripcion = models.TextField(null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

class Pregunta(models.Model):
    id_test = models.ForeignKey(Test, on_delete=models.CASCADE)
    pregunta = models.TextField(null=False)
    tipo_pregunta = models.CharField(max_length=255, null=False)
    valor_minimo = models.IntegerField(null=False)
    valor_maximo = models.IntegerField(null=False)

class Proyecto(models.Model):
    nombre = models.CharField(max_length=255, null=False)
    descripcion = models.TextField(null=True)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

class ProyectoTest(models.Model):
    id_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    id_test = models.ForeignKey(Test, on_delete=models.CASCADE)

class ProyectoDimension(models.Model):
    id_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    id_dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE)

class ProyectoPregunta(models.Model):
    id_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    id_pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)