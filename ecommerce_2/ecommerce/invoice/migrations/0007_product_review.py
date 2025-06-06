# Generated by Django 5.1.5 on 2025-01-18 10:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0006_wishlist'),
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='product_review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('review', models.TextField(max_length=250)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
