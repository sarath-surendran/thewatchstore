from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CategoryForm
from .models import Category
from django.contrib.auth.decorators import user_passes_test,login_required

# Create your views here.
@user_passes_test(lambda user:user.is_superuser,login_url='/')
@login_required
def category_management(request):
    categories = Category.objects.all().order_by('name').values()
    context = {
        'categories': categories
    }
    return render(request,"admin/admin_categories.html",context)


@user_passes_test(lambda user:user.is_superuser,login_url='/')
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_category_management')
    else:
        form = CategoryForm()
    context = {'form': form}
    return render(request,'admin/admin_add_category.html',context)

@user_passes_test(lambda user:user.is_superuser,login_url='/')
@login_required
def edit_category(request):
    if request.method == 'POST':
        cat_id = request.POST['category_id']
        category = Category.objects.get(id=cat_id)
        return render(request,'admin/admin_edit_category.html',{'category':category})
    
@user_passes_test(lambda user:user.is_superuser,login_url='/')
@login_required
def save_category(request):
    if request.method == 'POST':
        cat_name = request.POST['category_name']
        id = request.POST['category_id']
        category = Category.objects.get(id=id)
        category.name = cat_name
        category.save()
        return redirect('admin_category_management')

@user_passes_test(lambda user:user.is_superuser,login_url='/')
@login_required    
def delete_category(request):
    if request.method == 'POST':
        id = request.POST['category_id']
        category = Category.objects.get(id=id)
        category.delete()
        return redirect('admin_category_management')
