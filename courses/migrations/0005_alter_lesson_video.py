# Generated by Django 5.0.4 on 2024-04-26 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_lesson_finishers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video',
            field=models.URLField(max_length=1000),
        ),
    ]