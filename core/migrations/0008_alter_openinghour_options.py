# Generated by Django 4.1.5 on 2023-02-22 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_openinghour_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='openinghour',
            options={'ordering': ['day', '-from_hour']},
        ),
    ]
