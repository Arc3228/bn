# Generated by Django 3.2.25 on 2025-02-19 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='file_book',
        ),
        migrations.AlterField(
            model_name='book',
            name='published_date',
            field=models.DateField(verbose_name='Дата написания'),
        ),
    ]
