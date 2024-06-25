# Generated by Django 4.2.5 on 2024-06-25 08:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("order", "0047_remove_order_user_customer_user_alter_order_customer_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customer",
            name="user",
        ),
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_orders",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
