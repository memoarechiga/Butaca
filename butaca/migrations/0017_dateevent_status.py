# Generated by Django 4.2.3 on 2023-07-21 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('butaca', '0016_alter_event_promoter'),
    ]

    operations = [
        migrations.AddField(
            model_name='dateevent',
            name='status',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]