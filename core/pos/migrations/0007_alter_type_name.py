# Generated by Django 4.1.1 on 2022-09-12 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0006_alter_category_table_alter_type_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='Tipo'),
        ),
    ]
