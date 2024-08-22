from django import forms
from .models import Account, UserProfile
from django.forms import ValidationError

class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password'

    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'

    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs["placeholder"] = 'First Name'
        self.fields['last_name'].widget.attrs["placeholder"] = 'Last Name'
        self.fields['email'].widget.attrs["placeholder"] = 'Email'
        self.fields['password'].widget.attrs["placeholder"] = 'Enter Password'
        self.fields['confirm_password'].widget.attrs["placeholder"] = 'Repeat Password'
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError('Password does not match')


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = 'form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages ={'invalid': "Image files Only"}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ("address_line_1", "house_number", "address_line_2", "city", "zipcode", "country", "profile_picture")

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = 'form-control'


