# Generated by Django 3.1.4 on 2021-04-05 16:43

from django.db import migrations, models
import django.utils.timezone
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='api_url',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='consumer_key',
            field=django_cryptography.fields.encrypt(models.CharField(default=django.utils.timezone.now, max_length=500)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='store',
            name='consumer_secret',
            field=django_cryptography.fields.encrypt(models.CharField(default=django.utils.timezone.now, max_length=500)),
            preserve_default=False,
        ),
    ]