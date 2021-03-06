# Generated by Django 3.1.7 on 2021-03-21 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20210321_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('m', 'Mantenimiento'), ('o', 'Prestamo'), ('d', 'Disponible'), ('r', 'Reservado')], default='m', help_text='Disponibilidad del libro', max_length=1),
        ),
    ]
