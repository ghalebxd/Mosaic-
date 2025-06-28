from app import db
from datetime import datetime
from sqlalchemy import Text, DateTime, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Category(db.Model):
    id = db.Column(Integer, primary_key=True)
    name_ar = db.Column(String(100), nullable=False)
    name_en = db.Column(String(100), nullable=False)
    slug = db.Column(String(100), unique=True, nullable=False)
    description_ar = db.Column(Text)
    description_en = db.Column(Text)
    image_url = db.Column(String(200))
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    products = relationship("Product", back_populates="category")

class Product(db.Model):
    id = db.Column(Integer, primary_key=True)
    code = db.Column(String(50), unique=True, nullable=False)
    name_ar = db.Column(String(200), nullable=False)
    name_en = db.Column(String(200), nullable=False)
    description_ar = db.Column(Text)
    description_en = db.Column(Text)
    price = db.Column(Float, nullable=False)
    dimensions = db.Column(String(100))  # e.g., "17 سم × 8 ملم"
    material_ar = db.Column(String(100))
    material_en = db.Column(String(100))
    features_ar = db.Column(Text)
    features_en = db.Column(Text)
    installation_guide_ar = db.Column(Text)
    installation_guide_en = db.Column(Text)
    usage_ar = db.Column(String(200))
    usage_en = db.Column(String(200))
    stock_quantity = db.Column(Integer, default=0)
    is_featured = db.Column(Boolean, default=False)
    is_new_arrival = db.Column(Boolean, default=False)
    image_url = db.Column(String(200))
    gallery_images = db.Column(Text)  # JSON string of image URLs
    category_id = db.Column(Integer, ForeignKey('category.id'), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")

class CartItem(db.Model):
    id = db.Column(Integer, primary_key=True)
    session_id = db.Column(String(100), nullable=False)
    product_id = db.Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = db.Column(Integer, nullable=False, default=1)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="cart_items")

class Order(db.Model):
    id = db.Column(Integer, primary_key=True)
    order_number = db.Column(String(50), unique=True, nullable=False)
    customer_name = db.Column(String(100), nullable=False)
    customer_email = db.Column(String(120), nullable=False)
    customer_phone = db.Column(String(20), nullable=False)
    customer_address = db.Column(Text, nullable=False)
    total_amount = db.Column(Float, nullable=False)
    payment_method = db.Column(String(50), nullable=False)
    status = db.Column(String(20), default='pending')  # pending, confirmed, shipped, delivered
    notes = db.Column(Text)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(db.Model):
    id = db.Column(Integer, primary_key=True)
    order_id = db.Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = db.Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = db.Column(Integer, nullable=False)
    price = db.Column(Float, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")

class BlogPost(db.Model):
    id = db.Column(Integer, primary_key=True)
    title_ar = db.Column(String(200), nullable=False)
    title_en = db.Column(String(200), nullable=False)
    slug = db.Column(String(200), unique=True, nullable=False)
    content_ar = db.Column(Text, nullable=False)
    content_en = db.Column(Text, nullable=False)
    excerpt_ar = db.Column(Text)
    excerpt_en = db.Column(Text)
    image_url = db.Column(String(200))
    is_published = db.Column(Boolean, default=True)
    created_at = db.Column(DateTime, default=datetime.utcnow)

class GalleryImage(db.Model):
    id = db.Column(Integer, primary_key=True)
    title_ar = db.Column(String(200))
    title_en = db.Column(String(200))
    description_ar = db.Column(Text)
    description_en = db.Column(Text)
    image_url = db.Column(String(200), nullable=False)
    category_id = db.Column(Integer, ForeignKey('category.id'))
    is_featured = db.Column(Boolean, default=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    category = relationship("Category")

class Newsletter(db.Model):
    id = db.Column(Integer, primary_key=True)
    email = db.Column(String(120), unique=True, nullable=False)
    is_active = db.Column(Boolean, default=True)
    created_at = db.Column(DateTime, default=datetime.utcnow)
