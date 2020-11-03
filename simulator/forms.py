from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from simulator.models import WatchListAlert
from django.db import models

from django.contrib.auth import password_validation

from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import StrictButton

class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=3, max_length=15)
    # first_name = forms.CharField(label='Enter Name', min_length=3, max_length=15)
    email = forms.EmailField(label='Enter Email')
    password1 = forms.CharField(label='Enter Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('Sign up', 'Sign up', css_class='btn-primary'))
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class BuyForm(forms.Form):
    amount = forms.IntegerField(label='Enter Amount Of Shares To Buy')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-4'
    helper.field_class = 'col-lg-8'
    helper.add_input(Submit('Confirm', 'Confirm', css_class='btn-primary'))

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise ValidationError("Value must be greater than 0")
        return amount

    def save(self, commit=True):
        return self.cleaned_data['amount']

class SellForm(forms.Form):
    amount = forms.IntegerField(label='Enter Amount Of Shares To Sell')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-4'
    helper.field_class = 'col-lg-8'
    helper.add_input(Submit('Confirm', 'Confirm', css_class='btn-primary'))

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise ValidationError("Value must be greater than 0")
        return amount

    def save(self, commit=True):
        return self.cleaned_data['amount']

class SetWatchPriceForm(forms.Form):
    
    amount = forms.DecimalField(label='Enter Watch Price to Trigger At')
    action_choices = (
        ('', 'Choose...'),
        ('buy', 'Buy'),
        ('sell', 'Sell')
    )
    action = forms.ChoiceField(choices=action_choices)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-4'
    helper.field_class = 'col-lg-8'
    helper.add_input(Submit('Confirm', 'Confirm', css_class='btn-primary'))

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise ValidationError("Value must be greater than 0")
        return amount

    def save(self, commit=True):
        return self.cleaned_data['amount'], self.cleaned_data['action']

        
    

    
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('url', 'location', 'company')

# class UserForm(forms.ModelForm):
#     email = forms.EmailField(
#         label=("Email"),
#         max_length=254,
#         widget=forms.EmailInput(attrs={'autocomplete': 'email'})
#     )
#     password = forms.CharField(label=("Password"),
#         strip=False,
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#         help_text=password_validation.password_validators_help_text_html(),)
#     # number = forms.IntegerField()
#     confirm_password=forms.CharField(label=("Password confirmation"),
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#         strip=False,
#         help_text=("Enter the same password as before, for verification."),)
    
#     helper = FormHelper()
#     helper.form_method = 'POST'
#     helper.add_input(Submit('Sign up', 'Sign up', css_class='btn-primary'))
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password')

#     def clean(self):
#         # cleaned_data = super(UserForm, self).clean()
#         print (self.cleaned_data)
#         password = self.cleaned_data.get("password")
#         confirm_password = self.cleaned_data.get("confirm_password")

#         if password and confirm_password and password != confirm_password:
#             self.add_error('confirm_password', "The passwords do not match")

#         cleaned_data.pop("confirm_password")
        
#         return cleaned_data