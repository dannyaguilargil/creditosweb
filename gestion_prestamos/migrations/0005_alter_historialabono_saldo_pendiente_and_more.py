# Generated by Django 5.1.7 on 2025-03-13 19:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_prestamos', '0004_historialabono_saldo_pendiente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialabono',
            name='saldo_pendiente',
            field=models.BigIntegerField(verbose_name='Saldo pendiente'),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='valorcredito',
            field=models.BigIntegerField(editable=False, verbose_name='Valor del crédito'),
        ),
        migrations.CreateModel(
            name='ruta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('monto', models.BigIntegerField(verbose_name='Monto del abono')),
                ('concepto', models.CharField(max_length=100, verbose_name='Concepto del gasto')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clientes', to='gestion_prestamos.cliente')),
            ],
        ),
    ]
