# Generated by Django 4.2.5 on 2024-06-13 09:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0021_remove_orderitem_tax_rate_orderitem_tax"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="tax",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=0, max_digits=3
            ),
        ),
    ]
