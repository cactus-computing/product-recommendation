# Generated by Django 3.1.4 on 2021-04-20 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20210416_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='fare',
            field=models.IntegerField(null=True),
        ),
    ]