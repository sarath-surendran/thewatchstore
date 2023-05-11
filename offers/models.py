from django.db import models
from products.models import Product
from categories.models import Category

# Create your models here.
class ProductOffers(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=50)
    discount = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_applied = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class CategoryOffers(models.Model):
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=50)
    discount = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_applied = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    