# Generated by Django 5.0.6 on 2024-07-13 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circuitos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='circuitos',
            name='Morada_PTR2',
            field=models.TextField(default=0, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='circuitos',
            name='Outras_Ref',
            field=models.TextField(default=0, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='circuitos',
            name='Propriedade',
            field=models.TextField(default=0, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='circuitos',
            name='Uset_Cct',
            field=models.TextField(default=0, max_length=150),
            preserve_default=False,
        ),
    ]
