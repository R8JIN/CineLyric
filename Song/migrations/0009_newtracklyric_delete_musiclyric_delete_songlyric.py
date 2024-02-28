# Generated by Django 5.0.1 on 2024-02-27 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Song', '0008_tracklyric_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewTrackLyric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_name', models.CharField(max_length=255)),
                ('track_name', models.CharField(max_length=255)),
                ('genre', models.CharField(max_length=255)),
                ('type', models.CharField(default='music', max_length=255)),
                ('lyrics', models.TextField()),
                ('release_date', models.IntegerField()),
                ('youtube_link', models.URLField(blank=True, null=True)),
                ('spotify_link', models.URLField(blank=True, null=True)),
                ('album', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='MusicLyric',
        ),
        migrations.DeleteModel(
            name='SongLyric',
        ),
    ]