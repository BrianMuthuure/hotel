from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

# Create your models here.
from django.utils import timezone

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

ROLES = (
    ('Receptionist', 'Receptionist'),
    ('Other', 'Other')
)


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    class Meta:
        db_table = 'users_table'


class Staff(models.Model):
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    staff_id = models.AutoField(primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    role = models.CharField(choices=ROLES, max_length=20, default='Other')
    date_of_birth = models.DateField(default=timezone.now)
    nationality = models.CharField(max_length=20,  null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=10)
    age = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'staff'

    def __str__(self):
        return f'{self.staff_id}'

    def save(self, **kwargs):
        if not self.staff_id:
            max = Staff.objects.aggregate(id_max=models.Max('staff_id'))['id_max']
            if max is not None:
                max += 1
            else:
                max = 100
            self.staff_id = "{:08d}".format(max)

        today = datetime.date.today()
        self.age = today.year - self.date_of_birth.year

        super(Staff, self).save(**kwargs)


    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Guest(models.Model):
    guest_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_no = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(null=True)
    gender = models.CharField(max_length=10)
    nationality = models.CharField(max_length=100)
    dob = models.DateField(default=timezone.now)
    age = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'guest'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, **kwargs):
        today = datetime.date.today()
        self.age = today.year - self.dob.year

        super(Guest, self).save(**kwargs)

