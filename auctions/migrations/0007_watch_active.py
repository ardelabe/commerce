# Generated by Django 3.1.2 on 2020-12-06 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20201204_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='watch',
            name='active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
