# Generated by Django 4.1.7 on 2023-02-18 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("podcasts", "0004_alter_episode_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="podcast",
            name="name",
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
