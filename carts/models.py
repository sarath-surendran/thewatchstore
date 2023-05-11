from django.db import models
from products.models import Product,Variations
from user_home.models import CustomUser

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)
    coupon_added = models.BooleanField(default=False, blank=True)
    coupon_discount = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)

    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    user =  models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    variations = models.ManyToManyField(Variations, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.name
    def product_total(self):
        return self.product.selling_price * self.quantity
    

class Coupon(models.Model):
    code = models.CharField(max_length=20,blank=False)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code