from unicodedata import category

from django.db import models
from datetime import datetime

from django.db.models.fields import related


# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Tipo')

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'
        db_table = 'tipo'
        ordering = ['id']

    def __srt__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Categorías')

    def __srt__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        db_table = 'categoria'
        ordering = ['id']


class Employee(models.Model):
    category = models.ManyToManyField(Category, verbose_name='Categoría')
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, verbose_name='Tipo')
    first_name = models.CharField(max_length=255, verbose_name="Nombre")
    last_name = models.CharField(max_length=255, verbose_name="Apellidos")
    ci = models.CharField(max_length=10, unique=True, verbose_name="Carnet de Identidad")
    age = models.PositiveIntegerField(default=0, verbose_name="Edad")
    salary = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name="Salario")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', null=True, blank=True, verbose_name="Avatar")
    gender = models.CharField(max_length=50, verbose_name="Género")
    cv = models.FileField(upload_to='cv/%Y/%m/%d', null=True, blank=True, verbose_name='Hoja de vida')
    date_joined = models.DateField(default=datetime.now, verbose_name="Última conexión")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        db_table = 'empleado'
        ordering = ['id']

    def __str__(self):
        return self.first_name + " " + self.last_name