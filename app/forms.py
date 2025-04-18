from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from  app.models import Customer

class Registration(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1=forms.CharField( label='password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='confirmpassword',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model=User
        fields=['username','email','password1','password2']


class Customerform(forms.ModelForm):
    class Meta:

        model=Customer
        fields=['name','locality','city','mobile','state','zipcode']   
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
             'city':forms.TextInput(attrs={'class':'form-control'}),
              'mobile':forms.NumberInput(attrs={'class':'form-control'}),
               'state':forms.Select(attrs={'class':'form-control'}),
                'zipcode':forms.NumberInput(attrs={'class':'form-control'})
        }     