# Generated by Django 3.0.5 on 2020-04-15 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_library'),
    ]

    operations = [
        migrations.AddField(
            model_name='library',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]