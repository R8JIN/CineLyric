# Generated by Django 5.0.1 on 2024-02-26 13:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0005_bookmark'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='bid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='image_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='type',
            field=models.CharField(choices=[('movie', 'movie'), ('plot', 'plot'), ('music', 'music')], default=None, max_length=20),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
