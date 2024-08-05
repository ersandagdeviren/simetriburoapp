# Generated by Django 4.2.5 on 2024-07-29 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0060_supplier"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="buyinginvoice",
            name="order",
        ),
        migrations.AddField(
            model_name="buyinginvoice",
            name="supplier",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="supplier_invoices",
                to="order.supplier",
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="BuyingItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField()),
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, default=0, max_digits=10
                    ),
                ),
                (
                    "currency_rate",
                    models.DecimalField(
                        blank=True, decimal_places=2, default=0, max_digits=10
                    ),
                ),
                ("discount_rate", models.PositiveIntegerField(blank=True, default=0)),
                (
                    "buying_invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="buying_items",
                        to="order.buyinginvoice",
                    ),
                ),
                (
                    "inventory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="order.inventory",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="order.product"
                    ),
                ),
            ],
        ),
    ]