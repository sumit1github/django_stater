from django import forms
from django.contrib.auth.hashers import make_password

from . import models

class LoginForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields =["email","password",]
    email = forms.EmailField(max_length=255, label='Email')
    email.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Email',"required":"required"})
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))



class RegisterForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields =["email","password","confirm_password","contact",]

    email = forms.EmailField(max_length=255, label='Email')
    email.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Email',"required":"required"})
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    contact = forms.IntegerField(label='Contact Number')
    contact.widget.attrs.update({'class': 'form-control','type':'number', "required":"required"})

    invitation_code = forms.CharField(label='Invitation code', max_length=255, required= False)
    invitation_code.widget.attrs.update({'class': 'form-control','type':'text',})
    

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError("Password Mismatched")
        else:
            hashed_password = make_password(cleaned_data['password'])
            cleaned_data['password'] = hashed_password

        if len(str(cleaned_data['contact']))!= 10:
            raise forms.ValidationError("Enter a ten digit contact number....")
        
        return cleaned_data