from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User, Staff


class UserRegisterForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs=
                                                      {'class': 'form-control', 'type': 'text'}),
                               required=True,
                               max_length=20)
    first_name = forms.CharField(widget=forms.TextInput(attrs=
                                                        {'class': 'form-control', 'input type': 'text'}),
                                 max_length=20, required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs=
                                                       {'class': 'form-control', 'input type': 'text'}),
                                max_length=20, required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs=
                                                     {'class': 'form-control', 'type': 'email'}),
                             required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=
                                                           {'class': 'form-control', 'type': 'password', 'id': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=
                                                           {'class': 'form-control', 'type': 'password', 'id': 'password2'}))

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

        widgets = {
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control', 'placeholder': 'position'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'select date', 'type': 'date'})
        }