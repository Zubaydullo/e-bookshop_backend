# Generated by Django 3.2.7 on 2021-09-17 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20210917_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_type',
            field=models.CharField(choices=[('Audio', 'Audio'), ('Electronic', 'Electronic'), ('Paper', 'Paper')], max_length=100),
        ),
    ]
