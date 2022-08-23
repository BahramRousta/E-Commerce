# Generated by Django 4.0.6 on 2022-08-23 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_alter_cartitem_price_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='coupon',
        ),
        migrations.AddField(
            model_name='coupon',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coupon', to='cart.cart'),
        ),
    ]