# Generated by Django 4.2.1 on 2023-07-18 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fleetuser',
            name='contact',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
