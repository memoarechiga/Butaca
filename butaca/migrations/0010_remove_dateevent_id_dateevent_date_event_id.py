# Generated by Django 4.2.3 on 2023-07-19 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('butaca', '0009_alter_event_bann_img_alter_event_min_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dateevent',
            name='id',
        ),
        migrations.AddField(
            model_name='dateevent',
            name='date_event_id',
            field=models.CharField(default='1', max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]
