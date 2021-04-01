# Generated by Django 3.1.7 on 2021-03-25 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Breakfast', 'Breakfast'), ('Room Service', 'Room Service'), ('WI-FI', 'WI-FI'), ('Parking', 'Parking'), ('Business Center', 'Business Center'), ('Laundry', 'Laundry'), ('Swimming Pool', 'Swimming Pool'), ('Poolside Bar', 'PoolsideBar')], max_length=40)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name_plural': 'Facilities',
                'db_table': 'Facility',
            },
        ),
        migrations.AddField(
            model_name='roomtype',
            name='facility',
            field=models.ManyToManyField(blank=True, to='main.Facility'),
        ),
    ]