# Generated by Django 3.1 on 2020-08-23 01:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('browser', '0004_auto_20200823_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='modified_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]