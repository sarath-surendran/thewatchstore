from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from products.models import Product,Variations
from .models import Wishlist
from django.http import HttpResponse


@login_required
def wishlist(request):
    wish_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wish_items': wish_items
    }
    return render(request,'user/wishlist.html',context)


@login_required
def add_to_wishlist(request,product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    # cart = None
    
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            value = request.POST[item]
        
        try:
            variation = Variations.objects.get(variation_value=value,product=product)
            product_variation.append(variation)
        except:
            pass
        
    

   

    is_wish_item_exists = Wishlist.objects.filter(product=product,user=current_user).exists()

    if is_wish_item_exists:
       
        wish_item = Wishlist.objects.filter(product=product, user=current_user)
        existing_variation_list = []
        id = []
        for item in wish_item:
            existing_variation = item.variations.all()
            existing_variation_list.append(list(existing_variation))
            id.append(item.id)
        

        if product_variation in existing_variation_list:
            return redirect('wishlist')
        else:
            item = Wishlist.objects.create(product=product,user=current_user)
            
            if len(product_variation) > 0:
                print('wishlist')
              
                item.variations.clear()
               
                item.variations.add(*product_variation)
               
            item.user = current_user
            item.save()
           
    else:
      
        wish_item = Wishlist.objects.create(
            product=product,
           
            user=current_user,
        )
        if len(product_variation) > 0:
            wish_item.variations.clear()
            wish_item.variations.add(*product_variation)
        wish_item.user = request.user
        wish_item.save()

    return redirect('wishlist')

@login_required
def remove_wishlist(request,product_id,wish_item_id):
    
    product = get_object_or_404(Product,id=product_id)
    
    wish_item = Wishlist.objects.get(user=request.user, product=product,id = wish_item_id)
    wish_item.delete()
    return redirect('wishlist')