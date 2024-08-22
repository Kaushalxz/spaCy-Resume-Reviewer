# Generated by Django 5.0.6 on 2024-07-23 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumeApp', '0006_remove_resume_job_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='text_content',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='resume',
            name='file',
            field=models.FileField(upload_to='resumes/'),
        ),
    ]
