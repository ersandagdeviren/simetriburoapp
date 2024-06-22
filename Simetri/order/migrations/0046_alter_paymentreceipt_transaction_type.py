# Generated by Django 4.2.5 on 2024-06-22 16:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0045_remove_debit_expense_item_delete_credit_delete_debit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymentreceipt",
            name="transaction_type",
            field=models.CharField(
                choices=[("Tahsilat", "Tahsilat"), ("Tediye", "Tediye")],
                default="Tahsilat",
                max_length=10,
            ),
        ),
    ]
