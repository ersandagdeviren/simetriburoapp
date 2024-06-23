# Generated by Django 4.2.5 on 2024-06-18 18:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0036_bankaccount_cashaccount_employee_salarypayment_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="expense",
            name="bank_account",
        ),
        migrations.RemoveField(
            model_name="expense",
            name="cash_account",
        ),
        migrations.RemoveField(
            model_name="expense",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="paymenttransaction",
            name="bank_account",
        ),
        migrations.RemoveField(
            model_name="paymenttransaction",
            name="cash_account",
        ),
        migrations.RemoveField(
            model_name="posdevice",
            name="bank_account",
        ),
        migrations.RemoveField(
            model_name="salarypayment",
            name="bank_account",
        ),
        migrations.RemoveField(
            model_name="salarypayment",
            name="cash_account",
        ),
        migrations.RemoveField(
            model_name="salarypayment",
            name="employee",
        ),
        migrations.DeleteModel(
            name="BankAccount",
        ),
        migrations.DeleteModel(
            name="CashAccount",
        ),
        migrations.DeleteModel(
            name="Employee",
        ),
        migrations.DeleteModel(
            name="Expense",
        ),
        migrations.DeleteModel(
            name="PaymentTransaction",
        ),
        migrations.DeleteModel(
            name="POSDevice",
        ),
        migrations.DeleteModel(
            name="SalaryPayment",
        ),
    ]