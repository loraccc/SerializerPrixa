from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.text import slugify

# Create your models here.


class item(models.Model):
    name=models.CharField(max_length=200)
    desc=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generates the slug based on the 'name' field
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self,*args):
        return self.name
    

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other fields as needed

    def __str__(self):
        return self.user.username
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    owner=models.ForeignKey(Person,on_delete=models.CASCADE,default=1)
 
    def __str__(self):
        return self.name
 
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'