# Generated by Django 3.1.3 on 2021-01-21 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordersapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='активен'),
        ),
    ]
