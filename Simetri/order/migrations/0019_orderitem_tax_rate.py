# Generated by Django 4.2.5 on 2024-06-13 08:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0018_orderitem_currency_rate_alter_currencyrate_rateeur_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="TAX_rate",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=0, max_digits=10
            ),
        ),
    ]
