# Generated by Django 5.0.4 on 2024-06-15 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RateReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('deleted_time', models.DateTimeField(null=True)),
                ('deleted_status', models.BooleanField(default=False)),
                ('rating', models.FloatField(default=0.0)),
                ('review', models.TextField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
