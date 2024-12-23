from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from .models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError('პაროლები არ ემთხვევა')

        return cleaned_data

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')


        if not phone_number.startswith('+'):
            phone_number = '+995' + phone_number.strip()

        return phone_number


class VerificationForm(forms.Form):
    confirmation_code = forms.CharField(max_length=6, label='კოდი:')


