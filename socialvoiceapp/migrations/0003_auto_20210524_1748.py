# Generated by Django 3.0.5 on 2021-05-24 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialvoiceapp', '0002_auto_20210524_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
