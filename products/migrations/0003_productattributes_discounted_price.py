# Generated by Django 3.1.4 on 2021-04-07 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210403_0105'),
    ]

    operations = [
        migrations.AddField(
            model_name='productattributes',
            name='discounted_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True),
        ),
    ]
