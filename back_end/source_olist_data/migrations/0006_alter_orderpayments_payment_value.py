# Generated by Django 3.2.13 on 2022-04-29 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('source_olist_data', '0005_auto_20220426_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpayments',
            name='payment_value',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
