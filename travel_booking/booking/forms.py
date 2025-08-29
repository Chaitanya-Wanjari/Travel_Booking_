
from django import forms
from django.contrib.auth.models import User
from .models import Booking

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password']

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('confirm_password'):
            raise forms.ValidationError('Passwords do not match')
        return cleaned

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_seats']
        widgets = {'number_of_seats': forms.NumberInput(attrs={'min':1})}

class FilterForm(forms.Form):
    TYPE_CHOICES = [('', 'Any'), ('Flight','Flight'), ('Train','Train'), ('Bus','Bus')]
    type = forms.ChoiceField(choices=TYPE_CHOICES, required=False)
    source = forms.CharField(required=False)
    destination = forms.CharField(required=False)
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type':'date'}))
