# Generated by Django 4.0.4 on 2022-08-23 20:28

import datetime
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
            name='Destinataire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('prenom', models.CharField(max_length=200)),
                ('telephone', models.CharField(max_length=200)),
                ('gmail', models.CharField(max_length=200)),
                ('adresse', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'destinataire',
                'verbose_name_plural': 'destinataires',
            },
        ),
        migrations.CreateModel(
            name='Expediteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('prenom', models.CharField(max_length=200)),
                ('telephone', models.CharField(max_length=200)),
                ('gmail', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'expediteur',
                'verbose_name_plural': 'expediteurs',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'province',
                'verbose_name_plural': 'provinces',
            },
        ),
        migrations.CreateModel(
            name='Colis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('frais', models.FloatField()),
                ('poids', models.FloatField()),
                ('date_enregistrement', models.DateField(default=datetime.date.today)),
                ('code', models.CharField(max_length=200)),
                ('destinataire', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='login.destinataire')),
                ('expediteur', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='login.expediteur')),
                ('province_destinataire', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='province_destination', to='login.province')),
                ('province_expediteur', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='province_origine', to='login.province')),
            ],
            options={
                'verbose_name': 'colis',
                'verbose_name_plural': 'colis',
            },
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('telephone', models.CharField(max_length=200)),
                ('profil', models.CharField(max_length=200)),
                ('mdp', models.CharField(max_length=200)),
                ('province', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='login.province')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'agent',
                'verbose_name_plural': 'agents',
            },
        ),
    ]