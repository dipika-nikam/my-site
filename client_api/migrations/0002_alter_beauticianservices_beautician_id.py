# Generated by Django 4.0.6 on 2022-11-10 04:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
        ('client_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beauticianservices',
            name='beautician_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.beautician'),
        ),
    ]
