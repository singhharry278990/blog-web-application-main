from django import forms
from froala_editor.widgets import FroalaEditor
from .models import *
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ['title', 'content']


class ResetModel(forms.ModelForm):
    email = forms.EmailField()
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    mobile_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    mobile = forms.CharField(validators=[mobile_regex], max_length=17)


    class Meta:
        model = User
        fields = []
             
    def clean(self):
        email = self.cleaned_data['email']
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        mobile = cleaned_data.get('mobile')
        print("email", email,current_password, new_password, confirm_password, mobile)

        user = User.objects.filter(email=email).first()
        if not user:
            raise forms.ValidationError('There is no user with this email address.')
        
        if new_password != confirm_password:
            raise forms.ValidationError('Both passwords are not match.')
        
        check_pass = user and user.check_password(current_password)
        if not check_pass:
            raise forms.ValidationError('Current password is incorrect.')

        return cleaned_data

# class OtpForm(forms.ModelForm):
#     otp = forms.cleaned_data('otp')

#     def clean(self):
#         cleaned_data = super().clean()
#         otp = forms.cleaned_data('otp')
    
