# Generated by Django 4.1.5 on 2023-03-06 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_restaurants'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-updated_on', '-created_on']},
        ),
    ]
