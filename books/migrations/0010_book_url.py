# Generated by Django 3.0.5 on 2020-04-16 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_book_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='url',
            field=models.CharField(default='', max_length=300),
        ),
    ]
