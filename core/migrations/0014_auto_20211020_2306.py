# Generated by Django 3.2.7 on 2021-10-21 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20211004_0342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boardsuperuser',
            name='can_create_ticket',
        ),
        migrations.AlterField(
            model_name='boardsuperuser',
            name='can_complete_ticket',
            field=models.BooleanField(default=False),
        ),
    ]