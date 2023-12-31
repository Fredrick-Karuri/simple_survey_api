# Generated by Django 4.2.7 on 2023-11-13 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0017_remove_file_question_remove_response_file_file_file_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='file',
        ),
        migrations.RemoveField(
            model_name='file',
            name='response',
        ),
        migrations.AddField(
            model_name='file',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey.question'),
        ),
        migrations.AddField(
            model_name='response',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
