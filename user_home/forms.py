from django import forms
from .models import CustomUser,UserAddress

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'input--style-4'}))
    referal  = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'input--style-4'}))

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','phone','password','confirm_password','referal',]
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'input--style-4'}),
            'last_name': forms.TextInput(attrs={'class':'input--style-4'}),
            'email': forms.TextInput(attrs={'class':'input--style-4'}),
            'phone': forms.TextInput(attrs={'class':'input--style-4'}),
            'password': forms.TextInput(attrs={'class':'input--style-4'}),
        }

class AddressForm(forms.ModelForm):
    next = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = UserAddress
        fields = ['first_name','last_name','email','phone','address_line_1','address_line_2','country','state','city','pincode']
        widgets = {
            'first_name': forms.TextInput(attrs={"class":'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'address_line_1': forms.TextInput(attrs={'class':'form-control'}),
            'address_line_2': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'state': forms.TextInput(attrs={'class':'form-control'}),
            'country': forms.TextInput(attrs={'class':'form-control'}),
            'pincode': forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        next_param = self.initial.get('next')
        if next_param:
            self.fields['next'].initial = next_param

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','phone']
        widgets = {
            'first_name': forms.TextInput(attrs={"class":'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
        }