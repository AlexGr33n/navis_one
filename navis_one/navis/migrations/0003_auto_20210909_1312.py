# Generated by Django 3.2.7 on 2021-09-09 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navis', '0002_auto_20210907_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='comment_en',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='filter',
            name='comment_ru',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='filter',
            name='comment_uk',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='filter',
            name='name_en',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='filter',
            name='name_ru',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='filter',
            name='name_uk',
            field=models.CharField(max_length=300, null=True),
        ),
    ]