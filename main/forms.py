from django import forms
from django.utils.translation import ugettext_lazy as _
from main.models import Room, RoomImage


class RoomCreationForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_type', 'no_beds', 'image']


class RoomUpdateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_type', 'no_beds', 'image']


class ImageCreateForm(forms.ModelForm):

    class Meta:
        model = RoomImage
        fields = '__all__'

    def clean_room(self):
        images = self.cleaned_data['room']
        if not images:
            raise forms.ValidationError('You have to add an image')
        return images


class ReservationForm(forms.Form):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    first_name = forms.CharField(
        label=_("First Name"),
        max_length=50,
        widget=forms.TextInput(
        )
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=50,
        widget=forms.TextInput(
        )
    )
    phone_no = forms.CharField(
        label=_('Phone No'),
        max_length=15,
        widget=forms.TextInput(
        )
    )

    gender = forms.ChoiceField(
        label=_('Gender'),
        choices=GENDER
    )

    nationality = forms.CharField(
        label=_('Nationality'),
        max_length=15,
        widget=forms.TextInput(
        )
    )
    email = forms.EmailField(
        label=_("Email"),
        max_length=50,
        required=False,
        widget=forms.EmailInput(
        )
    )
    no_children = forms.IntegerField(
        widget=forms.NumberInput(
        )
    )
    no_adults = forms.IntegerField(
        widget=forms.NumberInput(
        )
    )

    date = forms.DateField(
        widget=forms.DateInput(
        )
    )
    rooms = forms.ModelMultipleChoiceField(
        queryset=Room.objects.filter(reservation__isnull=True),
        widget=forms.SelectMultiple(

        ),
    )




