# Generated by Django 3.0.4 on 2020-04-30 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0002_auto_20200430_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='data_entrada',
            field=models.DateField(auto_now_add=True, verbose_name='Data de entrada'),
        ),
    ]