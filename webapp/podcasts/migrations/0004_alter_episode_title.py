# Generated by Django 4.1.7 on 2023-02-18 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("podcasts", "0003_remove_pod_podcast_podcast_rss"),
    ]

    operations = [
        migrations.AlterField(
            model_name="episode",
            name="title",
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
