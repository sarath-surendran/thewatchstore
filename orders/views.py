from decimal import Decimal
from django.shortcuts import render,redirect
from carts.models import CartItem,Cart,Coupon
from carts.views import _cart_id
from .models import Orders,Payment,OrderProduct
from products.models import Product,Variations
from django.http import HttpResponse, JsonResponse
from user_home.models import UserAddress
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.
@login_required
def place_order(request,total=0,quantity=0):
    if request.method == 'POST':
        delivery_address_id = request.POST['delivery address']
        delivery_address = UserAddress.objects.get(id=delivery_address_id)
        # try:
        #     payment_mode = request.POST['payment_mode']
        #     payment_id = request.POST['payment_id']
            # new_payment = Payment()
            # new_payment.user = request.user
            # new_payment.payment_id = payment_id
            # new_payment.payment_method = payment_mode
            # new_payment.amount_paid = request.POST['total_price']
            # new_payment.status = "Paid"
            # new_payment.save()
            
        # except:
        #     pass
        
        cart_items = CartItem.objects.filter(user=request.user)
        # cart = Cart.objects.get(cart_id=_cart_id(request))
       
        
        
        for cart_item in cart_items:
            # cart = cart_item.cart
            # if coupon_applied:
            #     total += cart_item.product.selling_price * cart_item.quantity
            #     total = total-((cart_item.product.mrp * cart.coupon_discount)/100)
            # else:
            total += cart_item.product.selling_price * cart_item.quantity
            quantity += cart_item.quantity


        user = request.user
        if user.referal_count > 0:
            grant_total = total + 40
            grant_total = grant_total - 1000
            user.referal_count = user.referal_count - 1
            user.save()
        else:
            grant_total = total + 40
            try:
                # coupon_applied = request.session['coupon_applied']
                code = request.session['coupon_code']
                print("code in order : " + code)
                coupon = Coupon.objects.get(code=code)
                print('coupon object created')
                print(coupon.discount)
                discount = ((Decimal(grant_total)*coupon.discount)/100)
                grant_total = Decimal(grant_total)-discount
                print(grant_total)
                

            except Exception as e:
                print(e)

        
        
        
        
        data = Orders()
        data.user = request.user
        data.address = delivery_address
        data.order_total = grant_total
        data.save()
        #Generate Order Number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d= datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()

        #Since cash on delivery
        data.is_ordered = True
        data.save()

        for cart_item in cart_items:
            orderproduct = OrderProduct()
            # orderproduct.order_id=data.id
            orderproduct.order=data
            # orderproduct.user_id = request.user.id
            orderproduct.user = request.user
            # orderproduct.product_id = cart_item.product_id
            orderproduct.product = cart_item.product
            orderproduct.quantity = cart_item.quantity
            orderproduct.product_price = cart_item.product.selling_price*cart_item.quantity
            orderproduct.ordered = True
            ##################
            product_variation = list(cart_item.variations.all())
            for var in product_variation:
                variation = var

            var_obj = Variations.objects.get(variation_value=variation,product=cart_item.product)
            orderproduct.variation = var_obj
            
            

            ###############


            # orderproduct.save()
            # item = CartItem.objects.get(id=cart_item.id)
            # product_variation = item.variations.all()
            # orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            # orderproduct.variaton.set(product_variation)
            orderproduct.save()
            

            product = Product.objects.get(id=cart_item.product_id)
            product.quantity -= cart_item.quantity
            product.save()

        CartItem.objects.filter(user=request.user).delete()

        order = Orders.objects.get(order_number=order_number)
        ordered_products = OrderProduct.objects.filter(order=order)
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'total': total,
            
        }
        try:
            coupon = Coupon.objects.get(code=request.session['coupon_code'])
            context['coupon'] = coupon
            context['discount_amount'] = Decimal(grant_total) - Decimal(total)
            del request.session['coupon_code']
        except:
            pass
        return render(request,'user/confirmation.html',context)
        #     product = Product.objects.get(id=item.product.id)
        #     product.quantity -= quantity
        #     product.save()

        # CartItem.objects.filter(user=request.user).delete()

        # return render(request,'user/confirmation.html')
    else:
        return redirect('checkout')
    

@login_required
def place_order_online(request,total=0,quantity=0):
    if request.method == 'POST':
        delivery_address_id = request.POST['delivery address']
        delivery_address = UserAddress.objects.get(id=delivery_address_id)
        payment_mode = request.POST['payment_mode']
        payment_id = request.POST['payment_id']
        new_payment = Payment()
        new_payment.user = request.user
        new_payment.payment_id = payment_id
        new_payment.payment_method = payment_mode
        new_payment.amount_paid = request.POST['total_price']
        new_payment.status = "Paid"
        new_payment.save()


        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            total += cart_item.product.selling_price * cart_item.quantity
            quantity += cart_item.quantity


        user = request.user
        if user.referal_count > 0:
            grand_total = total + 40
            grand_total = grand_total - 1000
            user.referal_count = user.referal_count - 1
            user.save()
        else:
            grand_total = total + 40
            try:
                # coupon_applied = request.session['coupon_applied']
                code = request.session['coupon_code']
                print("code in order : " + code)
                coupon = Coupon.objects.get(code=code)
                print('coupon object created')
                print(coupon.discount)
                discount = ((Decimal(grand_total)*coupon.discount)/100)
                grand_total = Decimal(grand_total)-discount
                print(grand_total)
                request.session['discount'] = float(discount)

            except Exception as e:
                print(e)
        
        data = Orders()
        data.user = request.user
        data.address = delivery_address
        data.order_total = grand_total
        data.payment = new_payment
        data.save()
        #Generate Order Number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d= datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()

        #Since cash on delivery
        # data.is_ordered = True
        # data.save()

        for cart_item in cart_items:
            orderproduct = OrderProduct()
            # orderproduct.order_id=data.id
            orderproduct.order=data
            # orderproduct.user_id = request.user.id
            orderproduct.user = request.user
            # orderproduct.product_id = cart_item.product_id
            orderproduct.product = cart_item.product
            orderproduct.quantity = cart_item.quantity
            orderproduct.product_price = cart_item.product.selling_price*cart_item.quantity
            orderproduct.ordered = True
            orderproduct.payment = new_payment
            orderproduct.save()
            ##################
            product_variation = list(cart_item.variations.all())
            for var in product_variation:
                variation = var

            var_obj = Variations.objects.get(variation_value=variation,product=cart_item.product)
            orderproduct.variation = var_obj
            
            

            ###############


            # orderproduct.save()
            # item = CartItem.objects.get(id=cart_item.id)
            # product_variation = item.variations.all()
            # orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            # orderproduct.variaton.set(product_variation)
            orderproduct.save()

            product = Product.objects.get(id=cart_item.product_id)
            product.quantity -= cart_item.quantity
            product.save()

        total = float(total)
        CartItem.objects.filter(user=request.user).delete()
        return JsonResponse({
            'order_number':order_number,
            'total':total,
        })
        
@login_required
def order_confirmation(request):
    order_number = request.GET['order_number']
    total = request.GET['total']
    order = Orders.objects.get(order_number=order_number)
    order.is_ordered = True
    order.save()
    ordered_products = OrderProduct.objects.filter(order=order)
    context = {
        'order': order,
        'ordered_products': ordered_products,
        'total': total,
            
    }
    try:
        coupon = Coupon.objects.get(code=request.session['coupon_code'])
        context['coupon'] = coupon
        discount = request.session['discount']
        context['discount_amount'] = discount
        del request.session['discount']
        del request.session['coupon_code']
    except:
        pass
    return render(request,'user/confirmation.html',context)


    

@login_required
def razorpaycheck(request):
    if request.method == 'POST':
        id = request.POST['address_id']
        delivery_address = UserAddress.objects.get(id=id)
        first_name = delivery_address.first_name
        last_name = delivery_address.last_name
        email = delivery_address.email
        phone = delivery_address.phone
    cart_items = CartItem.objects.filter(user=request.user)
    total = 0
    for cart_item in cart_items:
        total += cart_item.product.selling_price * cart_item.quantity


    user = request.user
    if user.referal_count > 0:
        grand_total = total - 1000
    else:
        grand_total = total + 40
        try:
            # coupon_applied = request.session['coupon_applied']
            code = request.session['coupon_code']
            coupon = Coupon.objects.get(code=code)
            discount = ((Decimal(grand_total)*coupon.discount)/100)
            grand_total = Decimal(grand_total)-discount
            

        except Exception as e:
            print(e)

    return JsonResponse({
        'total_price': grand_total,
        'first_name': first_name,
        'last_name': last_name,
        'email':email,
        'phone': phone
    })