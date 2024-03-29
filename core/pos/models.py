from datetime import datetime

from django.db import models
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Coalesce
from django.forms import model_to_dict

from config import settings
from core.pos.choices import genders


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Categoría')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name
        # return 'Nro: {} / Nombre: {}'.format(self.id, self.name)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['id']


class Product(models.Model):
    product_name = models.CharField(max_length=150, unique=True, verbose_name='Nombre')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Categoría')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen del producto')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio')

    def __str__(self):
        return f'{self.product_name} ({self.category.name})'

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.__str__()
        item['category'] = self.category.toJSON()
        item['image'] = self.get_image()
        item['price'] = f'{self.price:.2f}'
        return item

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}images/default/default_product.png'

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


class Client(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='Nombres')
    last_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Apellidos')
    ci = models.CharField(max_length=10, unique=True, verbose_name='Carnet de identidad')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='Correo electrónico')
    mobile = models.CharField(max_length=12, null=True, blank=True, verbose_name='Teléfono')
    birthday = models.DateField(auto_now_add=False, null=True, blank=True, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=genders, default='male', verbose_name='Género')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} - {}'.format(self.first_name, self.last_name, self.ci)

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['birthday'] = self.birthday.strftime('%d/%m/%Y')
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente')
    date_joined = models.DateField(default=datetime.now, verbose_name="Fecha de venta")
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Subtotal')
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='IVA')
    total_iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Total IVA')
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Total')

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']

    def delete(self, using=None, keep_parents=False):
        for detail in self.saleproduct_set.all():
            detail.product.stock += detail.quantity
            detail.product.save()
        super(Sale, self).delete()

    def calculate_invoice(self):
        subtotal = self.saleproduct_set.all().aggregate(result=Coalesce(Sum(F('price') * F('quantity')), 0.00, output_field=FloatField())).get('result')
        self.subtotal = subtotal
        self.total_iva = self.subtotal * float(self.iva / 100)
        self.total = float(self.subtotal) + float(self.total_iva)
        self.save()

    def get_number(self):
        return f'{self.id:06d}'

    def toJSON(self):
        item = model_to_dict(self)
        item['number'] = self.get_number()
        item['client'] = self.client.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total_iva'] = f'{self.total_iva:.2f}'
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['saleproduct'] = [i.toJSON() for i in self.saleproduct_set.all()]
        return item

    def __str__(self):
        return self.client.first_name


class SaleProduct(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name='Venta')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio')
    quantity = models.IntegerField(default=0, verbose_name='Cantidad')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Subtotal')

    def __str__(self):
        return self.product.product_name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['product'] = self.product.toJSON()
        item['price'] = f'{self.price:.2f}'
        item['subtotal'] = f'{self.subtotal:.2f}'
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        default_permissions = ()
        ordering = ['id']
