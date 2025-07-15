from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Category, Product, Cart, CartItem, Order, OrderItem
import json


def home(request):
    """Главная страница с рекомендуемыми товарами"""
    featured_products = Product.objects.filter(featured=True)[:8]
    categories = Category.objects.all()[:6]
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)


def product_list(request):
    """Список всех товаров с фильтрацией и поиском"""
    products = Product.objects.all()
    categories = Category.objects.all()
    
    # Фильтрация по категории
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Фильтрация по наличию
    availability = request.GET.get('availability')
    if availability:
        products = products.filter(availability=availability)
    
    # Сортировка
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')
    
    # Пагинация
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
        'current_availability': availability,
        'current_sort': sort_by,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    """Детальная страница товара"""
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def category_detail(request, slug):
    """Страница категории"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    
    # Пагинация
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'store/category_detail.html', context)


def get_or_create_cart(request):
    """Получить или создать корзину для пользователя"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_view(request):
    """Просмотр корзины"""
    cart = get_or_create_cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'store/cart.html', context)


@csrf_exempt
def add_to_cart(request):
    """Добавить товар в корзину (AJAX)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
            
            product = get_object_or_404(Product, id=product_id)
            cart = get_or_create_cart(request)
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return JsonResponse({
                'success': True,
                'message': f'{product.name} добавлен в корзину',
                'cart_total_items': cart.total_items,
                'cart_total_price': float(cart.total_price)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Ошибка при добавлении товара в корзину'
            })
    
    return JsonResponse({'success': False, 'message': 'Неверный запрос'})


@csrf_exempt
def update_cart_item(request):
    """Обновить количество товара в корзине (AJAX)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            quantity = int(data.get('quantity'))
            
            cart = get_or_create_cart(request)
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
            
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
            
            return JsonResponse({
                'success': True,
                'cart_total_items': cart.total_items,
                'cart_total_price': float(cart.total_price),
                'item_total': float(cart_item.total_price) if quantity > 0 else 0
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Ошибка при обновлении корзины'
            })
    
    return JsonResponse({'success': False, 'message': 'Неверный запрос'})


def remove_from_cart(request, item_id):
    """Удалить товар из корзины"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()
    
    messages.success(request, f'{product_name} удалён из корзины')
    return redirect('store:cart')


def checkout(request):
    """Оформление заказа"""
    cart = get_or_create_cart(request)
    
    if not cart.items.exists():
        messages.warning(request, 'Ваша корзина пуста')
        return redirect('store:cart')
    
    if request.method == 'POST':
        # Создание заказа
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            total_amount=cart.total_price
        )
        
        # Создание элементов заказа
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
        
        # Очистка корзины
        cart.items.all().delete()
        
        messages.success(request, f'Заказ #{order.id} успешно оформлен!')
        return redirect('store:order_success', order_id=order.id)
    
    context = {
        'cart': cart,
    }
    return render(request, 'store/checkout.html', context)


def order_success(request, order_id):
    """Страница успешного оформления заказа"""
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'store/order_success.html', context)
