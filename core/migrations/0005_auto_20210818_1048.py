# Generated by Django 3.2.5 on 2021-08-18 10:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210816_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='assigned_user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
