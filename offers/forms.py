from django import forms
from .models import ProductOffers,CategoryOffers

class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffers
        fields = ['product','name','discount']
        widgets = {
            # 'product': forms.Select(attrs={'class': 'form-control'}),
            'discount': forms.TextInput(attrs={'placeholder': "(in %) "}),
        }


class CategoryOfferForm(forms.ModelForm):
    class Meta:
        model = CategoryOffers
        fields = ['category','name','discount']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            
        }
