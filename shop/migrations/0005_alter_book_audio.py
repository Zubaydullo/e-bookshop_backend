# Generated by Django 3.2.7 on 2021-09-18 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_book_audio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='audio',
            field=models.BooleanField(default=False),
        ),
    ]
