# Generated by Django 4.1.1 on 2022-09-25 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0015_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='date_joined',
            field=models.DateField(verbose_name='Fecha de venta'),
        ),
    ]
