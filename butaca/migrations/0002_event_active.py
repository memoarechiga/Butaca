# Generated by Django 4.2.3 on 2023-07-17 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('butaca', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]