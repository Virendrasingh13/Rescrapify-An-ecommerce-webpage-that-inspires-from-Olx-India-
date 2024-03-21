from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render
from rest_framework.views import APIView
from helpers import send_Contact_mail
from django.contrib import messages
from products.models import Item,Category
from django.db.models import Q
# Create your views here.
def home(request):
    categories = Category.objects.all()
    unsold_items_by_category = {}
    
    for category in categories:
        unsold_items_by_category[category] = Item.objects.filter(category_name=category, sold=False)
    
    context = {'items': Item.objects.filter(sold=False),'unsold_items_by_category': unsold_items_by_category, 'categories': categories}
    return render(request, 'home.html', context)

def search_items(request):
    query = request.GET.get('search')
    if query:
        items = Item.objects.filter(item_name__icontains=query)
    else:
        items = Item.objects.all()
        
    categories = Category.objects.all()
    unsold_items_by_category = {}
    
    for category in categories:
        unsold_items_by_category[category] = Item.objects.filter(category_name=category, sold=False)
    return render(request, 'home.html', {'items': items,'categories': categories,'unsold_items_by_category': unsold_items_by_category})

def get_items_by_category(request):
    
    if request.method == "GET":
        
        try:
        
            if 'category' in request.GET:
                category = request.GET['category']
                items_obj = Item.objects.filter(category_name__category_type =  category,sold=False) | Item.objects.filter(category_name__category_name = category ,sold=False)
                if items_obj:
                    
                    items = [{
                        'item_name':item .item_name,
                        'price' : item.price,
                        'slug' : item.slug,
                        'image' : item.item_image.first().image.url if item.item_image.exists() else None,

                    } for item in items_obj]
                    
                elif request.GET['category']=="All":
                    items_obj = Item.objects.filter(sold=False)
                    items = [{
                        'item_name':item .item_name,
                        'price' : item.price,
                        'slug' : item.slug,
                        'image' : item.item_image.first().image.url if item.item_image.exists() else None,
                    } for item in items_obj]
                else:
                    items = []

                return JsonResponse({'success':True,'items':items})
        
            
            
            
            return JsonResponse({'success':True,'items':items})
        except Exception as e:
            print(e)
            return JsonResponse({'success':False,'message':str(e)})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def about(request):
    return render(request, 'about.html')

def contact(request):
    
    if request.method == "POST":
        try:
            if request.user.is_authenticated:
                # body = request.data
                body = request.POST
                print(body)
                if ('name' in body and 'email' in body and 'phone_no' in body and 'subject' in body) :
                    if request.user.email == body['email']:
                        name = body['name']
                        email = body['email']
                        phone_no = body['phone_no']
                        subject = body['subject']
                        message = body['message']
                        
                        email_sent = send_Contact_mail(name,email,subject,message,phone_no)
                        if email_sent:
                            messages.success(request, "Email is sent")
                            return HttpResponseRedirect(request.path_info)
                        # return JsonResponse({
                            #     'success':True,
                            #     'message':'Email is sent'
                            # })
                        else:
                            raise Exception('Can not send the mail ')
                        
                    else:
                        raise Exception('Use the same email you logged in with.')
                        
                else:
                    raise Exception('Provide proper credentials')   
            else:
                raise Exception("You need to be logged in to send mail")
        except Exception as e:
            messages.warning(request, str(e))
            return HttpResponseRedirect(request.path_info)
            # return JsonResponse({'success':False, 'message':str(e)})
        
    return render(request,'contact.html')
    


