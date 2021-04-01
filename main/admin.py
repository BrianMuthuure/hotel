from django.contrib import admin

# Register your models here.
from main.models import RoomType, Facility, Room, RoomImage, Reservation

admin.site.register(RoomType)
admin.site.register(Facility)
admin.site.register(Reservation)


class RoomImageAdmin(admin.StackedInline):
    model = RoomImage


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomImageAdmin]

    class Meta:
        model = Room


@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    pass