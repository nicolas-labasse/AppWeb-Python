# Generated by Django 4.0.5 on 2022-07-13 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoEleusisApp', '0015_alter_integrantes_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lugar',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lugares', to='ProyectoEleusisApp.evento'),
        ),
    ]
