# Generated by Django 3.2.3 on 2021-09-24 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_ticketcomment_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticketcomment',
            options={'ordering': ['-timestamp']},
        ),
        migrations.RemoveField(
            model_name='board',
            name='group',
        ),
        migrations.AddField(
            model_name='board',
            name='group',
            field=models.ManyToManyField(to='core.Group'),
        ),
    ]
