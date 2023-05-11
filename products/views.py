from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ProductForm,VariationForm
from .models import Product, Variations
from categories.models import Category
from django.contrib.auth.decorators import user_passes_test, login_required

# Create your views here.
@user_passes_test(lambda user:user.is_superuser,login_url='/')
@login_required
def product_management(request):
    products = Product.objects.all().order_by("name").prefetch_related('categories')
    
    context = {
        'products': products
    }
    
    return render(request,"admin/admin_products.html",context)

@user_passes_test(lambda user:user.is_superuser,login_url='/')
@login_required
def add_product(request):
    if request.method == 'POST':
       

        
        productform = ProductForm(request.POST, request.FILES)
        variationform = VariationForm(request.POST)
       
        if productform.is_valid():
            
            product = productform.save(commit=False)
            product.save()
            productform.save_m2m()

            variation_values = request.POST.getlist('variation_value')
            for variation_value in variation_values:
                variation = Variations.objects.create(product=product, variation_value=variation_value)
                
                variation.save()
            



            return redirect('admin_product_management')

    else:
        productform = ProductForm()
        variationform = VariationForm()
        
    context = {
        'productform': productform,
        'variationform': variationform,
    }
    return render(request,'admin/admin_add_product.html',context)


@user_passes_test(lambda user:user.is_superuser,login_url='/')
@login_required
def delete_product(request):
    if request.method == 'POST':
        id = request.POST['product_id']
        product = Product.objects.get(id=id)
        for category in product.categories.all():
            category.products.remove(product)

        product.delete()
        try:
            variation = Variations.objects.filter(product_id = id)
            variation.delete()
        except:
            pass

        return redirect('admin_product_management')
    
# def edit_product(request):
#     categories = Category.objects.all()
#     if request.method == 'POST':
#         id = request.POST['product_id']
#         product = Product.objects.get(id=id)
#         context = {
#             'product':product,
#             'categories':categories
#         }
#     return render(request,'admin/admin_edit_product.html',context)

@user_passes_test(lambda user:user.is_superuser,login_url='/')
@login_required
def edit_product(request):
    if request.method == 'POST':
        id = request.POST['product_id']
        product = Product.objects.get(id=id)
        # variations = product.variations_set.all()
        productform = ProductForm(instance=product)
        variationform = VariationForm()
        
        context = {
            'productform':productform,
            'product':product,
            'variationform': variationform,
            # 'variations': variations,
            
            
        }
        return render(request,'admin/admin_edit_product.html',context)
    

@user_passes_test(lambda user:user.is_superuser,login_url='/')
@login_required
def edit_product_save(request):
    if request.method == 'POST':
        id = request.POST['product_id']
        product = Product.objects.get(id=id)
        productform = ProductForm(request.POST, request.FILES, instance=product)
        if productform.is_valid():
            productform.save()
            try:
                variation = Variations.objects.filter(product_id = id)
                variation.delete()
            except:
                pass

            
            variation_values = request.POST.getlist('variation_value')
            for variation_value in variation_values:
                variation = Variations.objects.create(product=product, variation_value=variation_value)
                
                variation.save()
            return redirect('admin_product_management')
        

