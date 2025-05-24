from django import forms
from .models import User

class SignUpForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2','placeholder':'Enter your password'}),label='')
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2','placeholder':'Retype your password'}),label='')
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        labels = {'email':'','first_name':'','last_name':''}
        error_messages = {
            'email':{
                'invalid': "Email invalid",
                'required': "Please enter your email"
            },
            'first_name':{
                'required':'Please enter your first name.',
                'min_length':'First name has to be at least 2 letters',
                'max_length':'First name cannot exceed 30 characterss'
                },
            'last_name':{
                'required':'Please enter your last name.',
                'min_length':'Last name has to be at least 2 letters',
                'max_length':'Last name cannot exceed 30 characterss'
                },
            'password':{
                'min_length':'Password must be at least 4 characters.'
                }
            }
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control my-2','placeholder':'Enter your email'}),
            'first_name':forms.TextInput(attrs={'class':'form-control my-2','placeholder':'Enter your first name','required':'True'}),
            'last_name':forms.TextInput(attrs={'class':'form-control my-2','placeholder':'Enter your last name'}),
            'password':forms.PasswordInput()
        }
    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match."
            )
        elif len(password) < 6:
            raise forms.ValidationError(
                "Password must be at least 6 characters."
            )
        

class LogInForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id':'id-login-email', 'class':'form-control my-2', 'placeholder':'Please insert your email'}),error_messages={'required':"Please, insert your email", 'invalid':'Email is invalid.'},label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'id-login-password', 'class':'form-control my-2', 'placeholder':'Please insert your password'}),label='')