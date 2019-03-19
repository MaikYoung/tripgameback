# Generated by Django 2.1.7 on 2019-03-19 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0008_auto_20190319_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='trip_type',
            field=models.CharField(choices=[('0', 'Ski & Snow'), ('1', 'Trekking'), ('2', 'Cultural'), ('3', 'Beach'), ('4', 'Party'), ('5', 'Festival'), ('6', 'Surf'), ('7', 'None'), ('8', 'Gastronomic')], max_length=1, null=True),
        ),
    ]
