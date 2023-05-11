from django import forms
from .models import Product,Variations,variation_choice

from categories.models import Category

class ProductForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget = forms.CheckboxSelectMultiple)

    class Meta:
        model = Product
        fields = ['name','mrp','selling_price','brand','quantity','image','categories','is_avaliable',]


class VariationForm(forms.ModelForm):
    variation_value = forms.MultipleChoiceField(choices=variation_choice, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Variations
        fields = ('variation_value',)

    