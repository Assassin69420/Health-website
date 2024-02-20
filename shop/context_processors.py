from .models import Cart, CartItem

def cart_item_count(request):
    cart_item_count = 0

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            cart_item_count = sum(item.quantity for item in cart_items)
        except Cart.DoesNotExist:
            pass

    return {'cart_item_count': cart_item_count}

