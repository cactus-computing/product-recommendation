# Generated by Django 3.1.4 on 2021-01-20 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0002_auto_20210120_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='suscription',
            name='created_at',
            field=models.DateField(auto_now=True),
        ),
    ]
