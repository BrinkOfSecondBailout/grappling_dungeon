# Generated by Django 5.0.2 on 2024-02-09 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techniques', '0004_alter_technique_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technique',
            name='category',
            field=models.CharField(choices=[('passing', 'Passing'), ('guard', 'Guard'), ('submission', 'Submission'), ('takedown', 'Takedown'), ('counter', 'Defense/Counter'), ('escape', 'Escape'), ('other', 'Other')], max_length=20),
        ),
    ]
