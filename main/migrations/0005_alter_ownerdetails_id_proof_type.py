# Generated by Django 5.0.4 on 2024-06-22 01:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_addres1_ownerdetails_address1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownerdetails',
            name='id_proof_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='id_proof', to='main.dropdown'),
        ),
    ]
