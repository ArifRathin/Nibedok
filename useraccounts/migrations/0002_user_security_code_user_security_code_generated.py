# Generated by Django 5.1.7 on 2025-03-10 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='security_code',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='security_code_generated',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
    ]
