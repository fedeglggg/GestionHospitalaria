# Generated by Django 3.1 on 2020-12-02 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appGestionHospitalaria', '0025_merge_20201129_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoestudio',
            name='especialidad',
            field=models.ForeignKey(help_text='Seleccione una especialidad', null=True, on_delete=django.db.models.deletion.CASCADE, to='appGestionHospitalaria.especialidad'),
        ),
    ]
