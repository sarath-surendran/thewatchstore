# Generated by Django 4.1.7 on 2023-04-25 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_variations_variation_category_and_more'),
        ('orders', '0004_remove_orderproduct_variaton_orderproduct_variaton'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='variaton',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='varition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.variations'),
        ),
    ]