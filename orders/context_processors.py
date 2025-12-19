from .models import Cart


def cart(request):
    """Provide cart and cart_count to all templates.

    - For authenticated users, get or create the Cart and count items.
    - For anonymous users, return None/0 (can be extended to use session later).
    """
    cart_obj = None
    count = 0
    try:
        if request.user.is_authenticated:
            cart_obj, _ = Cart.objects.get_or_create(user=request.user)
            count = cart_obj.items.count()
    except Exception:
        # Fail silently to avoid breaking templates if DB unavailable
        cart_obj = None
        count = 0

    return {
        'cart': cart_obj,
        'cart_count': count,
    }
