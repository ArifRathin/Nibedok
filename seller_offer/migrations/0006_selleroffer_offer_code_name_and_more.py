# Generated by Django 5.1.7 on 2025-04-27 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller_offer', '0005_selleroffer_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='selleroffer',
            name='offer_code_name',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='selleroffer',
            name='post_code_name',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
    ]
