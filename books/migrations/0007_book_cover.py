# Generated by Django 3.0.5 on 2020-04-16 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]