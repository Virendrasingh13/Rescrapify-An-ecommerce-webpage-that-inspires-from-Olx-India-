from django.contrib import admin
from .models import CustomUser,Cart,CartItems,LikedProducts,order
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(CartItems)
admin.site.register(Cart)
admin.site.register(LikedProducts)
admin.site.register(order)