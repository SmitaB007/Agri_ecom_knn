# Generated by Django 5.1.5 on 2025-01-26 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_delete_userpurchase'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=5, max_digits=4),
        ),
        migrations.AddField(
            model_name='product',
            name='delivery_charges',
            field=models.DecimalField(decimal_places=2, default=40, max_digits=4),
        ),
    ]
