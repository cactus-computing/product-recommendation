# Generated by Django 3.1.4 on 2021-04-22 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20210421_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='productattributes',
            name='vendor',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
