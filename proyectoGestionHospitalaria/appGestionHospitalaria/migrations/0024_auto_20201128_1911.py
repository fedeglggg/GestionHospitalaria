# Generated by Django 3.0.8 on 2020-11-28 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appGestionHospitalaria', '0023_remove_turno_timeto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiofile',
            name='descripcion',
            field=models.CharField(help_text='Ingrese descriptivo del archivo', max_length=20),
        ),
    ]
