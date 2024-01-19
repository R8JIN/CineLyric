# Generated by Django 5.0.1 on 2024-01-19 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Song', '0006_alter_billboardlyric_release_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackLyric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_name', models.CharField(max_length=255)),
                ('track_name', models.CharField(max_length=255)),
                ('genre', models.CharField(max_length=255)),
                ('lyrics', models.TextField()),
                ('release_date', models.IntegerField()),
                ('youtube_link', models.URLField(blank=True, null=True)),
                ('spotify_link', models.URLField(blank=True, null=True)),
                ('album', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]