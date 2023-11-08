# Generated by Django 4.2.7 on 2023-11-08 11:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('csvs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='csvs',
            name='csv_file',
            field=models.FileField(default=django.utils.timezone.now, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='csvs',
            name='file_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]