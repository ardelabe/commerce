# Generated by Django 3.1.2 on 2020-12-11 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(choices=[('1', 'Appliances'), ('2', 'Apps & Games'), ('3', 'Arts, Crafts, & Sewing'), ('4', 'Automotive Parts & Accessories'), ('5', 'Baby'), ('6', 'Beauty & Personal Care'), ('7', 'Books'), ('8', 'CDs & Vinyl'), ('9', 'Cell Phones & Accessories'), ('10', 'Clothing, Shoes and Jewelry'), ('11', 'Collectibles & Fine Art'), ('12', 'Computers'), ('13', 'Electronics'), ('14', 'Garden & Outdoor'), ('15', 'Grocery & Gourmet Food'), ('16', 'Handmade'), ('17', 'Health, Household & Baby Care'), ('18', 'Home & Kitchen'), ('19', 'Industrial & Scientific'), ('20', 'Luggage & Travel Gear'), ('21', 'Movies & TV'), ('22', 'Musical Instruments'), ('23', 'Office Products'), ('24', 'Pet Supplies'), ('25', 'Premium Beauty'), ('26', 'Sports & Outdoors'), ('27', 'Tools & Home Improvement'), ('28', 'Toys & Games'), ('29', 'Video Games'), ('30', 'Other categories')], default=30, max_length=64),
        ),
    ]
