# Generated by Django 3.1 on 2020-10-04 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appGestionHospitalaria', '0002_auto_20201002_0310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='especialidad',
            field=models.ManyToManyField(help_text='Seleccione una especialidad', null=True, to='appGestionHospitalaria.Especialidad'),
        ),
        migrations.AlterField(
            model_name='especialidad',
            name='name',
            field=models.CharField(help_text='Ingrese el nombre de la especialidad (p. ej. Neurología, Traumatología etc.)', max_length=100, unique=True),
        ),
    ]
