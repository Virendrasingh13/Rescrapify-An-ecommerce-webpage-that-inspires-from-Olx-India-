from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from accounts.models import CustomUser, LikedProducts, order
from django.contrib.auth import get_user_model,login,logout,authenticate
from django.views.decorators.csrf import csrf_exempt
from helpers import send_email_token,send_password_email
import json
from django.contrib import messages
from helpers import generate_unique_hash
from accounts.models import Cart,CartItems,LikedProducts
from products.models import Item
import razorpay
from django.conf import settings


# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from .serializers import MyTokenObtainPairSerializer
# from rest_framework.response import Response

User = get_user_model()

# Create your views here.
def LoginView(request):
    
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return redirect('home:home')
    else:
        if request.method == "POST":
            try:
                # body = request.data
                body = request.POST
                if ('email' in body and 'password' in body):
                    email = body['email']
                    password = body['password']
                    
                    user_obj = User.objects.filter(email=email).first()
                    
                    if user_obj and not user_obj.is_superuser:
                        if not user_obj.is_verified:
                            raise Exception('You have to verify your mail through link sent to you by mail')
                        
                        user = authenticate(request=request, email=email, password=password)
                        if user:
                            login(request=request,user=user)
                            return redirect('home:home')
                            # print(login(request=request,user=user))
                            # refresh = MyTokenObtainPairSerializer.get_token(user=user)
                            # return Response({
                            #     # 'refresh': str(refresh),
                            #     # 'access': str(refresh.access_token),
                            #     'success':True,
                            #     'message':'Login Success'
                            # })
                        else:
                            raise Exception('Invalid Password!')
                    else:
                        raise Exception("No user with this email exists!")
                    
                else:
                    raise Exception('Provide proper credentials to login')
                    
            except Exception as e:
                messages.warning(request, str(e))
                return HttpResponseRedirect(request.path_info)
                # return JsonResponse({'success':False, 'message':str(e)})
            
        
        return render(request, 'accounts/login.html')
   

def Register(request):
    
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return redirect('home:home')
    
    else:  
        if request.method == "POST":
            try:
                body = request.POST
                # body = request.data
                if ('email' in body and 'password' in body):
                    email = body['email']
                    password = body['password']
                    first_name = body['first_name']
                    phone_no = body['phone_no']
                    last_name = body['last_name']
                    user_image = request.FILES.get('user_image')
                    if user_image: 
                        if user_image.size > 1*1024*1024:
                            raise Exception('Image size should be less than 1MB')
                    
                    user, created = User.objects.get_or_create(email=email)
                    if created :
                        user.first_name = first_name
                        user.phone_no = phone_no
                        user.last_name = last_name
                        user.set_password(password)
                        user.user_image = user_image
                        
                        user.save()
                        email_sent = send_email_token(email, user.slug)
                        if email_sent: 
                            messages.success(request, "Verification mail is sent your email")
                            return HttpResponseRedirect(request.path_info)
                            # return JsonResponse({
                            #     'success':True,
                            #     'message':'Verification mail is sent your email'
                            # })
                        else:
                            raise Exception('There is some problem in sending mail')
                            # return JsonResponse({
                            #     'success':False,
                            #     'message':"There's some problem in sending mail"
                            # })
                        
                    else:
                        raise Exception('User with this email already exists')
                    
                else:
                    raise Exception('Provide proper credentials ')
            
            except Exception as e:
                messages.warning(request, str(e))
                return HttpResponseRedirect(request.path_info)
                # return JsonResponse({
                #     'status':False,
                #     'message':str(e)
                #     })
                
        return render(request, 'accounts/signup.html')

def verify(request, slug):
    try:
        user = User.objects.filter(slug=slug).first()
        if user:
            if user.is_verified :
                if user.temp_email != None:
                    user.email = user.temp_email
                    user.temp_email = None
                    user.save()
                    logout(request)
                    context = {
                        'success': True,
                        'message': 'New email set Successfully'
                    }
                    context_obj = { 'data':json.dumps(context)}
                    return render(request, 'accounts/verify.html', context_obj) 
                    
                context = {
                    'success': True,
                    'message': 'Your email is already verified. Youc can login'
                }
            
            user.is_verified = True
            user.save()
            context = {
                    'success': True,
                    'message': 'Your email is verified. You can login'
                }
        
        else:
            raise Exception('Invalid verification link!')
        
    except Exception as e:
        print(e)
        context = {
                    'success': False,
                    'message': str(e)
                }
    finally:
        context_json = json.dumps(context)
        context_obj = { 'data':context_json}
        return render(request, 'accounts/verify.html', context_obj) 
        

def LogoutView(request):
    logout(request)
    return redirect('accounts:login')



def editProfile(request):
    if request.user.is_authenticated:
        
        if request.method == "POST":
            try:
                body = request.POST
                print(body)
                if 'first_name' in body and 'last_name' in body and 'email' in body and 'phone_no' in body:
                    user = request.user
                    if user.email == body['email']:
                        
                        user.first_name = body['first_name']
                        user.phone_no = body['phone_no']
                        user.last_name = body['last_name']
                        user.city = body['city']
                        user.state = body['state']
                        user_image = request.FILES.get('user_image')
                        if user_image: 
                            if user_image.size > 1*1024*1024:
                                raise Exception('Image size should be less than 1MB')
                            else:
                                user.user_image = user_image
                            
                        user.save() 
                        messages.success(request, "Profile updated successfully")
                        return HttpResponseRedirect(request.path_info)
                    else:
                        raise Exception('Do not try anything funny with email here')
                else:
                    raise Exception('Provide your all details to complete profile')
                    
            except Exception as e:
                messages.success(request, str(e))
                return HttpResponseRedirect(request.path_info)
            
        if request.method == "GET":
            # print(request.user.user_image.url)
            return render(request, 'accounts/edit_profile.html')
        
    else:
        messages.warning(request,'You must be logged in to access this page.')
        return redirect('accounts:login')
            
    
def change_password(request):
    
    if request.method == "POST":
        try:
            body = request.POST
            if 'cur_password' in body and 'new_password' in body:
                cur_password = body['cur_password']
                new_password = body['new_password']
                
                user = authenticate(request, email=request.user.email, password=cur_password)   
                
                if user :
                    if not user.is_superuser:
                        user.set_password(new_password)
                        user.save()
                        # messages.success(request, 'Password changed successfully, You have to login again')
                        return JsonResponse({'success':True, 'message':'Password changed successfully, You have to login again'})
                    
                    else:
                        raise Exception('You can not send this request')
                else:
                    raise Exception('Invalid password !')
                
            else:
                raise Exception('Insufficient credentials')   
                  
        except Exception as e:
            print(e)
            # messages.warning(request, str(e))
            return JsonResponse({'success':False,'message':str(e)})
    else:
        return redirect('accounts:edit_profile')
            
            
def change_email(request):
    if request.method == "POST":
       try:
            body = request.POST
            print(body)
            if 'cur_email' in body and 'new_email' in body:
                cur_email = body['cur_email']
                new_email = body['new_email']
                
                if cur_email == request.user.email:
                    user = User.objects.filter(email=cur_email).first()
                    if not user.is_superuser:
                        user.slug = generate_unique_hash()
                        user.temp_email = new_email
                        user.save()
                        email_sent = send_email_token(new_email, user.slug)
                        if email_sent:
                            return JsonResponse({'success':True, 'message':'Verification is sent on your new email'})
                        else:
                            raise Exception('There is some problem in sending mail')
                    else:
                        raise Exception('You can not send this request')
                    
                else:
                    raise Exception('Invalid current email!')
            else:
                raise Exception('Insufficient credentials!')
       except Exception as e:
           print(e)
           return JsonResponse({'success':False,'message':str(e)})
       
    else:
        return redirect('accounts:edit_profile')
       
def check_email(request):
    if request.method == "POST":
        try: 
            if 'cur_email' in request.POST:
                email = request.POST['cur_email']     
                user = User.objects.filter(email=email).first()
                
                if user and not user.is_superuser:
                    user.forgot_password_token = generate_unique_hash()
                    user.save()
                    email_sent = send_password_email(email,user.forgot_password_token)
                    if email_sent:
                        return JsonResponse({'success':True, 'message':'A email it sent to your email id'})
                    else:
                        raise Exception('There is some problem in sending mail')
            else:
                raise Exception('Don not try anything funny with email!')
            
        except Exception as e:
            print(e)
            # messages.warning(request,str(e))
            # return HttpResponseRedirect(request.path_info)
            
    else:
        return redirect('home:home')
    
def forgot_password(request, forgot_password_token):
    try:
        user = User.objects.filter(forgot_password_token=forgot_password_token).first()
        if user and not user.is_superuser:  
            if request.method == "POST":
                if 'new_password' in request.POST:
                    new_pass = request.POST['new_password']
                    user.set_password(new_pass)
                    user.save()
                    return JsonResponse({'success':True, 'message':'Password changed successfully, You have to login again'})
                else:
                    raise Exception('Do not try anything funny with the password')
                
                                
            return render(request, 'accounts/forgot_password.html')
        
        else:
            raise Exception('Invalid verfication link')
        
    except Exception as e:
        print(e)
        messages.warning(request,str(e))
        return redirect('accounts:forgot_password',forgot_password_token=forgot_password_token)

    
def cart(request):
    
    if request.user.is_authenticated:
        
        cart_obj = Cart.objects.filter(is_paid=False,user= request.user).first()
        if cart_obj:
            amount = float(cart_obj.get_cart_total() * 100)
           
            if amount < 100:
                amount = 100
            client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY_ID, settings.RAZOR_PAY_KEY_SECRET))
            data = { "amount": amount, "currency": "INR", 'payment_capture': 1}
            payment = payment = client.order.create(data=data)
            cart_obj.razor_pay_order_id = payment['id']
            cart_obj.save()
            print(payment)
            
            context = {'cart': cart_obj ,'payment':payment}
            return render(request, 'accounts/cart.html', context)
        else:
            amount = 100
            
            return render(request, 'accounts/cart.html') 
        
    else :
        messages.warning(request,'You need to be looged in to access cart')
        return redirect('accounts:login')


def add_to_cart(request, slug):
    try:
        if request.user.is_authenticated:
            item = Item.objects.filter(slug=slug).first()
            user = request.user
            cart , creatd = Cart.objects.get_or_create(user = user, is_paid=False)
            
            cart_items,created = CartItems.objects.get_or_create(cart = cart, item=item)
            if created:
                item.sold = True
                item.save()
                messages.success(request,'Item added in cart successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                raise Exception('Item is already in your cart')
        
        else:
            raise Exception('You need to be logged in')
    
        
    except Exception as e:
        print(e)
        messages.warning(request,str(e))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
def remove_cart(request,slug):
    try:
        cart_item = CartItems.objects.filter(item__slug=slug).first()
        if cart_item:
            item = Item.objects.filter(slug = slug ).first()
            item.sold = False
            item.save()
            cart_item.delete()
            messages.success(request,'Item removed from cart successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        else:
            raise Exception('There is some problem in removing cart')
        
    except Exception as e:
        print(e)
        messages.warning(request,str(e))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        
def success(request):
    try: 
        if request.method == "POST":
            body = request.POST
            print(body)
            
            if 'razorpay_order_id' in body and 'razorpay_payment_id' in body and 'razorpay_signature' in body :
                razor_pay_order_id = body['razorpay_order_id']
                razor_pay_payment_id = body['razorpay_payment_id']
                razor_pay_payment_signature = body['razorpay_signature']
            
                cart_obj = Cart.objects.filter(razor_pay_order_id=razor_pay_order_id).first()
                print(cart_obj)
                if cart_obj:
                    
                    amount = cart_obj.get_cart_total()
                    cart_obj.is_paid = True
                    cart_obj.razor_pay_payment_id = razor_pay_payment_id
                    cart_obj.razor_pay_payment_signature = razor_pay_payment_signature
                    cart_obj.save()
                    name = body['name']
                    email = body['email']
                    phone_no = body['phone_no']
                    city = body['city']
                    address = body['address']
                    
                    
                    order_obj,created = order.objects.get_or_create(order_id = razor_pay_order_id,cart=cart_obj)
                    if created:
                        order_obj.user = request.user
                        order_obj.bill_name = name
                        order_obj.email = email
                        order_obj.phone_no = phone_no
                        order_obj.address = address
                        order_obj.city = city
                        order_obj.amount = amount
                        order_obj.save()
                    
                        return JsonResponse({'success':True})
                    
                    else:
                        raise Exception('This order is already exist')
                
                else:
                    raise Exception("There is some error in order")
        
            else:
                raise Exception("Don't try to direct go to success page")
            
            
        else:
            print(request.GET)
            if 'razorpay_order_id' in request.GET:
                order_id = request.GET['razorpay_order_id']
                context = {'order_id':order_id}
                return render(request,'success.html',context)
            
            else:
                raise Exception('order id should be provided')
        
    except Exception as e:
        print(e)
        messages.warning(request, str(e))
        return JsonResponse({'success':False})
    
    
def invoice(request,order_id):
    try:
        order_obj = order.objects.filter(order_id=order_id).first()
        if order_obj:
            context = {'order':order_obj}
            return render(request, 'invoice.html',context)
        else:
            raise Exception('Invalid order id')
            
        
    except Exception as e:
        print(e)

def user_product(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            items_obj = Item.objects.filter(seller = request.user)
            print(items_obj)
            context = {'items':items_obj}
            return render(request, 'accounts/user_products.html',context)
    else:
        messages.warning(request, "You need to login")
        return redirect('accounts:login') 
    
def user_order(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            order_obj = order.objects.filter(user=request.user)
            
            print(order_obj)
            context = {'orders':order_obj}
            return render(request, 'accounts/user_orders.html',context)
    else:
        messages.warning(request, "You need to login")
        return redirect('accounts:login') 
    
def like_product(request):
    
    if request.user.is_authenticated:
        try:
            if request.method == "GET":
                print(request.GET)
                if 'slug' in request.GET:
                    slug = request.GET['slug']
                    print(slug)
                    item = Item.objects.filter(slug=slug).first()
                    if item:  
                        print(item)
                        liked_product, created = LikedProducts.objects.get_or_create(user=request.user, item=item)
                        print(liked_product)
                        if created:
                            print(liked_product)
                            item.likes += 1
                            item.save()
                            return JsonResponse({'success':True,'message': 'Product liked successfully.','liked': True,'likes':item.likes})

                        else:
                            liked_product.delete()
                            item.likes -= 1
                            item.save()
                            return JsonResponse({'success':True,'message': 'Product removed from liked successfully.','liked': False,'likes':item.likes})
                    else:
                        raise Exception('There is some problem in Product liking')
                    
                else:
                    raise Exception('Do not try to manipulate things')
                    
                   
                
        except Exception as e:
            print(e)
            messages.warning(request, str(e))
            return JsonResponse({'success':False,'message':str(e),'safe':False})
            
    else:
        messages.warning(request, "You need to login to like the Product")
        return JsonResponse({'success':False,'message':'redirect','safe':False})