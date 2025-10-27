from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .form import SignUpForm, LoginForm, ReviewForm, UserUpdateForm, ProfileUpdateForm
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Review, Favorite
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def mainpage(request):
    return render(request, 'mainpage.html')

def products(request, category_id=None):
    categories = Category.objects.all()
    if category_id:
        products = Product.objects.filter(category__id=category_id)
    else:
        products = Product.objects.all()
    return render(request, 'products.html', {'categories': categories, 'products': products, 'selected_category_id': category_id})


def productdetail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).order_by('-created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('authorization')

        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            if Review.objects.filter(product=product, user=request.user).exists():
                messages.error(request, "Вы уже оставили отзыв на этот продукт.")
            else:
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, "Ваш отзыв успешно добавлен!")
            return redirect('productdetail', product_id=product.id)
    else:
        form = ReviewForm()

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()

    is_in_cart = False
    if request.user.is_authenticated:
        cart = _get_or_create_cart(request)
        is_in_cart = cart.cart_items.filter(product=product).exists()

    return render(
        request,
        'product-detail.html',
        {
            'product': product,
            'reviews': reviews,
            'review_form': form,
            'is_favorite': is_favorite,
            'is_in_cart': is_in_cart,
        }
    )

def longread(request):
    return render(request, 'longread.html')

def support(request):
    return render(request, 'support.html')

def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('mainpage')
    else:
        form = SignUpForm()
    return render(request, 'registration.html', {'form': form})

def authorization(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('mainpage')
    return render(request, 'authorization.html', {'form': form})

def _get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(id=session_key)
    return cart


def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = _get_or_create_cart(request)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            return JsonResponse({
                "status": "updated",
                "quantity": cart_item.quantity
            })
        else:
            return JsonResponse({
                "status": "added",
                "quantity": cart_item.quantity
            })

    return JsonResponse({"error": "Invalid request"}, status=400)

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = _get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        cart_item.delete()
        return redirect('cart')
    return redirect('cart')

def update_cart_quantity(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = _get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity -= 1

        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()
        return redirect('cart')
    return redirect('cart')

def cart(request):
    cart = _get_or_create_cart(request)
    cart_items = cart.cart_items.all()
    total_price = cart.get_total_price
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def create_order(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        cart = _get_or_create_cart(request)
        if not cart.cart_items.exists():
            return JsonResponse({'error': 'Cart is empty'}, status=400)

        import json
        try:
            data = json.loads(request.body)
            address = data.get('address', '')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        order = Order.objects.create(
            user=request.user,
            total_price=cart.get_total_price,
            address=address,
            status='pending'
        )

        for item in cart.cart_items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart.cart_items.all().delete()
        return JsonResponse({'success': 'Order created successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('authorization')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_edit')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'profile_edit.html', context)

@login_required
def toggle_favorite(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
        
        if not created:
            favorite.delete()
            return JsonResponse({'status': 'removed', 'message': 'Продукт удален из избранного.'})
        else:
            return JsonResponse({'status': 'added', 'message': 'Продукт добавлен в избранное.'})
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites.html', {'favorites': favorites})

def profil(request):
    return render(request, 'profil.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('mainpage')