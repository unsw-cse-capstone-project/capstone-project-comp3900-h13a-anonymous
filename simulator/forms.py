from django import forms
from django.contrib.auth.models import User

from django.contrib.auth import password_validation

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UserForm(forms.ModelForm):
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    password = forms.CharField(label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),)
    # number = forms.IntegerField()
    confirm_password=forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),)
    
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('Sign up', 'Sign up', css_class='btn-primary'))
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "The passwords do not match")

        cleaned_data.pop("confirm_password")
        
        return cleaned_data
