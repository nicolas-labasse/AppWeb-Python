# Generated by Django 4.0.5 on 2022-07-12 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoEleusisApp', '0014_delete_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='integrantes',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='imagenes/'),
        ),
    ]
