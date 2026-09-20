from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Product, Category, Supplier
import json

# Create your views here.
@csrf_exempt
def product_list(request):

    if request.method =='GET':
        products = Product.objects.all()

        data = []

        for product in products:
            data.append({
                'id': product.id,
                'name': product.name,
                'stock': product.stock,
                'price': product.price,
                'location': product.location,
                'category': product.category.name,
                'supplier': product.supplier.name,
            })
        return JsonResponse(data, safe=False)
    
    if request.method == 'POST':
        try: 
            data = json.loads(request.body) 
            category = Category.objects.get(id=data['category'])
            supplier = Supplier.objects.get(id=data['supplier'])

            product = Product.objects.create( 
                name=data['name'], 
                stock=data['stock'], 
                price=data['price'], 
                location=data['location'],
                category=category,
                supplier=supplier
            ) 
 
            return JsonResponse({ 
                'message': 'Product created successfully', 
                'id': product.id 
            }, status=201)  
 
        except KeyError as e: 
            return JsonResponse({ 
                'error': f'Missing field: {e.args[0]}' 
            }, status=400)

        except Category.DoesNotExist:
            return JsonResponse({
                'error': 'Category not found'
            }, status=404)

        except Supplier.DoesNotExist:
            return JsonResponse({
                'error': 'Supplier not found'
            }, status=404)
    
    if request.method == 'PUT':
        try:
            body = json.loads(request.body)

            category = Category.objects.get(id=body['category'])
            supplier = Supplier.objects.get(id=body['supplier'])

            product = Product.objects.get(id=body['id'])

            product.name = body['name']
            product.stock = body['stock']
            product.price = body['price']
            product.location = body['location']
            product.category = category
            product.supplier = supplier

            product.save()

            return JsonResponse({
                'message': 'Product updated successfully'
            })

        except KeyError as e:
            return JsonResponse({
                'error': f'Missing field: {e.args[0]}'
            }, status=400)

        except Product.DoesNotExist:
            return JsonResponse({
                'error': 'Product not found'
            }, status=404)
        
        except Category.DoesNotExist:
            return JsonResponse({
                'error': 'Category not found'
            }, status=404)

        except Supplier.DoesNotExist:
            return JsonResponse({
                'error': 'Supplier not found'
            }, status=404)

    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)

            product = Product.objects.get(id=data['id'])

            if 'name' in data:
                product.name = data['name']

            if 'stock' in data:
                product.stock = data['stock']

            if 'price' in data:
                product.price = data['price']

            if 'location' in data:
                product.location = data['location']
            
            if 'category' in data:
                category = Category.objects.get(id=data['category'])
                product.category = category
            
            if 'supplier' in data:
                supplier = Supplier.objects.get(id=data['supplier'])
                product.supplier = supplier

            product.save()

            return JsonResponse({
                'message': 'Product updated successfully'
            })

        except KeyError as e:
            return JsonResponse({
                'error': f'Missing field: {e.args[0]}'
            }, status=400)

        except Product.DoesNotExist:
            return JsonResponse({
                'error': 'Product not found'
            }, status=404)

        except Category.DoesNotExist:
            return JsonResponse({
            'error': 'Category not found'
            }, status=404)

        except Supplier.DoesNotExist:
            return JsonResponse({
                'error': 'Supplier not found'
            }, status=404)

    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)

            product = Product.objects.get(id=data['id'])
            product.delete()


            return JsonResponse({
                'message': 'Product deleted successfully'
            })
        except Product.DoesNotExist:
            return JsonResponse({
                'error': 'Product not found'
            }, status=404)

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
        'location': product.location,
        'category': product.category.name,
        'supplier': product.supplier.name,
    })

def low_stock_products(request):
    products = Product.objects.filter(stock__lt=5)

    data = []

    for product in products:
        data.append({
            'id': product.id,
            'name': product.name,
            'stock': product.stock,
            'price': product.price,
            'location': product.location,
        })

    return JsonResponse(data, safe=False)

def product_page(request):
    products = Product.objects.all()

    return render(request, 'product_list.html', {'products': products})

def home(request):
    return redirect('/product-page/')

def category_list(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return JsonResponse({
            'error': 'Category Not Found'
        }, status=404)
    
    products = category.product_set.all()

    data = []

    for product in products:
        data.append({
            'id': product.id,
            'name': product.name,
            'stock': product.stock,
            'price': product.price,
            'location': product.location,
            'supplier': product.supplier.name,
        })
    return JsonResponse(data, safe=False)

def supplier_list(request, id):
    try:
        supplier = Supplier.objects.get(id=id)
    except Supplier.DoesNotExist:
        return JsonResponse({
            'error': 'Supplier Not Found'
        }, status=404)
    
    products = supplier.product_set.all()

    data = []

    for product in products:
        data.append({
            'id': product.id,
            'name': product.name,
            'stock': product.stock,
            'price': product.price,
            'location': product.location,
            'category': product.category.name,
        })
    return JsonResponse(data, safe=False)

def category_counts(request):
    categories = Category.objects.all()

    data = []

    for category in categories:
        data.append({
            'id': category.id,
            'name': category.name,
            'product_count': category.product_set.count()
        })

    return JsonResponse(data, safe=False)

def supplier_counts(request):
    suppliers = Supplier.objects.all()

    data = []

    for supplier in suppliers:
        data.append({
            'id': supplier.id,
            'name': supplier.name,
            'product_count': supplier.product_set.count()
        })

    return JsonResponse(data, safe=False)