# Generated by Django 3.2.13 on 2022-05-02 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_mart', '0002_auto_20220417_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dimproduct',
            name='product_cat_name_en',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dimproduct',
            name='product_cat_name_pt',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
