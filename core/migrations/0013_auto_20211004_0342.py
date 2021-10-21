# Generated by Django 3.2.5 on 2021-10-04 10:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20211004_0339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boardsuperuser',
            name='users',
        ),
        migrations.AddField(
            model_name='boardsuperuser',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]