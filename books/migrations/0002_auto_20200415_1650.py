# Generated by Django 3.0.5 on 2020-04-15 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='librarytemplate',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='librarytemplate',
            name='slug',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]