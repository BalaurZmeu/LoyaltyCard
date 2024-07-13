# Generated by Django 5.0.6 on 2024-07-13 11:41

import card_manager.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='id_number',
            field=models.BigIntegerField(default=card_manager.utils.generate_id, help_text='Unique ID for this particular card across the whole system', primary_key=True, serialize=False),
        ),
    ]