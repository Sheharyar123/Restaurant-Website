# Generated by Django 4.1.5 on 2023-02-13 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_alter_fooditem_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='image',
            field=models.ImageField(default='food_items/default-food.png', upload_to='food_items'),
        ),
    ]
