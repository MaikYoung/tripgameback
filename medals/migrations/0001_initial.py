# Generated by Django 2.1.7 on 2019-03-19 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Medals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ski', models.BooleanField(default=False)),
                ('ski_count', models.IntegerField(default=0)),
                ('trekking', models.BooleanField(default=False)),
                ('trekking_count', models.IntegerField(default=0)),
                ('cultural', models.BooleanField(default=False)),
                ('cultural_count', models.IntegerField(default=0)),
                ('beach', models.BooleanField(default=False)),
                ('beach_count', models.IntegerField(default=0)),
                ('party', models.BooleanField(default=False)),
                ('party_count', models.IntegerField(default=0)),
                ('festival', models.BooleanField(default=False)),
                ('festival_count', models.IntegerField(default=0)),
                ('surf', models.BooleanField(default=False)),
                ('surf_count', models.IntegerField(default=0)),
                ('gastronomic', models.BooleanField(default=False)),
                ('gastronomic_count', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]