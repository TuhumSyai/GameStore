# Generated by Django 5.2 on 2025-04-16 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_game_description_remove_genre_slug_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
