from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':"enter the password",
        'class':'form-control',
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':"enter confirm password",
        'class':'form-control',
    }))

    class Meta:
        model = Account
        fields = ('first_name','last_name','email','phone_number','is_active')
    
    def __init__(self,*args, **kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = "enter first tname"
        self.fields['last_name'].widget.attrs['placeholder'] = "enter last name"
        self.fields['email'].widget.attrs['placeholder'] = "enter email address"
        self.fields['phone_number'].widget.attrs['placeholder'] = "enter phone number"
        
        for feild in self.fields:
            self.fields[feild].widget.attrs['class'] = 'form-control'  

    def clean(self):
        cleaned_data=super(RegistrationForm,self).clean()
        password=cleaned_data.get('password')              
        confirm_password=cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("password does not mathced........!")
                      