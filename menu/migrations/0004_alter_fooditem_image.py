# Generated by Django 4.1.5 on 2023-02-13 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_fooditem_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='image',
            field=models.ImageField(default='.static/extra-images/default-food.png', upload_to='food_items'),
        ),
    ]
