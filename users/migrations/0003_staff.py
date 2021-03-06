# Generated by Django 3.1.7 on 2021-03-25 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210325_0907'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('date_of_birth', models.DateField()),
                ('nationality', models.CharField(max_length=20)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
            ],
            options={
                'db_table': 'staff',
            },
        ),
    ]
