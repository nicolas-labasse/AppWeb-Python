# Generated by Django 4.0.5 on 2022-07-13 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoEleusisApp', '0016_alter_lugar_evento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lugar',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProyectoEleusisApp.evento'),
        ),
    ]
