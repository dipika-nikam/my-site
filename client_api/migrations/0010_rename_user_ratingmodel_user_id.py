# Generated by Django 4.0.6 on 2022-11-15 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client_api', '0009_rename_beautician_ratingmodel_beautician_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ratingmodel',
            old_name='user',
            new_name='user_id',
        ),
    ]
