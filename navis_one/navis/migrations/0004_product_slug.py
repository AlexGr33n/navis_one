# Generated by Django 3.2.7 on 2021-09-09 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navis', '0003_auto_20210909_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
