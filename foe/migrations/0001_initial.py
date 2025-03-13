# Generated by Django 5.1.6 on 2025-03-13 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Foe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_circ', models.CharField(help_text='Número/referência de Circuito', max_length=20, verbose_name='Número de circuito')),
                ('cliente', models.TextField(default='', help_text='Nome do cliente', max_length=150, verbose_name='Cliente')),
                ('dist_iet', models.DecimalField(decimal_places=3, default=0, help_text='Distância IET50', max_digits=6, verbose_name='Distância IET50')),
                ('dist_optica', models.DecimalField(decimal_places=3, default=0, help_text='Distância Óptica', max_digits=6, verbose_name='Distância Óptica')),
                ('data_pedido', models.DateField(help_text='Data do pedido', verbose_name='Data do pedido')),
                ('data_entrega', models.DateField(help_text='Data de entrega', verbose_name='Data de entrega')),
                ('estado', models.TextField(default='Inst', help_text='Estado do circuito', max_length=20, verbose_name='Estado do circuito')),
                ('local_a', models.TextField(default='', help_text='Local A', max_length=150, verbose_name='Local A')),
                ('equip_a', models.TextField(default='', help_text='Equipamento local A', max_length=20, verbose_name='Equipamento local A')),
                ('slot_a', models.CharField(default='---', help_text='Slot local A', max_length=15, verbose_name='Slot local A')),
                ('porta_a', models.CharField(default='---', help_text='Porta local A', max_length=15, verbose_name='Porta local A')),
                ('local_b', models.TextField(default='', help_text='Local B', max_length=150, verbose_name='Local B')),
                ('equip_b', models.TextField(default='', help_text='Equipamento local B', max_length=20, verbose_name='Equipamento local B')),
                ('slot_b', models.CharField(default='---', help_text='Slot local B', max_length=15, verbose_name='Slot local B')),
                ('porta_b', models.CharField(default='---', help_text='Porta local B', max_length=15, verbose_name='Porta local B')),
                ('observacoes', models.TextField(default='', help_text='Observações', max_length=150, verbose_name='Observações')),
            ],
            options={
                'ordering': ['n_circ'],
            },
        ),
    ]
