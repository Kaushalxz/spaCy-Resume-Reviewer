# Generated by Django 5.0.6 on 2024-07-21 14:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumeApp', '0003_alter_resume_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='analysis_results',
            field=models.JSONField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resume',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
