from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from django.core import serializers

import json
from .models import *

# Create your views here.
# The progress: Product->Cart Item->C
@csrf_exempt
def product(request):
    if request.method == "GET":
        result = []
        all_products = Product.objects.all()
        for product in all_products: 
            product_info = {
                "id": product.id,
                "from_user": product.from_user.profile.full_name, 
                "name" : product.name,
                "category": product.category,
                "description": product.description,
                "price": product.price,
                "stock_quantity": product.stock_quantity,
            }
            result.append(product_info)
        return JsonResponse(result, safe = False , status = 402)
    else:
        return HttpResponse({"Product"}, status = 402)




@csrf_exempt
def own_product(request):
    if not request.user.is_authenticated:
            return JsonResponse(
                {"status": "Unauthenticated"},
                status=400
            )   
    if request.method == "GET":
        user = CustomUser.objects.get(id = request.user.id)
        if Product.objects.filter(from_user = user).exists():
            own_products = Product.objects.filter(from_user = user)
        else:
            return JsonResponse({"status": "You have not sell anything"}, status = 402)
        result = []
        for product in own_products:
            product_info = {
                "id": product.id,
                "from_user": product.from_user.profile.full_name, 
                "name" : product.name,
                "category": product.category,
                "description": product.description,
                "price": product.price,
                "stock_quantity": product.stock_quantity,
            }
            result.append(product_info)
        return JsonResponse(result, safe=False , status = 200)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse(
                {"status": "Unauthenticated"},
                status=400
            )   
        data = json.loads(request.body)
        user = CustomUser.objects.get(id = request.user.id)
        name = data.get("name")
        category = data.get("category")
        description = data.get("description")
        price = data.get("price")
        stock_quantity = data.get("stock_quantity")
        new_product = Product.objects.create(from_user = user, name = name , category = category , description = description , price = price, stock_quantity = stock_quantity)
        new_product.save()
        return JsonResponse({"status" : "Save successfully"}, status = 402)
    
    elif request.method == "PUT":
        if not request.user.is_authenticated:
            return JsonResponse(
                {"status": "Unauthenticated"},
                status=400
            )
        data = json.loads(request.body)
        id = data.get("id")
        current_user = CustomUser.objects.get(id = request.user.id)

        
        try: 
            fix_product = Product.objects.get(id= id)
            if fix_product.from_user == current_user:
                fix_product.name = name = data.get("name")
                fix_product.category = data.get("category")
                fix_product.description = data.get("description")
                fix_product.price = data.get("price")
                fix_product.stock_quantity = data.get("stock_quantity")
                fix_product.save()
                return JsonResponse({"status": "Updated successfully"}, status=200)
            else:
                return JsonResponse({"status": "You can no modify this products"}, status = 402)
        except Product.DoesNotExist:
            return JsonResponse({"status": "Not found the updated products"}, status = 402)
    
    elif request.method == "DELETE":
        if not request.user.is_authenticated:
            return JsonResponse(
                {"status": "Unauthenticated"},
                status=400
            )
        id = json.loads(request.body).get("id")
        current_user = CustomUser.objects.get(id = request.user.id)

        try:
            product = Product.objects.get(id = id)
            if product.from_user == current_user:
                product.delete()
                return JsonResponse({"status": "Product deleted successfully"}, status=200)
            else:
                return JsonResponse({"status": "You can not delete this one"}, status = 402)
            
        except Product.DoesNotExist:
            return JsonResponse({"status": "Product not found for deletion"}, status=404)
    else:
        return HttpResponse({"Own Product ManageMent"}, status = 402)
    
       
csrf_exempt
def searchProduct(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "Unauthenticated"},
            status=400
        )
    products = Product.objects.all()
    query = json.loads(request.body)
    name = query.get(name)
    result = products.filter(name = name)
    serialized_result = [{"name": product.name, "description" : product.description, "price": product.price, "stock_quantity": product.stock_quantity} for product in result]
    return JsonResponse({"status": "Success", "result": serialized_result})


@csrf_exempt
def shopping(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "Unauthenticated"}, status = 402)
    
    if request.method == "GET":
        user =  CustomUser.objects.get(id = request.user.id)
        all_shopping = Product.objects.exclude(from_user=user)
        result = []
        for product in all_shopping:
            product_info = {
                "id": product.id,
                "from_user": product.from_user.profile.full_name, 
                "name" : product.name,
                "category": product.category,
                "description": product.description,
                "price": product.price,
                "stock_quantity": product.stock_quantity,
            }
            result.append(product_info)
        return JsonResponse(result, safe=False , status = 200)
    else:
        return HttpResponse({"Shopping"}, status = 402)


        

'''
Putting the customer products to your cart
'''




@csrf_exempt
def shoppingCart(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "Unauthenticated"},
            status=400
        )
    if request.method == "GET":
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        
        # Ensure that the user has a shopping cart
        if not ShoppingCart.objects.filter(user=user).exists():
            ShoppingCart.objects.create(user=user)
        
        # Retrieve the user's shopping cart
        user_cart = ShoppingCart.objects.get(user=user)
        
        # Initialize an empty list to store cart item information
        result = []
        
        # Iterate over each cart item in the user's cart
        for cart_item in user_cart.cart_items.all():
            each_cart_info = {
                "id": cart_item.product.id,
                "from_user": cart_item.product.from_user.profile.full_name,
                "name": cart_item.product.name,
                "description": cart_item.product.description,
                "price": cart_item.product.price,
                "stock_quantity": cart_item.product.stock_quantity,  # Access cart item's product's stock quantity
                "quantity": cart_item.quantity,
            } 
            result.append(each_cart_info)
        
        # Return the cart item information as JSON response
        return JsonResponse(result, safe=False, status=202)
    
    elif request.method == "POST":
        cart_data = json.loads(request.body)
        stock_quantity = cart_data.get("quantity")
        product_id = cart_data.get('id')
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"status": "No product found"}, status=402)

        if product.from_user == user:
            return JsonResponse({"status": "Cannot cart this product"}, status=402)

        if not ShoppingCart.objects.filter(user=user).exists():
            ShoppingCart.objects.create(user=user)

        cart_user = ShoppingCart.objects.get(user=user)
        new_cart = CartItem.objects.create(product=product, quantity = stock_quantity)
        cart_user.cart_items.add(new_cart)

        # Construct response JSON with updated cart information
        response_data = {
            "status": "Save successfully",
            "cart": [
                {
                    "product_id": item.product.id,
                    "product_name": item.product.name,
                    "quantity": item.quantity
                }
                for item in cart_user.cart_items.all()
            ]
        }
        return JsonResponse(response_data, status=202)
    
    elif request.method == "PUT":
        cart_data = json.loads(request.body)
        new_quantity = cart_data.get("quantity")
        product_id = cart_data.get('id')
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"status": "No product found"}, status=404)

        if product.from_user != user:
            return JsonResponse({"status": "Cannot update quantity for this product"}, status=403)

        try:
            cart_user = ShoppingCart.objects.get(user=user)
            cart_item = cart_user.cart_items.get(product=product)
        except ShoppingCart.DoesNotExist:
            return JsonResponse({"status": "Shopping cart not found"}, status=404)
        except CartItem.DoesNotExist:
            return JsonResponse({"status": "Product not found in the shopping cart"}, status=404)
        
        cart_item.quantity = new_quantity
        cart_item.save()
        return JsonResponse({"status": "Updated successfully"}, status = 200)
    
    elif request.method == "DELETE":
        cart_data = json.loads(request.body)
        product_id = cart_data.get('id')
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"status": "No product found"}, status=404)

        if product.from_user != user:
            return JsonResponse({"status": "Cannot delete for this product"}, status=403)

        try:
            cart_user = ShoppingCart.objects.get(user=user)
            cart_item = cart_user.cart_items.get(product=product)
        except ShoppingCart.DoesNotExist:
            return JsonResponse({"status": "Shopping cart not found"}, status=404)
        except CartItem.DoesNotExist:
            return JsonResponse({"status": "Product not found in the shopping cart"}, status=404)
        
        cart_user.cart_items.remove(cart_item)
        return JsonResponse({"status": "Remove successfully"}, status = 200)
    



def order(request):
    if not request.user.is_authenticated:
        return JsonResponse({"Status": "Unauthenticated"}, status = 402)
    
    if request.method == "GET":
        try: 
            user = CustomUser.objects.get(id = request.user.id)
            own_orders = Order.objects.filter(user = user)

            result = []
            for order in own_orders:
                order_products = order.orders.all()
                orders_list = []
                for order_item in order_products:
                    product = order_item.product  # Access the related product
                    orders_list.append({
                        'from_user': product.from_user.profile.full_name,
                        'name': product.name,
                        'category': product.category,
                        'description': product.description,
                        'price': product.price,
                        'stock_quantity': product.stock_quantity
                    })
                result.append({
                    'user': order.user.profile.full_name,
                    'orders': orders_list,
                    'total_price': order.total_price,
                    'status': order.status,
                })
            return JsonResponse(result, safe=False, status=200)
        except Order.DoesNotExist:
            return JsonResponse({"status": "No orders found"}, status=404)

    else:
        return HttpResponse("Order Management", status=405)
    



        



@csrf_exempt
def make_order_from_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({"Status": "Unthenticated"}, status = 402)
    
    if request.method == "POST":
        # Request body here is a list of product id in the shopping cart
        data = json.loads(request.body)
        product_ids = data.get('product_ids', [])
        current_user = CustomUser.objects.get(id = request.user.id)
        if ShoppingCart.objects.filter(user = current_user).exists():
            shopping_cart = ShoppingCart.objects.get(user = current_user)
        else: 
            shopping_cart = ShoppingCart.objects.create(user = current_user)
        
        
        total_price = 0
        new_order = Order.objects.create(user = current_user, status = "Pending", total_price = 0)

        for product_id in product_ids:
            product =  Product.objects.get(id = product_id)
            
            
            cart_item = CartItem.objects.get(product = product)
            order_item = OrderItem.objects.create(product = product, quantity = cart_item.quantity)
            
            new_order.orders.add(order_item)
            total_price += cart_item.quantity * cart_item.product.price
            product.stock_quantity -= cart_item.quantity
            product.save()
            if product.stock_quantity == 0:
                product.delete()
            
            cart_item.delete()
        new_order.total_price = total_price
        new_order.status = "Delivering"
        if new_order.orders != []:
            new_order.save()
            return JsonResponse({"Status": "Order created successfully", "Order ID": new_order.id}, status=201)
        else:
            return JsonResponse({"status": "Can not buy it"})
    else:
        return HttpResponse({"make_order"}, status = 402)
    





    






        