# Generated by Django 3.2.7 on 2021-09-09 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navis', '0004_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=300, unique=True),
        ),
    ]
