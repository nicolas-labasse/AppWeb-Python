# Generated by Django 4.0.5 on 2022-07-11 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoEleusisApp', '0010_remove_evento_fecha_creacion_evento_propaganda'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='fecha_creacion',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
