import os
import random
import string

from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone

from main.utils import random_string_generator
from users.models import Guest


class RoomType(models.Model):
    ROOMTYPES = (
        ('Double Suit', 'Double Suit'),
        ('Luxury Suit', 'Luxury Suit'),
        ('Exclusive Suit', 'Exclusive Suit'),
        ('EXECUTIVE FLOOR', 'EXECUTIVE FLOOR'),
        ('SUPERIOR ROOM', 'SUPERIOR ROOM'),
        ('BUSINESS SUITE', 'BUSINESS SUITE'),
        ('STATE SUITE', 'STATE SUITE')
    )
    facility = models.ManyToManyField('Facility', blank=True)
    name = models.CharField(choices=ROOMTYPES, max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Room Types'
        db_table = 'room_types'

    def display_facility(self):
        """
        This function should be defined since facility is many-to-many relationship
        It cannot be displayed directly on the admin panel for list_display
        """
        return ', '.join([facility.name for facility in self.facility.all()])

    display_facility.short_description = 'Facilities'

    def __str__(self):
        return f'{self.name}'


class Facility(models.Model):
    FACILITIES = (
        ('Breakfast', 'Breakfast'), ('Room Service', 'Room Service'), ('WI-FI', 'WI-FI'),
        ('Parking', 'Parking'), ('Business Center', 'Business Center'), ('Laundry', 'Laundry'),
        ('Swimming Pool', 'Swimming Pool'), ('Poolside Bar', 'PoolsideBar'),
    )
    name = models.CharField(choices=FACILITIES, max_length=40)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'facility'
        verbose_name_plural = 'Facilities'

    def __str__(self):
        return self.name


class Room(models.Model):
    room_id = models.CharField(primary_key=True, blank=True, max_length=10, editable=False)
    image = models.ImageField(blank=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    reservation = models.ForeignKey('Reservation', null=True, blank=True, on_delete=models.SET_NULL)
    no_beds = models.PositiveIntegerField(default=1)
    available = models.BooleanField(default=True)

    class Meta:
        db_table = 'room'

    def save(self, *args, **kwargs):  # Overriding default behaviour of save
        if self.reservation:  # If it is reserved, than it should not be available
            self.available = 0
        else:
            self.available = 1

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("room_detail", kwargs={"pk": self.pk})

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return f'{self.room_id}'


def room_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.room_id:
        instance.room_id = f'B-' + ''.join(random.choices(string.digits, k=2))


pre_save.connect(room_pre_save_receiver, sender=Room)


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='room_pictures', default='default.jpg', null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Images'
        db_table = 'image'

    def __str__(self):
        return self.room.room_id


class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    no_children = models.PositiveIntegerField(default=0)
    no_adults = models.PositiveIntegerField(default=0)
    expected_arrival_date_time = models.DateField(default=timezone.now)
    expected_departure_date_time = models.DateField(default=timezone.now)

    def get_absolute_url(self):
        return reverse("reservation_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return '({0}) {1}'.format(self.reservation_id, self.guest)

