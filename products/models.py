from django.db import models
from categories.models import Category

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=True)
    mrp = models.IntegerField(blank=False)
    selling_price = models.FloatField(blank=False)
    brand = models.CharField(max_length=200)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    is_avaliable = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, related_name='products')
    pro_offer = models.BooleanField(default=False)
    cat_offer = models.BooleanField(default=False)

    def __str__(self):
        return self.name

variation_choice = (
    ('Leather','Leather'),
    ('Rubber','Rubber'),
    ('Metal','Metal'),
)


class Variations(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_value = models.CharField(max_length=100, choices=variation_choice)

    def __str__(self):
        return self.variation_value