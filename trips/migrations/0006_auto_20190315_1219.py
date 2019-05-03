# Generated by Django 2.1.7 on 2019-03-15 12:19

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0005_trip_create_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='counter_verified',
        ),
        migrations.AddField(
            model_name='trip',
            name='verified_by',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None),
        ),
    ]