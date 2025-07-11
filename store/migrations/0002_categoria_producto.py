# Generated by Django 5.1.4 on 2025-07-07 19:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Categoría del Producto', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Nombre del Producto', max_length=100)),
                ('precio', models.IntegerField(help_text='Precio', null=True)),
                ('stock', models.IntegerField(help_text='Cantidad en stock', null=True)),
                ('imagen', models.ImageField(null=True, upload_to='productos')),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.categoria')),
            ],
        ),
    ]
