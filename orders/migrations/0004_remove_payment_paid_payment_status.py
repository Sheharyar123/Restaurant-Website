# Generated by Django 4.1.5 on 2023-03-03 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='paid',
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]