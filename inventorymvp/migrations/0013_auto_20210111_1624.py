# Generated by Django 3.1.4 on 2021-01-11 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventorymvp', '0012_auto_20210111_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydata',
            name='document_location',
            field=models.CharField(max_length=500),
        ),
    ]
