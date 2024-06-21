# Generated by Django 4.2.5 on 2024-06-12 13:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0017_remove_order_price_remove_order_product_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="currency_rate",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=0, max_digits=10
            ),
        ),
        migrations.AlterField(
            model_name="currencyrate",
            name="rateEUR",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="currencyrate",
            name="rateUSD",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
    ]
