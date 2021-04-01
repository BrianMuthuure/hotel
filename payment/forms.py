from django import forms

from payment.models import CheckIn, CheckOut


class CheckInRequestForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = ['reservation']
        widgets = {'reservation': forms.HiddenInput()}


class CheckoutRequestForm(forms.ModelForm):
    class Meta:
        model = CheckOut
        fields = ['check_in']
        widgets = {'check_in': forms.HiddenInput()}
