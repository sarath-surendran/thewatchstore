# Generated by Django 4.1.7 on 2023-04-27 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_variations_variation_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='selling_price',
            field=models.FloatField(),
        ),
    ]