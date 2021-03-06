# Generated by Django 3.1.4 on 2021-04-22 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20210421_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='front',
            name='store',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.store'),
        ),
        migrations.AlterField(
            model_name='integration',
            name='store',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.store'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='store',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.store'),
        ),
    ]
