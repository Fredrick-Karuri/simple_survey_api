# Generated by Django 4.2.7 on 2023-11-13 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0018_remove_file_file_remove_file_response_file_question_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='submitted_at',
            field=models.DateTimeField(null=True),
        ),
    ]
