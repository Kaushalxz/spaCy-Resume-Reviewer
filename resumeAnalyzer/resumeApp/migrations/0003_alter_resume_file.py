# Generated by Django 5.0.6 on 2024-07-19 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumeApp', '0002_remove_resume_analysis_results_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]
