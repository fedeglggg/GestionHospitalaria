# Generated by Django 3.1 on 2020-10-22 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appGestionHospitalaria', '0011_auto_20201022_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='timeTo',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
