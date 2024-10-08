# Generated by Django 5.0.7 on 2024-07-22 14:42

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sb', '0004_remove_category_slug_remove_subcategory_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='max_allowed_spend',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='spend',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 7, 22, 14, 41, 25, 133363, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='spend',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='spends', to='sb.subcategory'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='sb.category'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='max_allowed_spend',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
