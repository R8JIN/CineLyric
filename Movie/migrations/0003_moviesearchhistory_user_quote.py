# Generated by Django 4.1.7 on 2023-12-12 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movie', '0002_moviesearchhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviesearchhistory',
            name='user_quote',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
