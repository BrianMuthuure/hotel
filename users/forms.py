from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User, Staff


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in  ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class StaffCreationForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields =['date_of_birth', 'nationality', 'gender', 'role', 'image']
