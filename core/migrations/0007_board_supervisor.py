# Generated by Django 3.2.5 on 2021-09-26 11:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20210924_0252'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='supervisor',
            field=models.ManyToManyField(blank=True, related_name='board_supervisors', to=settings.AUTH_USER_MODEL),
        ),
    ]
