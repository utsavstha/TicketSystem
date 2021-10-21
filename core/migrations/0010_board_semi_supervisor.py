# Generated by Django 3.2.5 on 2021-10-04 08:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20210929_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='semi_supervisor',
            field=models.ManyToManyField(blank=True, related_name='board_semi_supervisors', to=settings.AUTH_USER_MODEL),
        ),
    ]
