# Generated by Django 3.1.3 on 2023-11-07 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
