# Generated by Django 3.0.8 on 2020-08-07 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auction_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='image',
            field=models.TextField(default='https://drive.google.com/file/d/16luB3wU5GxvnXfJKHbs4YDUU_n-B-UcJ/view?usp=sharing'),
        ),
    ]
