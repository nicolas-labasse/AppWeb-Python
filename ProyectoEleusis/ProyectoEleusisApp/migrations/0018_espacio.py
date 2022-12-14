# Generated by Django 4.0.5 on 2022-07-13 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoEleusisApp', '0017_alter_lugar_evento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Espacio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('hora', models.TimeField(blank=True, null=True)),
                ('evento', models.ManyToManyField(to='ProyectoEleusisApp.evento')),
            ],
        ),
    ]
