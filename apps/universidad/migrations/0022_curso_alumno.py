# Generated by Django 2.0.7 on 2018-07-18 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('universidad', '0021_auto_20180718_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='alumno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='universidad.Alumno'),
            preserve_default=False,
        ),
    ]
