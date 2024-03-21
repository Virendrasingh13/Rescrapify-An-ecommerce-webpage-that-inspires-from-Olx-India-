
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from helpers import generate_unique_hash
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth import get_user_model


# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, verbose_name='username',null=True, blank=True)
    email = models.EmailField(unique=True,max_length = 255)
    slug = models.SlugField(unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    user_image = models.ImageField(upload_to = 'images/user/',null=True, blank=True)
    phone_no = models.IntegerField(validators=[MaxValueValidator(999999999999),MinValueValidator(000000000000)],null=True, blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=100,null=True, blank=True,default=None)
    city = models.CharField(max_length=150,null=True, blank=True,default=None)
    temp_email = models.EmailField(null=True,blank=True,max_length = 255,default= None)
    forgot_password_token = models.SlugField(unique=True, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def name(self):
        return self.first_name +" "+ self.last_name
    
    def __str__(self) -> str:
        return self.email
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(CustomUser, self).save(*args, **kwargs)
        
    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid = False, cart__user__email = self.email).count()
            
    
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='carts')
    is_paid = models.BooleanField(default=False)
    razor_pay_order_id = models.CharField( max_length=150,null=True, blank=True)
    razor_pay_payment_id = models.CharField( max_length=150,null=True, blank=True)
    razor_pay_payment_signature = models.CharField( max_length=150,null=True, blank=True)
    
    
    def __str__(self) -> str:
        return self.user.email + " - cart" 
    
    def get_cart_total(self):
        cart_items = CartItems.objects.filter(cart__is_paid=False,cart=self)
        price = []
        for cart_item in cart_items:
            price.append(cart_item.item.price)
            
        return sum(price) 
    
    
class CartItems(models.Model):
    from products.models import Item
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE, related_name="cart_items")
    item = models.ForeignKey(Item,  on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self) -> str:
        if self.item:
            return f"{self.cart.user.email} - cart item - {self.item.item_name}"
        else:
            return f"{self.cart.user.email} - cart item - None"
    
    def get_item_price(self):
        return self.item.price
    
    
class LikedProducts(models.Model):
    from products.models import Item
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="liked_products")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True,blank=True, related_name="liked_by")
    
    
    def __str__(self):
        return self.user.email + " liked " + self.item.item_name
    
class order(models.Model):
    email = models.EmailField( max_length=254,null=True,blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="ordered",null=True,blank=True)
    bill_name = models.CharField(max_length=200,null=True,blank=True)
    phone_no = models.IntegerField(validators=[MaxValueValidator(999999999999),MinValueValidator(000000000000)],null=True, blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    order_id =  models.CharField( max_length=150,null=True, blank=True)
    address = models.TextField(null=True, blank=True,default=None)
    city = models.CharField(max_length=150,null=True, blank=True,default=None)
    slug = models.SlugField(unique=True, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name="order_cart")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(order, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.order_id
    
    def name(self):
        return self.order_id