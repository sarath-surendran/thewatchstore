# Generated by Django 4.1.7 on 2023-04-07 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.ImageField(default='photos/users/default_user.jpg', upload_to='photos/users'),
        ),
    ]
