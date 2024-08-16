# Generated by Django 4.2.5 on 2024-08-16 06:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0073_transaction"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="priceBuying",
        ),
        migrations.AddField(
            model_name="buyingitem",
            name="tax",
            field=models.DecimalField(decimal_places=2, default=20, max_digits=5),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="tax",
            field=models.DecimalField(decimal_places=2, default=20, max_digits=5),
        ),
    ]
