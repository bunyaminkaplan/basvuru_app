# Generated by Django 5.0.3 on 2025-03-06 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basvuru_app', '0003_basvuru_details_gerekce'),
    ]

    operations = [
        migrations.AddField(
            model_name='basvuru_details',
            name='basvuru_sahibi',
            field=models.CharField(default='none', max_length=30),
        ),
    ]
