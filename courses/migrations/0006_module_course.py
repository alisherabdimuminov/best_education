# Generated by Django 5.0.4 on 2024-04-26 04:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_alter_lesson_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
            preserve_default=False,
        ),
    ]
