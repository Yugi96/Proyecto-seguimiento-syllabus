# Generated by Django 2.0.7 on 2018-07-18 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('universidad', '0016_remove_curso_periodo'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='periodo',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='universidad.Periodo'),
        ),
    ]
