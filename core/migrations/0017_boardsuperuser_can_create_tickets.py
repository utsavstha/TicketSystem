# Generated by Django 3.2.7 on 2021-10-21 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_remove_boardsuperuser_can_create_tickets'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardsuperuser',
            name='can_create_tickets',
            field=models.BooleanField(default=False),
        ),
    ]
