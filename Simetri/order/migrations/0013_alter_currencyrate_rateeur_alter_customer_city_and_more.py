# Generated by Django 4.2.5 on 2024-04-10 19:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0012_alter_currencyrate_rateeur_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="currencyrate",
            name="rateEUR",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=35.7, max_digits=10
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="city",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="customer",
            name="district",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="customer",
            name="taxOffice",
            field=models.CharField(max_length=50),
        ),
    ]
