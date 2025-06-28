from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db
from models import Category, Product, CartItem, Order, OrderItem, BlogPost, GalleryImage, Newsletter
import uuid
import json
from datetime import datetime
from utils import get_cart_items, calculate_cart_total, send_order_confirmation_email

@app.route('/')
def index():
    """Home page with featured products and categories"""
    categories = Category.query.all()
    featured_products = Product.query.filter_by(is_featured=True).limit(8).all()
    new_arrivals = Product.query.filter_by(is_new_arrival=True).limit(6).all()
    gallery_images = GalleryImage.query.filter_by(is_featured=True).limit(6).all()
    
    return render_template('index.html', 
                         categories=categories,
                         featured_products=featured_products,
                         new_arrivals=new_arrivals,
                         gallery_images=gallery_images)

@app.route('/products')
@app.route('/products/<category_slug>')
def products(category_slug=None):
    """Products listing page with category filtering"""
    categories = Category.query.all()
    
    if category_slug:
        category = Category.query.filter_by(slug=category_slug).first_or_404()
        products_query = Product.query.filter_by(category_id=category.id)
    else:
        category = None
        products_query = Product.query
    
    # Search functionality
    search = request.args.get('search', '')
    if search:
        products_query = products_query.filter(
            (Product.name_ar.contains(search)) | 
            (Product.name_en.contains(search)) |
            (Product.code.contains(search))
        )
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    products = products_query.paginate(
        page=page, per_page=12, error_out=False
    )
    
    return render_template('products.html', 
                         products=products,
                         categories=categories,
                         current_category=category,
                         search=search)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Individual product detail page"""
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id
    ).limit(4).all()
    
    # Parse gallery images
    gallery_images = []
    if product.gallery_images:
        try:
            gallery_images = json.loads(product.gallery_images)
        except:
            gallery_images = []
    
    return render_template('product_detail.html', 
                         product=product,
                         related_products=related_products,
                         gallery_images=gallery_images)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Add product to cart"""
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    # Get or create session ID
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    session_id = session['session_id']
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(
        session_id=session_id,
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            session_id=session_id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    flash('تم إضافة المنتج إلى السلة بنجاح', 'success')
    
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/cart')
def cart():
    """Shopping cart page"""
    if 'session_id' not in session:
        return render_template('cart.html', cart_items=[], total=0)
    
    cart_items = get_cart_items(session['session_id'])
    total = calculate_cart_total(cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update_cart', methods=['POST'])
def update_cart():
    """Update cart item quantities"""
    if 'session_id' not in session:
        return redirect(url_for('cart'))
    
    session_id = session['session_id']
    
    for key, value in request.form.items():
        if key.startswith('quantity_'):
            cart_item_id = int(key.split('_')[1])
            quantity = int(value)
            
            cart_item = CartItem.query.filter_by(
                id=cart_item_id,
                session_id=session_id
            ).first()
            
            if cart_item:
                if quantity > 0:
                    cart_item.quantity = quantity
                else:
                    db.session.delete(cart_item)
    
    db.session.commit()
    flash('تم تحديث السلة بنجاح', 'success')
    
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:cart_item_id>')
def remove_from_cart(cart_item_id):
    """Remove item from cart"""
    if 'session_id' in session:
        cart_item = CartItem.query.filter_by(
            id=cart_item_id,
            session_id=session['session_id']
        ).first()
        
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            flash('تم حذف المنتج من السلة', 'info')
    
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    """Checkout page"""
    if 'session_id' not in session:
        return redirect(url_for('cart'))
    
    cart_items = get_cart_items(session['session_id'])
    if not cart_items:
        flash('السلة فارغة', 'warning')
        return redirect(url_for('cart'))
    
    total = calculate_cart_total(cart_items)
    
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/place_order', methods=['POST'])
def place_order():
    """Process order placement"""
    if 'session_id' not in session:
        return redirect(url_for('cart'))
    
    cart_items = get_cart_items(session['session_id'])
    if not cart_items:
        flash('السلة فارغة', 'warning')
        return redirect(url_for('cart'))
    
    # Generate order number
    order_number = f"MO{datetime.now().strftime('%Y%m%d')}{Order.query.count() + 1:04d}"
    
    # Create order
    order = Order(
        order_number=order_number,
        customer_name=request.form['customer_name'],
        customer_email=request.form['customer_email'],
        customer_phone=request.form['customer_phone'],
        customer_address=request.form['customer_address'],
        total_amount=calculate_cart_total(cart_items),
        payment_method=request.form['payment_method'],
        notes=request.form.get('notes', '')
    )
    
    db.session.add(order)
    db.session.flush()  # Get order ID
    
    # Create order items
    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product.id,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        db.session.add(order_item)
    
    # Clear cart
    CartItem.query.filter_by(session_id=session['session_id']).delete()
    
    db.session.commit()
    
    # Send confirmation email
    send_order_confirmation_email(order)
    
    flash(f'تم تأكيد طلبك برقم: {order_number}', 'success')
    
    return redirect(url_for('index'))

@app.route('/gallery')
def gallery():
    """Gallery page showing project images"""
    categories = Category.query.all()
    category_id = request.args.get('category', type=int)
    
    if category_id:
        images = GalleryImage.query.filter_by(category_id=category_id).all()
        current_category = Category.query.get(category_id)
    else:
        images = GalleryImage.query.all()
        current_category = None
    
    return render_template('gallery.html', 
                         images=images,
                         categories=categories,
                         current_category=current_category)

@app.route('/blog')
def blog():
    """Blog listing page"""
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.filter_by(is_published=True).order_by(
        BlogPost.created_at.desc()
    ).paginate(page=page, per_page=6, error_out=False)
    
    return render_template('blog.html', posts=posts)

@app.route('/blog/<slug>')
def blog_post(slug):
    """Individual blog post page"""
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()
    related_posts = BlogPost.query.filter(
        BlogPost.is_published == True,
        BlogPost.id != post.id
    ).limit(3).all()
    
    return render_template('blog_post.html', post=post, related_posts=related_posts)

@app.route('/about')
def about():
    """About us page"""
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact us page"""
    if request.method == 'POST':
        # Handle contact form submission
        name = request.form['name']
        email = request.form['email']
        phone = request.form.get('phone', '')
        message = request.form['message']
        
        # Here you would typically send an email or save to database
        flash('تم إرسال رسالتك بنجاح. سنتواصل معك قريباً', 'success')
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    """Newsletter subscription"""
    email = request.form['email']
    
    # Check if email already exists
    existing = Newsletter.query.filter_by(email=email).first()
    if existing:
        flash('هذا البريد الإلكتروني مسجل مسبقاً', 'info')
    else:
        newsletter = Newsletter(email=email)
        db.session.add(newsletter)
        db.session.commit()
        flash('تم الاشتراك في النشرة الإخبارية بنجاح', 'success')
    
    return redirect(request.referrer or url_for('index'))

@app.context_processor
def inject_cart_count():
    """Inject cart count into all templates"""
    cart_count = 0
    if 'session_id' in session:
        cart_items = CartItem.query.filter_by(session_id=session['session_id']).all()
        cart_count = sum(item.quantity for item in cart_items)
    
    return {'cart_count': cart_count}
