from django import forms
from .models import Item
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ItemForm(forms.ModelForm):
    class Meta:
        model=Item
        fields=('name','price','file','category','description')
        widgets={
            'name':forms.TextInput(attrs={
              'class':''}),
            'price':forms.NumberInput(attrs={
              'class':''}),
            'file':forms.FileInput(attrs={
              'class':''}),
            'category':forms.Select(attrs={
              'class':''}),
            'description':forms.TextInput(attrs={
              'class':''}),
        }

class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username','email','password1','password2')
    username=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'your username',
        'class':'',
        }))
    email=forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder':'your email',
        'class':'',
        'id':'email-signup'
        }))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'enter password',
        'class':'',
        }))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'confirm password',
        'class':'',
        }))
    check=forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'id':'chk',
        'onclick':'func()',
        'class':'',
        }))