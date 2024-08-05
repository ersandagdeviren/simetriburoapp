# Generated by Django 5.0 on 2024-08-02 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0066_remove_buyinginvoice_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyingitem',
            name='finalized_currency_rate',
        ),
        migrations.AddField(
            model_name='buyinginvoice',
            name='status',
            field=models.CharField(default='Pending', max_length=50),
        ),
    ]
