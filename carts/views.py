from decimal import Decimal
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from products.models import Product,Variations
from .models import Cart,CartItem
from django.contrib.auth.decorators import login_required
from user_home.forms import AddressForm
from user_home.models import UserAddress
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from carts.models import Coupon

# Create your views here.

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active = True)
        for cart_item in cart_items:
            total += cart_item.product.selling_price * cart_item.quantity
            quantity += cart_item.quantity
    except:
        pass
    
    grant_total = total + 40
    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'grand_total': grant_total
    }

    return render(request, 'user/cart2.html', context)

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# def add_to_cart(request,product_id):
#     product = Product.objects.get(id=product_id)
#     cart = None
#     # if not request.user.is_authenticated:
#         # try:
#         #     cart = Cart.objects.get(cart_id=_cart_id(request))
#         # except Cart.DoesNotExist:
#         #     cart = Cart.objects.create(
#         #         cart_id = _cart_id(request)
#         #     )
#         # cart.save()

#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user)
#         else:
#             try:
#                 cart = Cart.objects.get(cart_id=_cart_id(request))
#             except Cart.DoesNotExist:
#                 cart = Cart.objects.create(
#                     cart_id = _cart_id(request)
#                 )
#             cart.save()
#             cart_item = CartItem.objects.get(product=product, cart=cart)
#         cart_item.quantity += 1
#         cart_item.save()
#     except CartItem.DoesNotExist:
#         cart_item = CartItem.objects.create(
#             product =  product,
#             cart = cart,
#             quantity = 1,
#             user = request.user
#         )
#         cart_item.save()
#     # return HttpResponse(cart_item.quantity)
#     return redirect('cart')


CustomUser = get_user_model()

def add_to_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    cart = None
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                value = request.POST[item]
            
            try:
                variation = Variations.objects.get(variation_value=value,product=product)
                product_variation.append(variation)
            except:
                pass
            
        

        # Check if the user is authenticated and is an instance of CustomUser
        # This code is different from the tutorial. If error occures bring this code and make necessory changes.
        # if isinstance(request.user, CustomUser):
        #     user = request.user
        # else:
        #     user = None
        #     try:
        #         cart = Cart.objects.get(cart_id=_cart_id(request))
        #     except Cart.DoesNotExist:
        #         cart = Cart.objects.create(cart_id=_cart_id(request))

        is_cart_item_exists = CartItem.objects.filter(product=product,user=current_user).exists()

        if is_cart_item_exists:
            # Try to get an existing cart item for the given product and user
            #removing cart=cart from the cart_item filter add if error occurs
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)
            

            if product_variation in existing_variation_list:
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.user = current_user
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product,quantity=1,user=current_user)
                # print("item created")
                if len(product_variation) > 0:
                    # print('product variation > 0')
                    item.variations.clear()
                    # print('item variation cleared')
                    item.variations.add(*product_variation)
                    # print('item variation added')
                item.user = current_user
                item.save()
                # print('item saved')
        else:
            # Create a new cart item if one does not exist
            cart_item = CartItem.objects.create(
                product=product,
                # cart=cart,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.user = request.user
            cart_item.save()

        return redirect('cart')
    # if user is not authenticated
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))

        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                value = request.POST[item]
            
            try:
                variation = Variations.objects.get(variation_value=value,product=product)
                product_variation.append(variation)
            except:
                pass
            
        

        # Check if the user is authenticated and is an instance of CustomUser
        # if request.user.is_authenticated and isinstance(request.user, CustomUser):
        #     user = request.user
        # else:
        #     user = None
        

        is_cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()

        if is_cart_item_exists:
            # Try to get an existing cart item for the given product and user
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)
            print(existing_variation_list)

            if product_variation in existing_variation_list:
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                # if isinstance(user, CustomUser):
                #     item.user = user
                # else:
                #     item.user = None
                # item.user=current_user
                item.cart = cart
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product,quantity=1,cart=cart)
                print("item created")
                if len(product_variation) > 0:
                    print('product variation > 0')
                    item.variations.clear()
                    print('item variation cleared')
                    item.variations.add(*product_variation)
                    print('item variation added')
                # if user.is_authenticated and isinstance(user, CustomUser):
                #     item.user = user
                # else:
                #     item.user = None
                item.user = current_user
                item.save()
                print('item saved')
        else:
            # Create a new cart item if one does not exist
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=1,
                # user = current_user
                
            )
           
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            # cart_item.user = current_user
            cart_item.cart = cart
            cart_item.save()

        return redirect('cart')


def decrease_cart(request,product_id,cart_item_id):
    
    product = get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product,user=request.user, id = cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(cart=cart,product=product,id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart(request,product_id,cart_item_id):
    
    product = get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(user=request.user, product=product,id = cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(cart=cart, product=product,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='login')
def checkout(request,total=0,quantity=0, cart_items = None):
    cart_items = CartItem.objects.filter(user=request.user)
    if cart_items.count() > 0:
        try:
            # if request.user.is_authenticated:
            #     cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            # else:
            #     cart = Cart.objects.get(cart_id=_cart_id(request))
            #     cart_items = CartItem.objects.filter(cart=cart, is_active = True)
            
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            for cart_item in cart_items:
                total += cart_item.product.selling_price * cart_item.quantity
                quantity += cart_item.quantity
        except:
            pass
        
        user = request.user
        referal_count = user.referal_count
        if user.referal_count > 0:
            grant_total = total - 1000
            referal_discount = 1000
        else:
            grant_total = total + 40
            referal_discount = 0

    
        addresses = UserAddress.objects.filter(user=request.user)
        context = {
            'cart_items': cart_items,
            'total': total,
            'quantity': quantity,
            'grand_total': grant_total,
            'referal_discount': referal_discount,
            'addresses': addresses,
            'referal_count': referal_count,
        }

        return render(request, 'user/checkout.html', context)
    else:
        return redirect('cart')
    
def verify_coupon(request):
    if request.method == 'POST':
        value = request.POST['coupon']
        
        try:
            coupon = Coupon.objects.get(code__exact=value,is_active=True)
            # coupon_applied = True
            # request.session['coupon_applied'] =  coupon_applied
            request.session['coupon_code'] = coupon.code
            valid = True
            #######
            cart_items = CartItem.objects.filter(user=request.user)
            total = 0
            for cart_item in cart_items:
                total += cart_item.product.selling_price * cart_item.quantity
            grand_total = total + 40
            discount = ((Decimal(grand_total)*coupon.discount)/100)
            grand_total = Decimal(grand_total)-discount
            return JsonResponse({
            'valid': valid,
            'grand_total': grand_total,
            'discount': discount,
            })
        except:
            valid = False
            return JsonResponse({
                'valid': valid,
            })
        
def remove_coupon(request):
    if request.method == 'POST':
        discount = request.POST['discount']
        total = request.POST['grand_total']
        grand_total = float(total) + float(discount)
        del request.session['coupon_code']
        return JsonResponse({
            'grand_total': grand_total,
        })

        
        
        

