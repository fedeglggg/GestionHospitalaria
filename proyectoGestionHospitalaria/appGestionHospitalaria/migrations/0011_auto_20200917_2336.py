# Generated by Django 3.1 on 2020-09-18 02:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appGestionHospitalaria', '0010_auto_20200917_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='obra_Social',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appGestionHospitalaria.obra_social'),
        ),
    ]
