# Generated by Django 3.2.5 on 2021-08-26 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_ticketcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='priority',
            name='priority_value',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
