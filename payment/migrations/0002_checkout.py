# Generated by Django 3.1.7 on 2021-03-30 20:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stay_duration', models.DurationField(editable=False, null=True)),
                ('total_amount', models.PositiveSmallIntegerField(default=0, editable=False)),
                ('pay_amount', models.PositiveSmallIntegerField(default=0, editable=False)),
                ('check_out_date_time', models.DateTimeField(editable=False, null=True)),
                ('check_in', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='payment.checkin')),
                ('user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]