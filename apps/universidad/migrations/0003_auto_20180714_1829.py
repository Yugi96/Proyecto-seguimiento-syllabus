# Generated by Django 2.0.7 on 2018-07-14 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universidad', '0002_auto_20180712_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignatura',
            name='asi_nombre',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]