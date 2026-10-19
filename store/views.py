from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from .cart import get_cart, merge_session_cart_into_user
from .forms import CheckoutForm, ProfileForm, ReviewForm, SignUpForm
from .models import Brand, Category, CartItem, Order, OrderItem, Product, Profile, Review, Wishlist


PAGE_SIZE = 12


def home(request):
    featured = Product.objects.filter(is_active=True, is_featured=True).select_related('category', 'brand')[:8]
    new_arrivals = Product.objects.filter(is_active=True).select_related('category', 'brand').order_by('-created_at')[:8]
    consoles = Product.objects.filter(is_active=True, category__slug='consoles').select_related('brand')[:6]
    categories = Category.objects.all()
    context = {
        'featured': featured,
        'new_arrivals': new_arrivals,
        'consoles': consoles,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)


def product_list(request, category_slug=None):
    products = Product.objects.filter(is_active=True).select_related('category', 'brand')
    categories = Category.objects.all()
    brands = Brand.objects.all()

    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(brand__name__icontains=query)
        )

    brand_ids = request.GET.getlist('brand')
    if brand_ids:
        products = products.filter(brand_id__in=brand_ids)

    platform = request.GET.get('platform')
    if platform:
        products = products.filter(platform=platform)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    in_stock_only = request.GET.get('in_stock')
    if in_stock_only:
        products = products.filter(stock__gt=0)

    sort = request.GET.get('sort', 'newest')
    sort_map = {
        'newest': '-created_at',
        'price_low': 'price',
        'price_high': '-price',
        'name': 'name',
    }
    products = products.order_by(sort_map.get(sort, '-created_at'))

    paginator = Paginator(products, PAGE_SIZE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'categories': categories,
        'brands': brands,
        'current_category': current_category,
        'query': query,
        'selected_brands': [int(b) for b in brand_ids if b.isdigit()],
        'selected_platform': platform,
        'sort': sort,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'in_stock_only': in_stock_only,
        'platform_choices': Product.Platform.choices,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category', 'brand').prefetch_related('extra_images', 'reviews__user'),
        slug=slug, is_active=True,
    )
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]

    review_form = ReviewForm()
    user_has_reviewed = False
    in_wishlist = False
    if request.user.is_authenticated:
        user_has_reviewed = product.reviews.filter(user=request.user).exists()
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.info(request, 'Please log in to leave a review.')
            return redirect('store:login')
        if user_has_reviewed:
            messages.warning(request, "You've already reviewed this product.")
            return redirect(product.get_absolute_url())
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Thanks for your review!')
            return redirect(product.get_absolute_url())

    context = {
        'product': product,
        'related_products': related_products,
        'review_form': review_form,
        'user_has_reviewed': user_has_reviewed,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'store/product_detail.html', context)


# ---------- Cart ----------

def cart_detail(request):
    cart = get_cart(request, create=False)
    return render(request, 'store/cart.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = get_cart(request, create=True)
    quantity = int(request.POST.get('quantity', 1) or 1)
    quantity = max(1, quantity)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
    if not created:
        item.quantity += quantity
        item.save()

    messages.success(request, f'"{product.name}" added to your cart.')
    next_url = request.POST.get('next') or product.get_absolute_url()
    return redirect(next_url)


@require_POST
def cart_update(request, item_id):
    cart = get_cart(request, create=False)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    quantity = int(request.POST.get('quantity', 1) or 1)
    if quantity <= 0:
        item.delete()
        messages.info(request, 'Item removed from cart.')
    else:
        item.quantity = quantity
        item.save()
        messages.success(request, 'Cart updated.')
    return redirect('store:cart_detail')


@require_POST
def cart_remove(request, item_id):
    cart = get_cart(request, create=False)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    item.delete()
    messages.info(request, 'Item removed from cart.')
    return redirect('store:cart_detail')


# ---------- Wishlist ----------

@login_required
def wishlist_detail(request):
    items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'store/wishlist.html', {'items': items})


@login_required
@require_POST
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.delete()
        messages.info(request, f'Removed "{product.name}" from your wishlist.')
    else:
        messages.success(request, f'Added "{product.name}" to your wishlist.')
    next_url = request.POST.get('next') or product.get_absolute_url()
    return redirect(next_url)


# ---------- Checkout / Orders ----------

@login_required
def checkout(request):
    cart = get_cart(request, create=False)
    if not cart or cart.items.count() == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:product_list')

    initial = {'full_name': request.user.get_full_name() or request.user.username, 'email': request.user.email}
    profile = getattr(request.user, 'profile', None)
    if profile:
        initial.update({
            'phone': profile.phone, 'address': profile.address, 'city': profile.city,
            'postal_code': profile.postal_code, 'country': profile.country,
        })

    if request.method == 'POST':
        form = CheckoutForm(request.POST, initial=initial)
        if form.is_valid():
            for item in cart.items.select_related('product'):
                if item.quantity > item.product.stock:
                    messages.error(request, f'Not enough stock for "{item.product.name}". Only {item.product.stock} left.')
                    return redirect('store:cart_detail')

            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = cart.subtotal
            order.save()

            for item in cart.items.select_related('product'):
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    price=item.product.discounted_price,
                    quantity=item.quantity,
                )
                item.product.stock = max(0, item.product.stock - item.quantity)
                item.product.save(update_fields=['stock'])

            cart.items.all().delete()
            messages.success(request, f'Order #{order.pk} placed successfully!')
            return redirect('store:order_success', order_id=order.pk)
    else:
        form = CheckoutForm(initial=initial)

    return render(request, 'store/checkout.html', {'form': form, 'cart': cart})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'store/order_success.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'store/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related('items'), pk=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


# ---------- Auth ----------

def signup(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            merge_session_cart_into_user(request, user)
            messages.success(request, f'Welcome to GameHub, {user.first_name or user.username}!')
            return redirect('store:home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


class LoginView(DjangoLoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        merge_session_cart_into_user(self.request, self.request.user)
        return response


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('store:home')


@login_required
def profile_view(request):
    profile, _created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('store:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'store/profile.html', {'form': form})
