from audioop import reverse

from django.shortcuts import render, get_object_or_404, redirect
from Webtote.models import Product, ProductImage, ProductCategory, ReviewProduct, OrderDetail, CartItems


def product_list(request, category_id=None):
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    selected_colors = request.GET.getlist('color')
    category_name = "Danh sách sản phẩm"
    category = None
    if category_id:
        category = get_object_or_404(ProductCategory, id=category_id)
        products = products.filter(Category=category)
        category_name = f"Danh mục sản phẩm: {category.Category_Name}"

    if price_min:
        try:
            price_min = int(price_min.replace('.', ''))
            products = products.filter(Unit_Price__gte=price_min)
        except ValueError:
            price_min = None

    if price_max:
        try:
            price_max = int(price_max.replace('.', ''))
            products = products.filter(Unit_Price__lte=price_max)
        except ValueError:
            price_max = None

    if selected_colors:
        products = products.filter(Color__in=selected_colors)

    for product in products:
        product.primary_image = product.productimage_set.filter(Is_Primary=True).first()

    colors = products.values_list('Color', flat=True).distinct()

    context = {
        'products': products,
        'categories': categories,
        'colors': colors,
        'selected_colors': selected_colors,
        'price_min': price_min if price_min else '',
        'price_max': price_max if price_max else '',
        'category': category,
        'category_name': category_name,
    }
    return render(request, 'product.html', context)


def search_products(request):
    search = request.GET.get('search')
    if search:
        products = Product.objects.filter(Product_Name__icontains=search)
    else:
        products = Product.objects.all()
    for product in products:
        product.primary_image = product.productimage_set.filter(Is_Primary=1).first()
    context = {'products': products,'search':search}
    return render(request, 'search.html', context)

def extract_description(content):
    if "THÔNG TIN SẢN PHẨM" in content:
        return content.split("THÔNG TIN SẢN PHẨM")[0].strip()
    elif "THÔNG SỐ SẢN PHẨM" in content:
        return content.split("THÔNG SỐ SẢN PHẨM")[0].strip()
    return content.strip()

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = ProductImage.objects.filter(Product_id=product.id)
    reviews = ReviewProduct.objects.filter(Order_Detail__Product=product).order_by('-Date_Created')
    primary_image = images.filter(Is_Primary=1).first()
    additional_images = images.exclude(Is_Primary=1)
    description = extract_description(product.Description)
    similar_products = Product.objects.filter(Category=product.Category).exclude(id=product.id)[:5]
    for similar_product in similar_products:
        similar_product.primary_image = ProductImage.objects.filter(Product_id=similar_product.id, Is_Primary=1).first()
    context = {
        'product': product,
        'primary_image': primary_image,
        'additional_images': additional_images,
        'description': description,
        'reviews':reviews,
        'similar_products':similar_products,
    }
    return render(request, 'product_detail.html', context)

def add_to_cart(request, product_id):
    return redirect('product_detail', product_id=product_id)

def checkout(request):
    return render(request, 'checkout.html')


from django.contrib.auth.decorators import login_required


@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    # Create cart item
    cart_item = CartItems.objects.create(
        User=request.user,
        Product=product,
        Quantity=quantity,
        Subtotal=product.Unit_Price * quantity
    )
    return redirect('checkout')