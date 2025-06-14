# Generated by Django 5.2 on 2025-06-11 15:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('relotagrid', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('conditionnement', models.CharField(blank=True, max_length=255)),
                ('quantite_limite', models.PositiveIntegerField(help_text='Quantité minimale avant alerte')),
            ],
        ),
        migrations.CreateModel(
            name='UtilisationJournal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_utilisation', models.DateField()),
                ('quantite_utilisee', models.PositiveIntegerField()),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='utilisations', to='stock.produit')),
            ],
            options={
                'ordering': ['-date_utilisation'],
            },
        ),
        migrations.CreateModel(
            name='LivraisonMensuelle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mois', models.DateField(help_text='Ex: 2025-06-01 pour juin 2025')),
                ('quantite_livree', models.PositiveIntegerField()),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='livraisons_stock', to='relotagrid.site')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='livraisons', to='stock.produit')),
            ],
            options={
                'ordering': ['-mois'],
                'unique_together': {('site', 'produit', 'mois')},
            },
        ),
    ]
