# Generated by Django 5.0.3 on 2024-03-30 20:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_matchregistration_player'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchregistration',
            name='player',
        ),
        migrations.AddField(
            model_name='matchregistration',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='match_registrations', to=settings.AUTH_USER_MODEL, verbose_name='User'),
            preserve_default=False,
        ),
    ]
