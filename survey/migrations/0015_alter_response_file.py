# Generated by Django 4.2.7 on 2023-11-13 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0014_user_response_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='certificates/'),
        ),
    ]
