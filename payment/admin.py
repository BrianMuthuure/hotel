from django.contrib import admin

# Register your models here.
from payment.models import CheckIn, CheckOut

admin.site.register(CheckIn)
admin.site.register(CheckOut)