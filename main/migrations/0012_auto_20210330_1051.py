# Generated by Django 3.1.7 on 2021-03-30 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20210326_1517'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='roomimage',
            options={'verbose_name_plural': 'Images'},
        ),
        migrations.AlterModelTable(
            name='roomimage',
            table='image',
        ),
    ]