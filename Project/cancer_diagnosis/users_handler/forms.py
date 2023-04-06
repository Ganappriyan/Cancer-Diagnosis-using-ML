from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    phone_number = forms.CharField(max_length=20, help_text='Required')
    
    # Custom validation for phone_number
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit():
            raise ValidationError(_('Invalid phone number - must contain only digits'), code='invalid')
        return phone_number

    # Custom validation for password mismatch
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(_('Passwords do not match'), code='password_mismatch')
        
        return cleaned_data
    
    # Custom validation for email
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError(_('This email is already in use'), code='email_in_use')
        return email
    
    # Custom validation for username
    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.isalnum() and '-' not in username:
            raise ValidationError(_('Username can only contain letters, numbers, and -'), code='invalid')
        return username

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'phone_number')


User = get_user_model()
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
        
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username or not password:
            raise ValidationError(
                _("Please enter both username and password"),
                code='invalid_login',
                params={'username': self.username_field.verbose_name},
            )

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise forms.ValidationError(
                    _("Invalid password"),
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
        except User.DoesNotExist:
            raise forms.ValidationError(
                _("Invalid username"),
                code='invalid_login',
                params={'username': self.username_field.verbose_name},
            )

        return cleaned_data

