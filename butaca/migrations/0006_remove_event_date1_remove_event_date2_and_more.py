# Generated by Django 4.2.3 on 2023-07-19 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('butaca', '0005_event_bann_img_event_min_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='date1',
        ),
        migrations.RemoveField(
            model_name='event',
            name='date2',
        ),
        migrations.RemoveField(
            model_name='event',
            name='date3',
        ),
        migrations.RemoveField(
            model_name='event',
            name='date4',
        ),
    ]