# Generated by Django 4.1.7 on 2024-01-08 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Movie', '0009_rename_quote_quotation'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Quotation',
        ),
    ]
