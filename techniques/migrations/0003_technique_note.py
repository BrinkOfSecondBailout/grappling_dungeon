# Generated by Django 5.0.1 on 2024-02-08 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techniques', '0002_technique_cropped_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='technique',
            name='note',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]