# Generated by Django 5.0.4 on 2024-04-25 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='activity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]