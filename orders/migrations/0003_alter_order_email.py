# Generated by Django 4.1.5 on 2023-03-03 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=255),
        ),
    ]
