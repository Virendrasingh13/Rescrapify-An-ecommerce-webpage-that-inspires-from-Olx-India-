# from django.db import models
# from accounts.models import CustomUser
# from products.models import Item
# from helpers import generate_unique_hash


# # Create your models here.
# class Feedback(models.Model):
#     subject = models.CharField(max_length=255)
#     message = models.TextField()
#     slug = models.SlugField(null=True, blank=True, unique=True)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
    
#     def name(self):
#         return f"feedback of {self.item} by {self.user}"
    
#     def __str__(self) -> str:
#         return f"feedback of {self.item} by {self.user}" 
    
#     def save(self,*args, **kwargs):
#         if not self.slug:
#             self.slug = generate_unique_hash()
#         super(CustomUser, self).save(*args, **kwargs)