from django.db import models
from category.models import Category

# Create your models here.
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100, unique= True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=150, blank=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='photos/products')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product_name