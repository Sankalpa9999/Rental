# Generated by Django 5.1.4 on 2025-02-05 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0002_user_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Bio',
            field=models.TextField(max_length=500),
        ),
    ]
