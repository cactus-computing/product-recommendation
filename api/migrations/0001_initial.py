# Generated by Django 3.1.4 on 2021-03-22 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductAttributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_id', models.IntegerField(unique=True)),
                ('sku', models.CharField(default=None, max_length=2000)),
                ('name', models.CharField(max_length=2000)),
                ('price', models.FloatField(blank=True, null=True)),
                ('href', models.CharField(default=None, max_length=2000)),
                ('permalink', models.CharField(max_length=2000)),
                ('status', models.CharField(max_length=500)),
                ('stock_quantity', models.FloatField(blank=True, default=None, null=True)),
                ('company', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='UpSellPredictions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.CharField(max_length=500)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.productattributes', to_field='product_id')),
                ('recommended_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='up_sell_id', to='api.productattributes', to_field='product_id')),
            ],
        ),
        migrations.CreateModel(
            name='CrossSellPredictions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.CharField(max_length=500)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.productattributes', to_field='product_id')),
                ('recommended_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cross_sell_id', to='api.productattributes', to_field='product_id')),
            ],
        ),
    ]
