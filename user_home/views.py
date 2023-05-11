from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache,cache_control
from django.core.mail import send_mail
from django.conf import settings
from random import randint
from .models import CustomUser as User, UserAddress, Referals
from django.http import HttpResponse
from django.contrib import messages
from .forms import RegistrationForm,AddressForm
from twilio.rest import Client
from products.models import Product,Variations
from categories.models import Category
from carts.models import Cart,CartItem
from carts.views import _cart_id
from offers.models import ProductOffers,CategoryOffers

# Create your views here.
def index(request):
    products = Product.objects.all()
    men_watches = []
    women_watches = []
    smart_watches = []
    for product in products:
        for category in product.categories.all():
            if category.name == "Men Watches" and product.is_avaliable == True and product.quantity > 0:
                men_watches.append(product)
            elif category.name == "Women Watches" and product.is_avaliable == True and product.quantity > 0:
                women_watches.append(product)
            elif category.name == "Smart Watches" and product.is_avaliable == True and product.quantity > 0:
                smart_watches.append(product)
    # for product in products:
    #     for category in product.categories.all():
    #         if category.name == "Women Watches":
    #             women_watches.append(product)
    context = {
        'men_watches': men_watches[:3],
        'women_watches': women_watches[:3],
        'smart_watches': smart_watches[:3],
    }
    return render(request,'user/index.html',context)

def login(request):
    if request.user.is_authenticated:
        return redirect('index') # change this after adding a profile.html 
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            # otp = randint(100000,999999)
            # request.session['email'] = email
            # request.session['otp'] = otp
            # send_mail(
            #     'OTP Verification',
            #     f"Your OTP is {otp}",
            #     settings.EMAIL_HOST_USER,
            #     [email],
            #     fail_silently=False,
            # )
            # return redirect('verify_otp')
            if user.is_verified:
                try:
                    
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    
                    is_cart_item_exist = CartItem.objects.filter(cart=cart).exists()
                    
                    if is_cart_item_exist:
                        cart_items = CartItem.objects.filter(cart=cart)
                        #Getting product variations

                        product_variation = []
                        for item in cart_items:
                            variation = item.variations.all()
                            product_variation.append(list(variation))


                        cart_item = CartItem.objects.filter(user=user)
                        existing_variation_list = []
                        id = []
                        for item in cart_item:
                            existing_variation = item.variations.all()
                            existing_variation_list.append(list(existing_variation))
                            id.append(item.id)

                        for pr in product_variation:
                            if pr in existing_variation_list:
                                index = existing_variation_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity += 1
                                item.user = user
                                item.save()
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()



                        
                except:
                    
                    pass
                auth.login(request,user)
                # del request.session['otp']
                return redirect('index')
            else:
                otp = randint(100000,999999)
                request.session['email'] = email
                request.session['otp'] = otp
                send_mail(
                    'OTP Verification',
                    f"Your OTP is {otp}",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                return redirect('verify_register')
                
        else:
            error_msg = "Invalid Username or Password"
            return render(request,'user/login.html',{'error_msg' : error_msg})
            #messages.error(request, "Invalid credentials")  
        
    
    return render(request,'user/login.html')

def phone_login(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        if phone == '':
            messages.error(request,"Enter valid phone number")
            
        else:
            user = User.objects.get(phone=phone)
            
            if user is not None:
                otp = randint(100000,999999)
                request.session['phone'] = phone
                request.session['otp'] = otp
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    body=f'Your OTP is {otp}',
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to='+91'+ phone
                )
                return redirect('verify_login')
            else:
                messages.error(request,"User not Found")
                return render(request,'user/phone_login.html')
    
    return render(request,'user/phone_login.html')    

def verify_login(request):
    if 'otp' not in request.session:
        return redirect('index')
    if request.method == 'POST':
        otp = request.POST['otp']
        if otp == '':
            messages.error(request,"Enter valid OTP")
            return redirect('verify_login')
        if int(otp) == request.session['otp']:
            phone = request.session['phone']
           
            #//////////This is enough for login if otp is passed in session/////////#
             # user = User.objects.get(phone=phone)
            # if user is not None:
            #     auth.login(request,user)
            #     del request.session['otp']
            #     del request.session['phone']
            #     return redirect('index')
            #When using this change the settings. Remove Authentication backends from setiings.
            #///////////////////////////////////////////#

            
            user = auth.authenticate(request,phone=phone)
            print(user)
            if user is not None:
                auth.login(request,user)
                del request.session['otp']
                del request.session['phone']
                return redirect('index')
            
        else:
            messages.error(request,'Invalid OTP')
    
    return render(request,'user/verify_login.html')

def verify_register(request):
    if 'otp' not in request.session:
        return redirect('index')
    
    if request.method == 'POST':
        otp = request.POST['otp']
        if otp == '':
            messages.error(request,"Incorrect OTP")
            return redirect('verify_register')
        if int(otp) == request.session['otp']:
            email = request.session['email']
            user = User.objects.get(email=email)
            user.is_verified = True
            user.save()
            # auth.login(request,user)
            del request.session['otp']

            return redirect('login')
        else:
            messages.error(request,"Invalid Credentials")
    
    return render(request,'user/verify_register.html')    

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        # # date_of_birth = request.POST['birthday']
        # # gender = request.POST.get('gender')
        # email = request.POST['email']
        # phone = request.POST['phone']
        # password = request.POST['password']
        # confirm_password = request.POST['confirm_password']
        # if first_name == '' or last_name == '' or email == '' or phone == '' or password == '' or confirm_password == '' :
        #     messages.error(request,"Fields cannot be empty")
        # else:
        form = RegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            referal = request.POST['referal']
            #image = form.cleaned_data['image']
            if password == confirm_password:
                if User.objects.filter(email=email).exists():
                    messages.error(request,"Email already exists")
                elif User.objects.filter(phone = phone).exists():
                    messages.error(request,"Phone already exists")
                else:
                    user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email, phone=phone,password=password)
                    #user.image = image
                    user.save()
                    otp = randint(100000,999999)
                    print("Otp is :" + str(otp))
                    request.session['email'] = email
                    request.session['otp'] = otp
                    send_mail(
                        'OTP Verification',
                        f"Your OTP is {otp}",
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                    )

                    #Generate Referal code#
                    id = user.id
                    name = user.first_name.replace(" ", "")
                    referal_code = name + str(id)
                    user.referal_code = referal_code
                    user.save()

                    #setting who refferd user
                    if referal != None:
                        refered_user = User.objects.get(referal_code=referal)
                        referal_data = Referals()
                        referal_data.refered_by = refered_user
                        referal_data.joined_user = user
                        referal_data.save()
                        refered_user.referal_count += 1
                        refered_user.save()
                    else:
                        print("no referal")


                    return redirect('verify_register')
                    
                    # return render(request,'user/login.html')
            else:
                messages.error(request,"Passwords not matching")

    forms = RegistrationForm()
    context = {
        'forms':forms
    }
    return render(request, 'user/register.html',context)



    
    # return render(request,'user/register.html')


def forgot_password(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        email = request.POST['email']
        if email == '':
            messages.error(request,"Email cannot be blank")
            return redirect('forgot_password')
        else:
            
            if User.objects.filter(email=email).exists():
                otp = randint(10000,999999)
                request.session['email'] =  email
                request.session['otp'] = otp
                send_mail(
                            'Password Reset',
                            f"Your OTP is {otp}",
                            settings.EMAIL_HOST_USER,
                            [email],
                            fail_silently=False,
                        )
                
                return render(request,'user/verify_reset_otp.html')
            else:
                messages.error(request,"Email does not exist.")
                return render(request,'user/forgot_password.html')
    return render(request,'user/forgot_password.html')

def verify_reset_otp(request):
    if 'otp' not in request.session:
        return redirect('forgot_password')
    
    if request.method == 'POST':
        otp = request.POST['otp']
    
        if otp == '':
            messages.error(request,'Enter valid otp')
            return redirect('verify_reset_otp')
        elif int(otp) == request.session['otp']:
            return render(request,'user/reset_password.html')
        else:
            messages.error(request,"Invalid OTP")
            return redirect('verify_reset_otp')
    return render(request,'user/verify_reset_otp.html')

def reset_password(request):
    if 'otp' not in request.session:
        return redirect('forgot_password')
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == '' or confirm_password == '':
            messages.error(request,"Fields cannot be empty")
            return redirect('reset_password')
        if password == confirm_password:
            email = request.session['email']
            user = User.objects.get(email=email)
            
            user.set_password(password)
            user.save()
            del request.session['otp']
            del request.session['email']
            
            return redirect('login')
        else:
            messages.error(request,"Passwords doesn't match")
            return redirect('reset_password')
    else:
        return render(request,'reset_password.html')

@never_cache
@login_required
def logout(request):
    auth.logout(request)
    return redirect('index')



def product_details(request,id):
    product = Product.objects.get(id=id)
    related_products = Product.objects.filter(categories__in=product.categories.all(),is_avaliable=True).exclude(id=id)
    variations = Variations.objects.filter(product=id)
    # prooffers = ProductOffers.objects.filter(product=product)
    # for prooffer in prooffers:
    #     if prooffer.is_active:
    #         if prooffer.is_applied == False:
    #             product.selling_price = product.selling_price - prooffer.discount
    #             product.save()
    #             prooffer.is_applied = True
        
    # categories = product.categories.all()
    # for category in categories:
    #     catoffers = CategoryOffers.objects.filter(category=category)
    #     for catoffer in catoffers:
    #         if catoffer.is_active:
    #             if not catoffer.is_applied:
    #                 product.selling_price = product.selling_price - catoffer.discount
    #                 product.save()
    #                 catoffer.is_applied = True
           

    context = {
        'product': product,
        'related_products':related_products[0:4],
        'variations': variations,
    }
    return render(request,'user/product_detail.html',context)


def category_wise_listing(request,cat_name):
    
    category = Category.objects.get(name=cat_name)
    products = Product.objects.filter(categories__in=[category], is_avaliable = True)
    context = {
        'products': products,
        'cat_name': cat_name,
    }
    return render(request,'user/category_wise_listing.html',context)
@login_required(login_url='cart')
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        # if form.is_valid():
        #     data = UserAddress()
        #     data.first_name = form.cleaned_data['first_name']
        #     data.last_name = form.cleaned_data['last_name']
        #     data.email = form.cleaned_data['email']
        #     data.phone = form.cleaned_data['phone']
        #     data.address_line_1 = form.cleaned_data['address_line_1']
        #     data.address_line_2 = form.cleaned_data['address_line_2']
        #     data.city = form.cleaned_data['city']
        #     data.state = form.cleaned_data['state']
        #     data.country = form.cleaned_data['country']
        #     data.pincode = form.cleaned_data['pincode']
            
        #     data.user = request.user
        #     data.save()
        #     next_param = form.cleaned_data.get('next')
        #     print("Second : " + next_param)
        #     return redirect('profile')
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            next_param = form.cleaned_data.get('next')
            if next_param:
                return redirect(next_param)
            else:
                return redirect('profile')
    else:
        next_param = request.GET.get('next')
        print('first : '+ next_param)
        form = AddressForm(initial={'next': next_param})
    context = {
        'form': form
    }
    return render(request,'user/add_address.html',context)
