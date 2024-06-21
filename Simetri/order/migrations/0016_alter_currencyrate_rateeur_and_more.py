# Generated by Django 4.2.5 on 2024-06-08 14:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0015_rename_invoicenumber_order_order_number_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="currencyrate",
            name="rateEUR",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=36.0, max_digits=10
            ),
        ),
        migrations.AlterField(
            model_name="currencyrate",
            name="rateUSD",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=33.32, max_digits=10
            ),
        ),
    ]
