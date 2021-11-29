from builtins import max

from django import forms
from django.conf import settings

from django.contrib.auth import authenticate
# from django.contrib.admin.forms import AdminAuthenticationForm
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
ERROR_MESSAGE = ("Please enter a correct email and password. ")
ERROR_MESSAGE_RESTRICTED = ("You do not have permission to access the admin.")
ERROR_MESSAGE_INACTIVE = ("This account is inactive.")
from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name', max_length=20)
    last_name = forms.CharField(label='Last Name', max_length=20)
    location = forms.CharField(label='Location', max_length=20)
    profile_photo = forms.ImageField(label='Profile Image' )
    phone_number = forms.CharField(label='Phone Number')
    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name', 'location', 'phone_number', 'profile_photo',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


# class LoginForm(AuthenticationForm):
#     username = forms.CharField(label='Email / Username')

class AuthenticationForm(forms.Form):
    email = forms.EmailField(label="E-mail address", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None

    def authenticate(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Please enter a correct e-mail address and password. Note that both fields are case-sensitive.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")

        return self.user_cache

    def clean(self):
        self.authenticate()
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(
                "Your Web browser doesn't appear to have cookies enabled. "
                "Cookies are required for logging in.")

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'active',)

    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):

        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

"""
class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        return self.initial["password"]
"""

class EmailAdminAuthenticationForm(forms.ModelForm):
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        super(EmailAdminAuthenticationForm, self).__init__(*args, **kwargs)
        # del self.fields['username']
        self.request = request
        self.user_cache = None

    def authenticate(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Please enter a correct e-mail address and password. Note that both fields are case-sensitive.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")

        return self.user_cache

    def clean(self):
        self.authenticate()
        self.check_for_test_cookie()
        return self.cleaned_data