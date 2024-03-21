from django.db import models

from accounts.models import CustomUser
from helpers import generate_unique_hash
from django.utils.text import slugify
# Create your models here.

CATEGORY_TYPES = [
    ("scrapify","Scrapify"),
    ("creative","Creative"),
]

class Category(models.Model):
    category_name = models.CharField(max_length=50)
    category_type = models.CharField(choices = CATEGORY_TYPES, max_length = 10)
    slug = models.SlugField(unique=True, null=True, blank=True)
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_type) +"-"+ slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.category_name
    
class Item(models.Model):
    item_name = models.CharField(max_length=50)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="item")
    price = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    description = models.TextField()
    slug = models.SlugField(unique=True, null=True, blank=True)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sold = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=False,null=True, blank=True)
    # quantity = models.IntegerField(null=True,blank=True,default=None)
        
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.item_name)+"-"+generate_unique_hash()
        super(Item, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.item_name
    
    
class Item_image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE,related_name="item_image")
    image = models.ImageField(upload_to="images/products/", null=True, blank=True)