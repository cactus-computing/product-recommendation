# Generated by Django 3.1.4 on 2021-04-22 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20210422_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='customers',
            name='customers_code',
            field=models.IntegerField(default=123),
            preserve_default=False,
        ),
    ]
