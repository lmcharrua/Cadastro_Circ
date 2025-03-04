# Generated by Django 5.0.6 on 2024-07-04 09:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Circuitos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('N_Circuito', models.CharField(help_text='Numero/referencia de Circuito', max_length=20, verbose_name='Numero de circuito')),
                ('Data_Rate', models.CharField(max_length=10)),
                ('Data_Inst', models.DateField()),
                ('Data_Activ', models.DateField()),
                ('Entidade_PTR1', models.CharField(max_length=30)),
                ('Cod_Post_PTR1', models.CharField(max_length=50)),
                ('Interface_PTR1', models.CharField(max_length=30)),
                ('Equip_PTR1', models.CharField(max_length=20)),
                ('Slot_PTR1', models.CharField(default='---', max_length=5)),
                ('Trib_PTR1', models.CharField(default='0', max_length=10)),
                ('Entidade_PTR2', models.CharField(max_length=30)),
                ('Cod_Post_PTR2', models.CharField(max_length=50)),
                ('Interface_PTR2', models.CharField(max_length=30)),
                ('Equip_PTR2', models.CharField(max_length=20)),
                ('Slot_PTR2', models.CharField(default='---', max_length=5)),
                ('Trib_PTR2', models.CharField(default='0', max_length=10)),
            ],
            options={
                'ordering': ['N_Circuito'],
            },
        ),
        migrations.CreateModel(
            name='Hist_Cct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Data', models.DateField()),
                ('User', models.CharField(max_length=30)),
                ('N_Circuito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circuitos.circuitos')),
            ],
            options={
                'ordering': ['-Data'],
            },
        ),
    ]
