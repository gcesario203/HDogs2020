# Generated by Django 3.0.4 on 2020-04-20 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='administrador',
            options={'ordering': ('nome',), 'verbose_name': 'administrador', 'verbose_name_plural': 'administradores'},
        ),
    ]
