# Generated by Django 3.1.4 on 2021-04-23 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20210422_1512'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderattributes',
            old_name='user',
            new_name='customer',
        ),
    ]
