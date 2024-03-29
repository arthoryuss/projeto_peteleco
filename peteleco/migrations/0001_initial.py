# Generated by Django 2.2.6 on 2019-10-18 18:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local', models.CharField(max_length=50, verbose_name='Local')),
                ('tipo', models.CharField(blank=True, choices=[('', ''), ('banheira', 'Banheira'), ('chuveiro', 'Chuveiro'), ('filtro', 'Filtro'), ('hidromassagem', 'Hidromassagem'), ('lava-loucas', 'Lava Louças'), ('vaso-sanitario', 'Vazo Sanitário'), ('maquina-de-lavar', 'Máquina de Lavar'), ('pia', 'Pia'), ('piscina', 'Piscina'), ('ofuro', 'Ofurô'), ('outros', 'Outros')], max_length=25, null=True, verbose_name='Tipo do ponto de vazão')),
                ('status', models.BooleanField(default=True, verbose_name='Ativo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Cliente', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(verbose_name='Valor')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Data da Captura')),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensor', to='peteleco.Sensor')),
            ],
        ),
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('', ''), ('m³', 'm³'), ('R$', 'R$')], max_length=25, verbose_name='Critério')),
                ('limit', models.FloatField(verbose_name='Valor Limite')),
                ('status', models.BooleanField(default=False, verbose_name='Repetir')),
                ('date_finish', models.DateField(verbose_name='Data para término do alarme')),
                ('datecreation', models.DateTimeField(auto_now_add=True, verbose_name='Data da Criação')),
                ('sensor_alarm', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sensor_alarm', to='peteleco.Sensor')),
            ],
        ),
    ]
