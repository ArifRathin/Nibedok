# Generated by Django 5.1.7 on 2025-03-12 00:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer_post', '0003_buyersamplephoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyersamplephoto',
            name='post',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='buyer_post.buyerpost'),
        ),
    ]
