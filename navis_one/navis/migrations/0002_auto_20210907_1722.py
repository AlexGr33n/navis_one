# Generated by Django 3.2.7 on 2021-09-07 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('comment', models.CharField(blank=True, max_length=300, null=True)),
                ('url', models.SlugField(max_length=300, unique=True)),
            ],
            options={
                'verbose_name': 'Filter',
                'verbose_name_plural': 'Filters',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='filter',
            field=models.ManyToManyField(blank=True, null=True, related_name='product_filter', to='navis.Filter'),
        ),
    ]