# Generated by Django 2.0.7 on 2018-07-16 22:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('universidad', '0008_auto_20180716_1742'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='periodo',
            name='per_codigo',
        ),
        migrations.AddField(
            model_name='periodo',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
