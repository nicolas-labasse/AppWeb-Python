# Generated by Django 4.0.5 on 2022-07-11 00:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoEleusisApp', '0005_remove_tiempo_evento_tiempo_lugares'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tiempo',
            name='hora',
        ),
    ]