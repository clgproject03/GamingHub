from .cart import get_cart
from .models import Category, Wishlist


def cart_context(request):
    cart = get_cart(request, create=False)
    count = cart.total_items if cart else 0
    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
    return {
        'nav_cart_count': count,
        'nav_categories': Category.objects.all(),
        'user_wishlist_ids': wishlist_ids,
    }
