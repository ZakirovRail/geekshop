# Generated by Django 3.1.3 on 2021-01-03 12:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0007_auto_20210103_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 5, 12, 30, 54, 231700, tzinfo=utc), verbose_name='актуальность ключа'),
        ),
    ]
