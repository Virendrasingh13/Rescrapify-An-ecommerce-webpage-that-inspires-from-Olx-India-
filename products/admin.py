from django.contrib import admin
from .models import Item, Category,Item_image
# Register your models here.

admin.site.register(Category)

class ItemImageAdmin(admin.StackedInline):
    model = Item_image
admin.site.register(Item_image)

class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemImageAdmin]

admin.site.register(Item, ItemAdmin)