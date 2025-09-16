from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from main.productForm import ProductForm
from main.models import Product

def show_main(request):
    product_list = Product.objects.all()
    
    products_by_category = [
        (label, product_list.filter(category=key))
        for key, label in Product.CATEGORY_CHOICES
    ]

    context = {
        'npm' : '2406358472',
        'name': 'Tristan Rasheed Satria',
        'class': 'PBP C',
        'product_list': product_list,
        'products_by_category': products_by_category,
    }

    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)

def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    # Increment views each time the detail page is accessed
    if hasattr(product, 'increment_views'):
        product.increment_views()

    context = {
        'product': product
    }
    return render(request, "product_detail.html", context)


def show_xml():
     product_list = Product.objects.all()
     xml_data = serializers.serialize("xml", product_list)
     return HttpResponse(xml_data, content_type="application/xml")

def show_json():
    product_list = Product.objects.all()
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(product_id):
   try:
       product_item = Product.objects.filter(pk=product_id)
       xml_data = serializers.serialize("xml", product_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except Product.DoesNotExist:
       return HttpResponse(status=404)

def show_json_by_id(product_id):
   try:
       product_item = Product.objects.get(pk=product_id)
       json_data = serializers.serialize("json", [product_item])
       return HttpResponse(json_data, content_type="application/json")
   except Product.DoesNotExist:
       return HttpResponse(status=404)
       return HttpResponse(status=404)