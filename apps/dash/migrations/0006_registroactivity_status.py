# Generated by Django 5.0.7 on 2024-08-16 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0005_registroactivity_progress_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='registroactivity',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
