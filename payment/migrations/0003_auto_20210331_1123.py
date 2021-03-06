# Generated by Django 3.1.7 on 2021-03-31 08:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_checkout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='check_in_date_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='pay_amount',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=12),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='stay_duration',
            field=models.DurationField(null=True),
        ),
    ]
