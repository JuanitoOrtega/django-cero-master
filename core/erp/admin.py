from django.contrib import admin
from .models import Employee, Type, Category

# Register your models here.
admin.site.register(Employee)
admin.site.register(Type)
admin.site.register(Category)