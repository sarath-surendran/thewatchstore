from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from user_home.models import CustomUser,UserAddress
from user_home.forms import AddressForm,EditProfileForm
from orders.models import OrderProduct,Payment,Orders
from django.contrib.auth.models import auth

# Create your views here.
@login_required(login_url="index")
def profile(request):
    current_user = request.user
    user = CustomUser.objects.get(id=current_user.id)
    address = UserAddress.objects.filter(user=user)
    context = {
        'user': user,
        'address': address,
    }
    return render(request,'user/profile.html',context) 

@login_required
def view_address(request):
    user_id = request.user
    addresses = UserAddress.objects.filter(user=user_id)
    context = {
        'addresses': addresses,
    }
    return render(request,'user/view_address.html',context)

def edit_address(request,address_id):
    address = UserAddress.objects.get(id=address_id)

    if request.method == 'POST':
        addressform = AddressForm(request.POST,instance=address)
        if addressform.is_valid():
            addressform.save()
            return redirect('profile')
    else:
        addressform = AddressForm(instance=address)
    context = {
        'addressform': addressform,
        'address_id': address_id
    }
    return render(request,'user/edit_address.html',context)

@login_required
def delete_address(request,address_id):
    address = UserAddress.objects.get(id=address_id)
    address.delete()
    return redirect('view_address')


@login_required
def edit_user_profile(request,user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        userform = EditProfileForm(request.POST, instance=user)
        if userform.is_valid():
            userform.save()
            return redirect('profile')
    else:
        userform = EditProfileForm(instance=user)
    context = {
        'userform': userform,
        'user_id': user_id,
    }
    return render(request,'user/edit_user_profile.html',context)

@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        old_password = request.POST['old_password']
        if user.check_password(old_password):
            new_password = request.POST['new_password']
            user.set_password(new_password)
            user.save()
            
            return redirect('profile')
        else:
            return render(request, 'change_password.html', {'error_message': 'Incorrect old password'})
    
    return render(request,'user/change_password.html')


@login_required
def view_orders(request):
    current_user = request.user
    orders = OrderProduct.objects.filter(user=current_user).order_by('created_at').reverse()
    context = {
        'orders': orders,
    }

    return render(request,'user/view_order.html',context)

def view_order_details(request,id):
    order = OrderProduct.objects.get(id=id)
    context = {
        'order': order,
    }
    return render(request,'user/view_order_details.html',context)

def cancel_order(request,order_number):
    order = Orders.objects.get(order_number=order_number)
    order.status = 'Cancelled'
    order.save()
    return redirect('view_orders')