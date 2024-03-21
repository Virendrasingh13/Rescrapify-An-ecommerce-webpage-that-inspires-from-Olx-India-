# Generated by Django 5.0.2 on 2024-03-18 13:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='state',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ordered', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
