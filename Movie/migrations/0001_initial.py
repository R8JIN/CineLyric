# Generated by Django 4.1.7 on 2023-11-28 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MovieQuotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.CharField(max_length=255)),
                ('movie', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=255)),
            ],
        ),
    ]
