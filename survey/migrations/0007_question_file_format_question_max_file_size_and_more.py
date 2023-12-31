# Generated by Django 4.2.7 on 2023-11-03 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_response_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='file_format',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='max_file_size',
            field=models.IntegerField(blank=True, default=5000000, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='multiple_files',
            field=models.BooleanField(default=False),
        ),
    ]
