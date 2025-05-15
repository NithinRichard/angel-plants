from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from decimal import Decimal
from .models import Product, Cart, CartItem

@login_required
def add_to_cart(request, product_id, quantity=1):
    """
    Add a product to the cart or update quantity if already in cart.
    """
    try:
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # Get or create cart for the current user
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            defaults={'status': 'active'}
        )
        
        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 0, 'price': product.price}
        )
        
        # Increase quantity
        cart_item.increase_quantity(quantity)
        
        # Prepare response data
        response_data = {
            'status': 'success',
            'message': f"{product.name} added to cart",
            'cart': {
                'item_count': cart.item_count,
                'total': str(cart.total),
            },
            'added_item': {
                'product_id': product.id,
                'name': product.name,
                'quantity': cart_item.quantity,
                'price': str(product.price),
                'subtotal': str(cart_item.total_price)
            }
        }
        
        # Set success message
        messages.success(request, f"{product.name} has been added to your cart.")
        
        # If it's an AJAX request, return JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(response_data)
            
        # For regular form submission, redirect to cart or previous page
        redirect_url = request.META.get('HTTP_REFERER', reverse('cart'))
        return redirect(redirect_url)
        
    except Product.DoesNotExist:
        error_msg = 'Product not found.'
    except Exception as e:
        error_msg = f'An error occurred: {str(e)}'
    
    # Handle errors
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'error', 'message': error_msg}, status=400)
    
    messages.error(request, error_msg)
    return redirect('store:home')

@login_required
def update_cart(request):
    """
    Update cart item quantities.
    Expected POST data: {'product_id': quantity, ...}
    """
    if request.method == 'POST':
        try:
            # Get the user's cart
            cart = Cart.objects.get(user=request.user, status='active')
            
            # Process each item in the request
            for product_id, quantity in request.POST.items():
                if product_id.isdigit():
                    try:
                        cart_item = CartItem.objects.get(
                            cart=cart,
                            product_id=product_id
                        )
                        # Update quantity
                        cart_item.quantity = int(quantity)
                        cart_item.save()
                        
                        # If quantity is 0 or negative, remove the item
                        if cart_item.quantity <= 0:
                            cart_item.delete()
                            
                    except (CartItem.DoesNotExist, ValueError):
                        continue
            
            # Prepare success response
            response_data = {
                'status': 'success',
                'message': 'Cart updated',
                'cart': {
                    'item_count': cart.item_count,
                    'total': str(cart.total),
                }
            }
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data)
                
            messages.success(request, 'Your cart has been updated.')
            return redirect('cart')
            
        except Cart.DoesNotExist:
            error_msg = 'No active cart found.'
        except Exception as e:
            error_msg = f'An error occurred: {str(e)}'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': error_msg}, status=400)
            
        messages.error(request, error_msg)
        return redirect('cart')
    
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    """
    Remove a product from the cart or decrease its quantity.
    """
    try:
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # Get the user's cart
        cart = get_object_or_404(Cart, user=request.user, status='active')
        
        # Get the cart item
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            
            # Remove the item from the cart
            cart_item.delete()
            
            # Prepare success response
            response_data = {
                'status': 'success',
                'message': f"{product.name} removed from cart",
                'cart': {
                    'item_count': cart.item_count,
                    'total': str(cart.total),
                },
                'removed_item': {
                    'product_id': product.id,
                    'name': product.name,
                    'quantity': 0,
                    'price': str(product.price),
                    'subtotal': '0.00'
                }
            }
            
            # Set success message
            messages.success(request, f"{product.name} has been removed from your cart.")
            
        except CartItem.DoesNotExist:
            # Item not in cart
            response_data = {
                'status': 'error',
                'message': 'Item not found in cart',
            }
            messages.error(request, 'Item not found in your cart.')
        
        # If it's an AJAX request, return JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(response_data)
            
        # For regular form submission, redirect to cart or previous page
        redirect_url = request.META.get('HTTP_REFERER', reverse('cart'))
        return redirect(redirect_url)
        
    except Product.DoesNotExist:
        error_msg = 'Product not found.'
    except Cart.DoesNotExist:
        error_msg = 'No active cart found.'
    except Exception as e:
        error_msg = f'An error occurred: {str(e)}'
    
    # Handle errors
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'error', 'message': error_msg}, status=400)
    
    messages.error(request, error_msg)
    return redirect('cart')
