# Generated by Django 3.1.2 on 2020-11-21 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0006_auto_20201119_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
    ]
