from django import forms
from .models import Coupon

class CouponAddForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code','discount','is_active']