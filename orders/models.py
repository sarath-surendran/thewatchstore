from django.db import models
from user_home.models import CustomUser,UserAddress
from products.models import Product, Variations

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id





class Orders(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Shipped', 'Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
    )
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number = models.CharField(max_length=20)
    address = models.ForeignKey(UserAddress,on_delete=models.SET_NULL,null=True)
    order_total = models.FloatField()
    status = models.CharField(max_length=10,choices=STATUS,default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name


class OrderProduct(models.Model):
    order = models.ForeignKey(Orders,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    # variaton = models.ManyToManyField(Variations,blank=True)
    variation = models.ForeignKey(Variations,on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

   