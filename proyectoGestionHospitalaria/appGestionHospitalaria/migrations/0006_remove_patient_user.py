# Generated by Django 3.1 on 2020-09-18 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appGestionHospitalaria', '0005_auto_20200917_2242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='user',
        ),
    ]
