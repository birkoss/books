# Generated by Django 3.0.5 on 2020-04-15 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_library_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('active', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=0, null=True)),
                ('library', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='books.Library')),
            ],
        ),
    ]