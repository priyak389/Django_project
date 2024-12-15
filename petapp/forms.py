from django import forms

 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Customer_details

class RegisterForm(UserCreationForm):
 
    class Meta:
        model = User
        fields = ['username' , 'first_name' , 'last_name' , 'email' , 'password1' , 'password2']

        labels = {
            'username':'Enter Username',
            'first_name' :'Enter First Name',
            'last_name' : 'Enter Last Name',
            'email' :'Enter Email-ID',
        }

        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control'}),
        }
        def clean_password2(self):
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")

        # Custom password validation
            if password1 and password2 and password1 != password2:
                raise ValidationError("Passwords do not match.")

            if len(password1) < 8:
                raise ValidationError("Password must be at least 8 characters long.")

            if not any(char.isdigit() for char in password1):
                raise ValidationError("Password must contain at least one digit.")

            return password2

class UserAuthentication(AuthenticationForm):     
    username = forms.CharField(label="Enter Username" , widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(
        label=("Enter Password"),
        
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password" , 'class':'form-control'}),
    )

    class Meta:
        model = User
        fields = ['username' ]
        labels = {
            'password':'Enter Password'
        }



from .models import Pet

class petform(forms.ModelForm):
    class Meta:
        model=Pet
        fields=['petname','age','breed','price','description','image']
        
        labels = {
            'petname':'Enter petname',
            'age' :'Enter age',
            'breed' : 'Enter breed',
            'price' :'Enter price',
            'description':'Enter description',
            'image':'enter description'
        }

        widgets = {
            'petname' : forms.TextInput(attrs={'class':'form-control'}),
            'age':forms.NumberInput(attrs={'class':'form-control'}),
            'breed':forms.Select(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control'}),
            
        }
        













class UserauthenticationForm(AuthenticationForm):
    username=forms.CharField(label='Enter username',widget=forms.TextInput(attrs={'class':'form-control'})),
    password=forms.CharField(label='Enter Password',widget=forms.PasswordInput(attrs={'class':'form-control'})),


    class Meta:
        model=User
        fields=['username']








from django import forms

class petform1(forms.Form):
    petname=forms.CharField(max_length=100)
    pet_price=forms.FloatField()
    pet_cat=forms.CharField(max_length=100)
    pet_desc=forms.CharField(max_length=100)
 


class Customer_detailsform(forms.ModelForm):
    class Meta:
        model=Customer_details
        fields=["name","address","city","state","pincode"]

 
    