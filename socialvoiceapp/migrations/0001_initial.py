# Generated by Django 3.0.5 on 2021-04-28 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djongo.storage
import socialvoiceapp.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(null=True, storage=djongo.storage.GridFSStorage(base_url='myfiles/', collection='myfiles'), upload_to='avatars', validators=[socialvoiceapp.validators.validate_image_file_extension])),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='socialvoiceapp.City')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='socialvoiceapp.Country')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='socialvoiceapp.Country'),
        ),
        migrations.CreateModel(
            name='AudioMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_data', models.FileField(null=True, storage=djongo.storage.GridFSStorage(base_url='myfiles/', collection='myfiles'), upload_to='messages', validators=[socialvoiceapp.validators.validate_audio_file_extension])),
                ('upload_time', models.DateTimeField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
