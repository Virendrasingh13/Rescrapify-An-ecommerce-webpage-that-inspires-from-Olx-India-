from django.urls import path
from products.views import sellProduct,get_categories_by_type,get_product,buy_product

app_name = 'products'

urlpatterns = [
    path('sellproduct/',sellProduct,name='sell_product'),
    path('get_categories_by_type/', get_categories_by_type, name='get_categories_by_type'),
    path('<slug>', get_product, name="get_product"),
    path('buy/',buy_product,name="buy_product"),
]   
