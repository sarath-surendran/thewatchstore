from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import auth
from user_home.models import CustomUser as User
from orders.models import Orders,OrderProduct,Payment
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib import messages
from offers.models import ProductOffers,CategoryOffers
from offers.forms import ProductOfferForm,CategoryOfferForm
from products.models import Product
from carts.models import Coupon
from carts.forms import CouponAddForm
from django.utils import timezone
from django.db.models import Sum
from user_home.models import CustomUser



# Create your views here.
def admin(request):
    return redirect('/admin/login')
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')  #change this to admin dashboard
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)
        if user is not None:
            if user.is_superuser:
                auth.login(request,user)
                return redirect('admin_dashboard')
            else:
                return HttpResponse("Not admin")
        else:
            return HttpResponse("user not authenticated")
    return render(request,'admin/admin_login.html')

@user_passes_test(lambda user:user.is_superuser,login_url='/')
def admin_dashboard(request):
    today = timezone.now().date()
    order_total = Orders.objects.filter(created_at__date=today).aggregate(Sum('order_total'))
    total = order_total['order_total__sum']
    target = 1000000
    if total == None:
        percent = 0
    else:
        percent = ((total/target)*100)


    total_users = CustomUser.objects.count()
    orders = Orders.objects.all().order_by('order_number').reverse()

    context = {
        'total': total,
        'percent': percent,
        'total_users': total_users,
        'orders': orders[:10]
    }
    return render(request,'admin/admin_dashboard.html',context)

@user_passes_test(lambda user:user.is_superuser,login_url='/')
@login_required
def admin_profile(request):
    return HttpResponse("Dynamic Admin profile")


@user_passes_test(lambda user:user.is_superuser,login_url='/')
@login_required
def user_management(request):
    users = User.objects.all().order_by('first_name').values()
    context = {
        'users': users
    }
    return render(request,'admin/admin_users.html',context)


@user_passes_test(lambda user:user.is_superuser,login_url='/')
@login_required
def block_user(request):
    id = request.POST['user_id']
    user = User.objects.get(id = id)
    if user.is_active:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return redirect('admin_user_management')
@user_passes_test(lambda user:user.is_superuser,login_url='/')
@login_required
def delete_user(request):
    id = request.POST['user_id']
    user = User.objects.get(id=id)
    user.delete()
    return redirect('admin_user_management')

@user_passes_test(lambda user:user.is_superuser,login_url='/')
@login_required
def make_admin(request):
    id = request.POST['user_id']
    user = User.objects.get(id=id)
    if user.is_superuser:
        user.is_superuser = False
        user.save()
    else:
        user.is_superuser = True
        user.save()
    return redirect('admin_user_management')
    

# @user_passes_test(lambda user:user.is_superuser,login_url='/')
# @login_required
# def product_management(request):
#     return HttpResponse("Product management page")

# @user_passes_test(lambda user:user.is_superuser,login_url='/')
# @login_required
# def category_management(request):
#     return HttpResponse("Caregory management page")

@user_passes_test(lambda user:user.is_superuser,login_url='/')
@login_required
def order_management(request):
    status_choices = Orders.STATUS
    orders = Orders.objects.all().order_by('order_number').reverse()
    context = {
        'orders': orders,
        'status_choices' : status_choices
    }
    return render(request,'admin/admin_order.html',context)

@user_passes_test(lambda user:user.is_superuser,login_url='/')
@login_required
def view_order(request,order_number):
    # if request.method == 'POST':
    #     id = request.POST['order_id']

        order = Orders.objects.get(order_number=order_number)
        ordered_products = OrderProduct.objects.filter(order=order)

        context = {
            'order': order,
            'ordered_products': ordered_products,
        }
        return render(request, 'admin/view_order.html',context)
    

@user_passes_test(lambda user:user.is_superuser,login_url='/')
@login_required    
def change_status(request, order_number):
    if request.method == 'POST':
        status = request.POST.get('status')
        order = Orders.objects.get(order_number=order_number)
        if order.status != status:
            order.status = status
        else:
            return redirect('admin_order_management')

        order.save()
        return redirect('admin_order_management')
    

@login_required
@user_passes_test(lambda user:user.is_superuser,login_url='/')
def admin_sales(request):
    return render(request,'admin/admin_sales.html')

@login_required
@user_passes_test(lambda user:user.is_superuser,login_url='/')
def sales_report(request):
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            # sales_data = Orders.objects.filter(
            #     created_at_gte=start_date, created_at_lte=end_date)
            sales_data = Orders.objects.filter(created_at__range=(start_date,end_date))
        else:
            sales_data = Orders.objects.all()

        context = {
            'data': sales_data,
            'start_date': start_date,
            'end_date': end_date
        }
        template_path = 'admin/sales_report.html'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="sales_report_{start_date}.pdf"'

        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            messages.error(request, 'Report Generating failed')
        return response
    else:
        return redirect('admin_order_management')
    

@login_required
@user_passes_test(lambda user:user.is_superuser,login_url='/')
def product_offers(request):
    offers = ProductOffers.objects.all()
    context = {
        'offers': offers
    }
    return render(request,'admin/product_offer_management.html',context)


@login_required
@user_passes_test(lambda user:user.is_superuser,login_url='/')
def add_product_offer(request):
    if request.method == 'POST':
        form = ProductOfferForm(request.POST)
        if form.is_valid():
            instance = form.save()
            # formproduct = form.cleaned_data['product']
            # discount = form.cleaned_data['discount']
            
            offer = ProductOffers.objects.get(pk=instance.id)
            product = offer.product 
            if product.pro_offer:
                if offer.is_active:
                    product.selling_price = product.selling_price - ((product.mrp*offer.discount)/100)
                    product.save()
            else:
                if product.cat_offer:
                    if offer.is_active:
                        product.selling_price = product.selling_price - ((product.mrp*offer.discount)/100)
                        product.pro_offer = True
                        product.save()
                else:
                    if offer.is_active:
                        product.selling_price = product.mrp - ((product.mrp*offer.discount)/100)
                        product.pro_offer = True
                        product.save()
            return redirect('product_offers')
    else:
        form = ProductOfferForm()
    context = {
        'form': form
    }
    return render(request,'admin/add_product_offer.html',context)


# @login_required
# @user_passes_test(lambda user:user.is_superuser,login_url='/')
# def edit_product_offer(request):
#     if request.method == 'POST':
#         id = request.POST['offer_id']
#         offer = ProductOffers.objects.get(id=id)
#         form = ProductOfferForm(instance=offer)
#         context = {
#             'form': form,
#             'id':id,
#         }
#         return render(request,'admin/edit_product_offer.html',context)
    
# @login_required
# @user_passes_test(lambda user:user.is_superuser,login_url='/')
# def edit_product_offer_save(request,id):
    
#     if request.method == 'POST':
#         offer = ProductOffers.objects.get(id=id)
#         form = ProductOfferForm(request.POST,instance=offer)
#         orderPro = offer.product
#         product = Product.objects.get(name=orderPro)
#         product.selling_price = product.selling_price + ((product.selling_price*offer.discount)/100)
#         print(product.selling_price)
#         if form.is_valid():
#             form.save()
#             formproduct = form.cleaned_data['product']
#             discount = form.cleaned_data['discount']
#             product = Product.objects.get(name=formproduct)
#             offer = ProductOffers.objects.get(product=product,discount=discount)
#             if offer.is_active:
#                 product.selling_price = product.selling_price - ((product.selling_price*discount)/100)
#                 product.save()
#             return redirect('product_offers')
#         else:
#             product.selling_price = product.selling_price - ((product.selling_price*offer.discount)/100)

        

@login_required
@user_passes_test(lambda user:user.is_superuser,login_url='/')
def delete_product_offer(request):
    if request.method == 'POST':
        id = request.POST['offer_id']
        offer = ProductOffers.objects.get(id=id)
        orderPro = offer.product
        product = Product.objects.get(name=orderPro)
        if offer.is_active:
            product.selling_price = product.selling_price + ((product.mrp*offer.discount)/100)
            product.save()
        
        offer.delete()
        remaining_offer = ProductOffers.objects.filter(product=product)
        if remaining_offer is None:
            product.pro_offer = False
        return redirect('product_offers')
    
def change_offer_status(request):
    if request.method == 'POST':
        offer_id = request.POST['id']
        offer = ProductOffers.objects.get(id=offer_id)
        orderPro = offer.product
        product = Product.objects.get(name=orderPro)
        if offer.is_active:
            offer.is_active = False
            product.selling_price = product.selling_price + ((product.mrp*offer.discount)/100)
            product.save()
        else:
            offer.is_active = True
            product.selling_price = product.selling_price - ((product.mrp*offer.discount)/100)
            product.save()

        offer.save()
        return JsonResponse({
            'is_active': offer.is_active,
        })


@login_required
@user_passes_test(lambda user:user.is_superuser,login_url='/')
def category_offers(request):
    offers = CategoryOffers.objects.all()
    context = {
        'offers': offers,
    }
    return render(request,'admin/category_offer_management.html',context)

@login_required
@user_passes_test(lambda user:user.is_superuser,login_url='/')
def add_category_offer(request):
    if request.method == 'POST':
        form = CategoryOfferForm(request.POST)
        if form.is_valid():
            instance = form.save()
            
            category = instance.category
            products = Product.objects.filter(categories=category)
            offer = CategoryOffers.objects.get(pk=instance.id)
            
            
            for product in products:
                if product.cat_offer:
                    if offer.is_active:
                        product.selling_price = product.selling_price - ((product.mrp*offer.discount)/100)
                        product.save()
                else:
                    if product.pro_offer:
                        if offer.is_active:
                            product.selling_price = product.selling_price - ((product.mrp*offer.discount)/100)
                            product.cat_offer = True
                            product.save()
                    else:
                        if offer.is_active:
                            product.selling_price = product.mrp - ((product.mrp*offer.discount)/100)
                            product.cat_offer = True
                            product.save()
            return redirect('category_offers')
    else:
        form = CategoryOfferForm()
    context = {
        'form': form
    }
    return render(request,'admin/add_category_offer.html',context)


# # @login_required
# # @user_passes_test(lambda user:user.is_superuser,login_url='/')
# # def edit_category_offer(request):
# #     if request.method == 'POST':
# #         id = request.POST['offer_id']
# #         offer = CategoryOffers.objects.get(id=id)
# #         form = CategoryOfferForm(instance=offer)
# #         context = {
# #             'form': form,
# #             'id':id,
# #         }
# #         return render(request,'admin/edit_category_offer.html',context)
    

# # @login_required
# # @user_passes_test(lambda user:user.is_superuser,login_url='/')
# # def edit_category_offer_save(request,id):
#      if request.method == 'POST':
#         offer = CategoryOffers.objects.get(id=id)
#         form = CategoryOfferForm(request.POST,instance=offer)
#         if form.is_valid():
#             form.save()
#             return redirect('category_offers')
        
@login_required
@user_passes_test(lambda user:user.is_superuser,login_url='/')
def delete_category_offer(request):
    if request.method == 'POST':
        id = request.POST['offer_id']
        offer = CategoryOffers.objects.get(id=id)
        orderCat = offer.category
        products = Product.objects.filter(categories=orderCat)
       
        
        
        for product in products:
            if offer.is_active:
                product.selling_price = product.selling_price + ((product.mrp*offer.discount)/100)
                product.save()

        offer.delete()

        remaining_offer = []        
        for product in products:
            categories = product.categories.all()
            for category in categories:
                remaining_offer_cat = CategoryOffers.objects.filter(category=category)
                remaining_offer.append(remaining_offer_cat)

            if remaining_offer is None:
                product.cat_offer = False
        

        return redirect('category_offers')
    
@login_required
@user_passes_test(lambda user:user.is_superuser,login_url='/')
def change_catoffer_status(request):
    if request.method == 'POST':
        offer_id = request.POST['id']
        offer = CategoryOffers.objects.get(id=offer_id)
        category = offer.category
        products = Product.objects.filter(categories=category)
        for product in products:
            if offer.is_active:
                
                product.selling_price = product.selling_price + ((product.mrp*offer.discount)/100)
                product.save()
                
            else:
                
                product.selling_price = product.selling_price - ((product.mrp*offer.discount)/100)
                product.save()

        offer.is_active = not offer.is_active
        offer.save()    
        
        
        return JsonResponse({
            'is_active': offer.is_active,
        })
    

@login_required
@user_passes_test(lambda user:user.is_superuser,login_url='/')
def coupons(request):
    coupons = Coupon.objects.all()
    context = {
        'coupons': coupons,
    }
    return render(request,'admin/coupons.html',context)

@login_required
@user_passes_test(lambda user:user.is_superuser,login_url='/')
def add_coupon(request):
    if request.method == 'POST':
        form = CouponAddForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('coupons')
    else:
        form = CouponAddForm()
    context = {
        'form': form,
    }
    return render(request,'admin/add_coupon.html',context)

@login_required
@user_passes_test(lambda user:user.is_superuser,login_url='/')
def delete_coupon(request):
    if request.method == 'POST':
        id = request.POST['coupon_id']
        coupon = Coupon.objects.get(id=id)
        coupon.delete()
        return redirect('coupons')
    
@login_required
@user_passes_test(lambda user:user.is_superuser,login_url='/')
def change_coupon_status(request):
    if request.method == 'POST':
        coupon_id = request.POST['id']
        coupon = Coupon.objects.get(id=coupon_id)
        
        

        coupon.is_active = not coupon.is_active
        coupon.save()    
        
        
        return JsonResponse({
            'is_active': coupon.is_active,
        })