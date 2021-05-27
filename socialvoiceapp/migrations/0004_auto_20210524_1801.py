# Generated by Django 3.0.5 on 2021-05-24 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialvoiceapp', '0003_auto_20210524_1748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audiomessage',
            name='id',
        ),
        migrations.RemoveField(
            model_name='city',
            name='id',
        ),
        migrations.RemoveField(
            model_name='country',
            name='id',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='id',
        ),
        migrations.AddField(
            model_name='audiomessage',
            name='_id',
            field=models.IntegerField(auto_created=True, default=0, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AddField(
            model_name='city',
            name='_id',
            field=models.IntegerField(auto_created=True, default=0, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AddField(
            model_name='country',
            name='_id',
            field=models.IntegerField(auto_created=True, default=0, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='_id',
            field=models.IntegerField(auto_created=True, default=0, primary_key=True, serialize=False, unique=True),
        ),
    ]