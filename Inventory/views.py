from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Product, Category, Supplier
import json

# Create your views here.
@csrf_exempt
def product_list(request):
    user = get_authenticated_user(request)

    if user is None:
        return JsonResponse({
            'error': 'Authentication required'
        }, status=401)

    if request.method == 'GET':
        if not has_permission(user, 'Inventory.view_product'):
            return JsonResponse({
                'error': 'You do not have permission to view products'
            }, status=403)

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
                'created_by': product.created_by.username,
            })
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        if not has_permission(user, 'Inventory.add_product'):
            return JsonResponse({
                'error': 'You do not have permission to create products'
            }, status=403)

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
                supplier=supplier,
                created_by=user
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
        if not has_permission(user, 'Inventory.change_product'):
            return JsonResponse({
                'error': 'You do not have permission to update products'
            }, status=403)

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
        if not has_permission(user, 'Inventory.change_product'):
            return JsonResponse({
                'error': 'You do not have permission to update products'
            }, status=403)

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
        if not has_permission(user, 'Inventory.delete_product'):
            return JsonResponse({
                'error': 'You do not have permission to delete products'
            }, status=403)

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
    user = get_authenticated_user(request)

    if user is None:
        return JsonResponse({
            'error': 'Authentication required'
        }, status=401)

    if not has_permission(user, 'Inventory.view_product'):
        return JsonResponse({
            'error': 'You do not have permission to view products'
        }, status=403)

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
        'created_by': product.created_by.username,
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

@csrf_exempt
def signup(request):
    details = json.loads(request.body)

    try:
        username = details['username']
        password = details['password']
    except KeyError:
        return JsonResponse({
            'error': 'Username and password are required'
        }, status=400)

    try:
        user = User.objects.create_user(
            username=username,
            password=password
        )
    except IntegrityError:
        return JsonResponse({
            'error': 'Username already exists'
        }, status=400)

    return JsonResponse({
        'message': 'User Created Successfully',
    }, status=201)

@csrf_exempt
def login(request):
    details = json.loads(request.body)

    try:
        username = details['username']
        password = details['password']
    except KeyError:
        return JsonResponse({
            'error': 'Username and password are required'
        }, status=400)
    
    user = authenticate(
        username=username,
        password=password
    )
    if user is None:
        return JsonResponse({
            'error': 'Invalid username or password'
        }, status=401)
    
    token, created = Token.objects.get_or_create(user=user)
    return JsonResponse({
        'message': 'Login successful',
        'token': token.key
    }, status=200)

@csrf_exempt
def logout(request):
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return JsonResponse({
            'error': 'Authorization token is required'
        }, status=401)

    parts = auth_header.split()

    if len(parts)!=2 or parts[0]!= 'Token':
        return JsonResponse({
            'error': 'Invalid authorization header'
        }, status=401)
    
    token_key = parts[1]

    try:
        token = Token.objects.get(key=token_key)
    except Token.DoesNotExist:
        return JsonResponse({
            'error': 'Invalid or expired token'
        }, status=401)
    
    token.delete()

    return JsonResponse({
        'message': 'Logout successfull'
    }, status=200)

def get_authenticated_user(request):
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return None
    
    parts = auth_header.split()

    if len(parts)!=2 or parts[0]!= 'Token':
        return None
    
    token_key = parts[1]

    try:
        token = Token.objects.get(key=token_key)
    except Token.DoesNotExist:
        return None
    
    return token.user

def has_permission(user, permission):
    return user.has_perm(permission)
