# Generated by Django 2.0.7 on 2018-07-18 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universidad', '0020_asignatura_docente_asi_doc_eliminado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumno',
            name='alu_cedula',
        ),
        migrations.RemoveField(
            model_name='curso',
            name='alumno',
        ),
        migrations.AddField(
            model_name='alumno',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
