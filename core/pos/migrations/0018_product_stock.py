# Generated by Django 4.1.1 on 2022-10-02 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0017_alter_sale_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=0, verbose_name='Stock'),
        ),
    ]