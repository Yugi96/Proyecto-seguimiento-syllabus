# Generated by Django 2.0.7 on 2018-07-18 00:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('universidad', '0018_remove_asignatura_docente_periodo'),
    ]

    operations = [
        migrations.AddField(
            model_name='asignatura_docente',
            name='periodo',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='universidad.Periodo'),
        ),
    ]