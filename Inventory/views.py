from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Product
import json

# Create your views here.
@csrf_exempt
def product_list(request):
    products = Product.objects.all()

    data = []

    for product in products:
        data.append({
            'id': product.id,
            'name': product.name,
            'stock': product.stock,
            'price': product.price,
            'location': product.location,
        })

    if request.method =='GET':
        return JsonResponse(data, safe=False)
    
    if request.method == 'POST':
        body = json.loads(request.body)

        Product.objects.create(
            name=body['name'],
            stock=body['stock'],
            price=body['price'],
            location=body['location']
        )
        return JsonResponse({'status': 'Product created'}, safe=False)
    
    if request.method == 'PATCH':
        body = json.loads(request.body)

        product = Product.objects.get(id=body['id'])

        if 'name' in body:
            product.name = body['name']

        if 'stock' in body:
            product.stock = body['stock']

        if 'price' in body:
            product.price = body['price']

        if 'location' in body:
            product.location = body['location']

        product.save()
        return JsonResponse({'status': 'Product updated'}, safe=False)

    if request.method == 'DELETE':
        body = json.loads(request.body)
        product = Product.objects.get(id=body['id'])
        product.delete()
        return JsonResponse({'status': 'Product deleted'}, safe=False)

def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return JsonResponse({
            'error': 'Product not found'
        }, status=404)
    return JsonResponse({
        'id': product.id,
        'name': product.name,
        'stock': product.stock,
        'price': product.price,
        'location': product.location
    })

