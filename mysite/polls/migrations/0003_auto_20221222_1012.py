# Generated by Django 3.0.3 on 2022-12-22 08:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20221218_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='poll',
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 22, 8, 12, 2, 665812, tzinfo=utc)),
        ),
        migrations.DeleteModel(
            name='Poll',
        ),
    ]