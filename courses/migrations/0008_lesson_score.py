# Generated by Django 5.0.4 on 2024-04-26 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_lesson_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]