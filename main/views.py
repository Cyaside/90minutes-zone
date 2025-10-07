from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token

@login_required(login_url='/login')
def show_main(request):
    # data fetched via ajax endpoint aja
    context = {
        'npm': '2406358472',
        'name': 'Tristan Rasheed Satria',
        'class': 'PBP C',
        'last_login': request.COOKIES.get('last_login', 'Never'),
        'account_name': request.user.username,
    }
    return render(request, 'main.html', context)

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
    data = [
        {
            'id': str(product.id),
            'name': getattr(product, 'name', None),
            'description': getattr(product, 'description', None),
            'category': getattr(product, 'category', None),
            'category_display': product.get_category_display() if getattr(product, 'category', None) else None,
            'price': getattr(product, 'price', None),
            # Product.thumbnail is a URLField, so access directly
            'thumbnail': getattr(product, 'thumbnail', None),
            'views': getattr(product, 'views', 0),
            'is_featured': getattr(product, 'is_featured', False),
            'user_id': product.user_id,
        }
        for product in product_list
    ]
    return JsonResponse(data, safe=False)
    # json_data = serializers.serialize("json", product_list)
    # return HttpResponse(json_data, content_type="application/json")

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
   
def show_json_by_id(request, product_id):
    try:
        product = Product.objects.select_related('user').get(pk=product_id)
        data = {
            'id': str(product.id),
            'name': getattr(product, 'name', None),
            'description': getattr(product, 'description', None),
            'category': getattr(product, 'category', None),
            'category_display': product.get_category_display() if getattr(product, 'category', None) else None,
            'price': float(product.price) if getattr(product, 'price', None) is not None else None,
            'thumbnail': getattr(product, 'thumbnail', None),
            'views': getattr(product, 'views', 0),
            'is_featured': getattr(product, 'is_featured', False),
            'user_id': product.user_id,
            'user_username': product.user.username if product.user_id else None,
        }
        return JsonResponse(data, status=200)
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)
   

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


@login_required(login_url='/login')
@require_POST
def add_product_ajax(request):
    form = ProductForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    product = form.save(commit=False)
    product.user = request.user
    product.save()

    data = {
        'id': str(product.id),
        'name': product.name,
        'price': product.price,
        'description': product.description,
        'category': product.category,
        'category_display': product.get_category_display(),
        'thumbnail': product.thumbnail,
        'is_featured': product.is_featured,
        'views': product.views,
        'user_username': product.user.username,
    }
    return JsonResponse({'status': 'success', 'product': data}, status=201)


@login_required(login_url='/login')
@require_http_methods(["PATCH", "POST"]) 
def update_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    form = ProductForm(request.POST, instance=product)
    if not form.is_valid():
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    product = form.save()
    data = {
        'id': str(product.id),
        'name': product.name,
        'price': product.price,
        'description': product.description,
        'category': product.category,
        'category_display': product.get_category_display(),
        'thumbnail': product.thumbnail,
        'is_featured': product.is_featured,
        'views': product.views,
        'user_id': product.user_id,
        'user_username': product.user.username,
    }
    return JsonResponse({'status': 'success', 'product': data}, status=200)


@login_required(login_url='/login')
@require_http_methods(["DELETE"]) 
def delete_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    product.delete()
    return JsonResponse({'status': 'success', 'id': str(id)}, status=200)


@require_POST
def login_ajax(request):
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        resp = JsonResponse({'status': 'success', 'username': user.username})
        resp.set_cookie('last_login', str(datetime.datetime.now()))
        return resp
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@require_POST
def register_ajax(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@login_required(login_url='/login')
@require_POST
def logout_ajax(request):
    logout(request)
    response = JsonResponse({'status': 'success'})
    response.delete_cookie('last_login')
    return response


@login_required(login_url='/login')
def csrf_token_json(request):
    return JsonResponse({'csrfToken': get_token(request)})