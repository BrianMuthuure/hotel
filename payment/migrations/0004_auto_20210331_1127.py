# Generated by Django 3.1.7 on 2021-03-31 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20210331_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='pay_amount',
            field=models.PositiveBigIntegerField(default=0, editable=False),
        ),
    ]
