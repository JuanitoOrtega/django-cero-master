# Generated by Django 4.1.1 on 2022-10-06 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0020_rename_detailsale_saleproduct_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='birthday',
            field=models.DateField(verbose_name='Fecha de nacimiento'),
        ),
    ]
