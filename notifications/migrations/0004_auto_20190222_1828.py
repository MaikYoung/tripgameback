# Generated by Django 2.1.7 on 2019-02-22 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_auto_20190222_1202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='extra_info',
        ),
        migrations.AddField(
            model_name='notification',
            name='trip_related',
            field=models.IntegerField(default=None),
        ),
    ]