from django.db import models
from products.models import Product,Variations
from user_home.models import CustomUser


# Create your models here.
class Wishlist(models.Model):
    user =  models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    variations = models.ManyToManyField(Variations, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    # quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.name
    