# Generated by Django 4.0.5 on 2022-07-14 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoEleusisApp', '0020_alter_evento_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='imagen',
            field=models.ImageField(upload_to='imagenes/'),
        ),
    ]