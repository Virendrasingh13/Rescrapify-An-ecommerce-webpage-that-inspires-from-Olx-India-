# Generated by Django 5.0.2 on 2024-02-28 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_rename_category_choice_category_category_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_type',
            field=models.CharField(choices=[('Scrapify', 'Scrapify'), ('Creative', 'Creative')], max_length=10),
        ),
    ]
