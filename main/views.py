from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from main.productForm import ProductForm
from main.models import Product
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime
from django.urls import reverse

@login_required(login_url='/login')
def show_main(request):
    product_list = Product.objects.all()
    
    products_by_category = [
        (label, product_list.filter(category=key))
        for key, label in Product.CATEGORY_CHOICES
    ]

    filter_type = request.GET.get("filter", "all") 

    if filter_type == "all":
        product_list = Product.objects.all()
        all_product = True
        my_product = False
    else:
        product_list = Product.objects.filter(user=request.user)
        all_product = False
        my_product = True

    featured_products = product_list.filter(is_featured=True)

    context = {
        'npm' : '2406358472',
        'name': 'Tristan Rasheed Satria',
        'class': 'PBP C',
        'product_list': product_list,
        'featured_products': featured_products,
        'products_by_category': products_by_category,
        'last_login': request.COOKIES.get('last_login', 'Never'),
        'account_name': request.user.username,
        'all_product': all_product,
        'my_product': my_product,
    }

    return render(request, "main.html", context)

@login_required(login_url='/login')
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        product_entry = form.save(commit = False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "create_product.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    # Increment views each time the detail page is accessed
    if hasattr(product, 'increment_views'):
        product.increment_views()

    context = {
        'product': product
    }
    return render(request, "product_detail.html", context)


def show_xml(request):
     product_list = Product.objects.all()
     xml_data = serializers.serialize("xml", product_list)
     return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request,product_id):
   try:
       product_item = Product.objects.filter(pk=product_id)
       xml_data = serializers.serialize("xml", product_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except Product.DoesNotExist:
       return HttpResponse(status=404)

def show_json_by_id(request,product_id):
   try:
       product_item = Product.objects.get(pk=product_id)
       json_data = serializers.serialize("json", [product_item])
       return HttpResponse(json_data, content_type="application/json")
   except Product.DoesNotExist:
       return HttpResponse(status=404)
   

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@login_required(login_url='/login')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.user != request.user:
        return redirect('main:product_detail', id)

    form = ProductForm(request.POST or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Product updated.')
        return redirect('main:product_detail', id)

    context = {
        'form': form,
        'product': product,
        'is_edit': True,
    }

    return render(request, "edit_product.html", context)

@login_required(login_url='/login')
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.user != request.user:
        return redirect('main:product_detail', id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted.')
        return HttpResponseRedirect(reverse('main:show_main'))

    return render(request, 'confirm_delete.html', {'product': product})
