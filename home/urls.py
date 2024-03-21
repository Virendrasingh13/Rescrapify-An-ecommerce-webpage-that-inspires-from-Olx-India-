from django.urls import path
from .views import home,about,contact,get_items_by_category,search_items

app_name = 'home'

urlpatterns = [
    path('',home,name='home'),
    path('category_item/',get_items_by_category,name="get_items_by_category"),
    path("about/", about, name="about"),
    path("contact/",contact,name="contact"),
    path("search/",search_items,name="search")
]
