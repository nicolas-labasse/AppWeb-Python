# Generated by Django 4.0.5 on 2022-07-14 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoEleusisApp', '0019_evento_fecha_inicio_evento_hora_inicio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='imagenes/'),
        ),
    ]
