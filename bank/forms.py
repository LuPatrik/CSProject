from django import forms
from .models import User
from django.core.exceptions import ValidationError


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="For security reasons it is recommended for the password to be at least 10 characters long."
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        #passwords are not checked for their security
        
        has_letter = any(char.isalpha() for char in password)
        has_number = any(char.isdigit() for char in password)
        if not has_letter:
            raise ValidationError("Password must contain at least one letter!")
        if not has_number:
            raise ValidationError("Password must contain at least one number!")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long!")
        
        return password

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)