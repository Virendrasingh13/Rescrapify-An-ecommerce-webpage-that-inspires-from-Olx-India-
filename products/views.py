from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import Category,Item,Item_image
from django.contrib import messages


# Create your views here.
def sellProduct(request):
    
    if request.user.is_authenticated:
    
        if request.method == "POST":
            try:
                body = request.POST
                print(body)
                if 'category_slug' in body and 'item_name' in body and 'price' in body and 'item_image1' in request.FILES and 'item_image2' in request.FILES and 'description' in body:
                    item_name = body['item_name']
                    category_slug = body['category_slug']
                    price = body['price']
                    item_image1 = request.FILES.get('item_image1')
                    item_image2 = request.FILES.get('item_image2')
                    
                    description = body['description']
                    user = request.user
                    print(user)
                    if item_image1.size > 1*1024*1024 or  item_image2.size > 1*1024*1024:
                            raise Exception('Image size should be less than 1MB')
                        
                    category_obj = Category.objects.filter(slug=category_slug).first()
                    item_obj,created = Item.objects.get_or_create(item_name= item_name, seller=user, price=price,category_name=category_obj)
                    if created:
                        item_obj.description = description
                        item_image_obj1 = Item_image.objects.create(item=item_obj,image = item_image1)
                        item_image_obj2 = Item_image.objects.create(item=item_obj,image = item_image2)
                        item_obj.save()
                        messages.success(request,'Product added for sell successfully.')
                        return redirect('products:sell_product')
                        
                    else:
                        raise Exception('You have already added one product with same details')
                    
                else:
                    raise Exception('Insuffiecient ditails provided')
            except Exception as e:
                print(e)
                messages.warning(request,str(e))
                return redirect('products:sell_product')
    
        category = Category.objects.all()
        return render(request,'products/sell_product.html',{'category':category})
    
    else:
        messages.warning(request,'You must be logged in to access this page.')
        return redirect('accounts:login')


def get_categories_by_type(request):
    try:
        if request.method == "GET" and 'type' in request.GET:
            category_type = request.GET['type']
            categories_obj = Category.objects.filter(category_type=category_type)
            if categories_obj:
                categories = [{'category_name':category.category_name, 'slug':category.slug } for category in categories_obj]
                return JsonResponse({'success':True,'categories':categories})
            else:
                raise Exception("Don't try anything funny with the fields")
        else :
            raise Exception('Invalid category request')
    except Exception as e:
        print(e)
        return JsonResponse({'success':False,'message':str(e)})

        
def get_product(request, slug):
    
    try:
        
        item = Item.objects.filter(slug=slug).first()
        context = {'item':item}
        return render(request, 'products/product.html',context)
    except Exception as e:
        print(e)
        
def buy_product(request):
    try:
        if 'category' in request.GET:
            category_type = request.GET['category']
            category_obj = Category.objects.filter(category_type=category_type)
            items_obj = Item.objects.filter(category_name__category_type =  category_type,sold=False)
            # categories = Category.objects.all()
        unsold_items_by_category = {}
        
        for category in category_obj:
            unsold_items_by_category[category] = Item.objects.filter(category_name=category, sold=False)
        
        
        context = {'items':items_obj,'unsold_items_by_category': unsold_items_by_category,'categories':category_obj}

        return render(request,'products/buy.html',context)
       
                
    except Exception as e:
        print(e)
       
         