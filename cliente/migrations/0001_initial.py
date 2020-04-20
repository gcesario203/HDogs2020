# Generated by Django 3.0.4 on 2020-04-20 22:30

import cliente.models
from django.db import migrations, models
import django.db.models.deletion
import django_enum_choices.choice_builders
import django_enum_choices.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_CPF', models.CharField(max_length=16)),
                ('_nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('_email', models.EmailField(blank=True, max_length=200, verbose_name='E-Mail')),
                ('_tel', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('_CTPS', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name': 'administrador',
                'verbose_name_plural': 'administradores',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_CPF', models.CharField(max_length=16)),
                ('_nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('_email', models.EmailField(blank=True, max_length=200, verbose_name='E-Mail')),
                ('_tel', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
            },
        ),
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('administrador_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cliente.Administrador')),
            ],
            options={
                'verbose_name': 'monitor',
                'verbose_name_plural': 'monitores',
            },
            bases=('cliente.administrador', models.Model),
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_nome_pet', models.CharField(max_length=30, verbose_name='Nome do pet')),
                ('_tipo', models.CharField(default='Cachorro', max_length=50, verbose_name='Tipo')),
                ('_porte', django_enum_choices.fields.EnumChoiceField(choice_builder=django_enum_choices.choice_builders.value_value, choices=[('P', 'P'), ('M', 'M'), ('G', 'G')], enum_class=cliente.models.Porte, max_length=1, verbose_name='Porte')),
                ('_especie', models.CharField(max_length=50, null=True, verbose_name='Espécie:')),
                ('_racao', models.CharField(max_length=30, verbose_name='Ração')),
                ('data_entrada', models.DateTimeField(verbose_name='Data de entrada')),
                ('_servicos', models.TextField(blank=True, max_length=400, verbose_name='Serviços')),
                ('_dono', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.Cliente', verbose_name='Dono')),
            ],
            options={
                'verbose_name': 'mascote',
                'verbose_name_plural': 'mascotes',
            },
        ),
    ]
