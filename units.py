import json
from models import Category, Product, BlogPost, GalleryImage, CartItem
from app import db
from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def init_sample_data():
    """Initialize sample data if database is empty"""
    if Category.query.count() == 0:
        # Create categories
        categories_data = [
            {
                'name_ar': 'بديل الخشب',
                'name_en': 'Wood Panels',
                'slug': 'wood-panels',
                'description_ar': 'ألواح بديل الخشب عالية الجودة مقاومة للرطوبة',
                'description_en': 'High-quality moisture-resistant wood alternative panels',
                'image_url': 'https://pixabay.com/get/g70327e9caba8e9f5020d946f7eefad413c2d18cbffe4946a71fd6f1d8ee76d5be383fd49e788e9adb2f2280d330f3cda473acf96b38f23d9f60a7388f81c7e0e_1280.jpg'
            },
            {
                'name_ar': 'بديل الرخام',
                'name_en': 'PVC Marble',
                'slug': 'pvc-marble',
                'description_ar': 'ألواح بديل الرخام البلاستيكية بتصاميم أنيقة',
                'description_en': 'Elegant PVC marble alternative panels',
                'image_url': 'https://pixabay.com/get/g608bb8d422d3216c5cf6229b3af268335541a9c7c707fd626c4d67828f244e451a7344d0f68143ff5ba040d4aa7a3c5cd81cd2392adcd78a517c92664e5018a6_1280.jpg'
            },
            {
                'name_ar': 'الشيبورد',
                'name_en': 'Chipboard',
                'slug': 'chipboard',
                'description_ar': 'ألواح الشيبورد المضغوط لمختلف الاستخدامات',
                'description_en': 'Compressed chipboard panels for various applications',
                'image_url': 'https://pixabay.com/get/g3ddc6222e79830303e215d6f71c0499d016eced01fc9b40220f7252998110ab1f8eae25d6f5f6df83680e3c4a4efcf024ff13c79626dc99f1bd172d6bf4bc14f_1280.jpg'
            },
            {
                'name_ar': 'البراويز',
                'name_en': 'Frames',
                'slug': 'frames',
                'description_ar': 'براويز ديكورية متنوعة للحوائط والأسقف',
                'description_en': 'Various decorative frames for walls and ceilings',
                'image_url': 'https://pixabay.com/get/ge98b60af3baefaf58bed21caa5f303c9e8a70ec4cc34ff6b031392d9094720a1c28c9ff6a5631237e7799dc2488d141c29dee43421a316d064a847b4ecf101f1_1280.jpg'
            },
            {
                'name_ar': 'الإكسسوارات',
                'name_en': 'Accessories',
                'slug': 'accessories',
                'description_ar': 'إكسسوارات التركيب والزوايا والفواصل',
                'description_en': 'Installation accessories, corners and dividers',
                'image_url': 'https://pixabay.com/get/gbf00cd26856fd9fd6f15f5fe270cd0475fb68b3fe8ee87b1b2abd85c858f46ceaa30615ab9e7244e3dd230104fd2402a890724657db9f77cfb7a8bb061d59e4d_1280.jpg'
            }
        ]
        
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.session.add(category)
        
        db.session.commit()
        
        # Create sample products
        products_data = [
            {
                'code': '1620K-001',
                'name_ar': 'بديل الخشب 17 سم',
                'name_en': 'Wood Panel 17cm',
                'description_ar': 'بديل خشب عالي الجودة بعرض 17 سم، مقاوم للرطوبة وسهل التركيب',
                'description_en': 'High-quality 17cm wood alternative panel, moisture-resistant and easy to install',
                'price': 25.00,
                'dimensions': '17 سم × 8 ملم',
                'material_ar': 'بوليمير',
                'material_en': 'Polymer',
                'features_ar': 'مقاوم للرطوبة، سهل التركيب، لا يحتاج صيانة',
                'features_en': 'Moisture resistant, easy installation, maintenance-free',
                'installation_guide_ar': 'يتم التركيب بالغراء الخاص أو المسامير',
                'installation_guide_en': 'Install with special adhesive or screws',
                'usage_ar': 'للاستخدام الداخلي والخارجي',
                'usage_en': 'For indoor and outdoor use',
                'stock_quantity': 353,
                'is_featured': True,
                'is_new_arrival': True,
                'image_url': 'https://pixabay.com/get/g70327e9caba8e9f5020d946f7eefad413c2d18cbffe4946a71fd6f1d8ee76d5be383fd49e788e9adb2f2280d330f3cda473acf96b38f23d9f60a7388f81c7e0e_1280.jpg',
                'category_id': 1
            },
            {
                'code': '6001-04',
                'name_ar': 'بديل الخشب فرزة ناعمة 6001-04',
                'name_en': 'Smooth Finish Wood Panel 6001-04',
                'description_ar': 'بديل خشب بفرزة ناعمة وتصميم أنيق',
                'description_en': 'Wood alternative with smooth finish and elegant design',
                'price': 28.50,
                'dimensions': '15 سم × 8 ملم',
                'material_ar': 'بوليمير',
                'material_en': 'Polymer',
                'features_ar': 'فرزة ناعمة، مقاوم للخدش، سهل التنظيف',
                'features_en': 'Smooth finish, scratch resistant, easy to clean',
                'stock_quantity': 200,
                'is_featured': True,
                'image_url': 'https://pixabay.com/get/g3ddc6222e79830303e215d6f71c0499d016eced01fc9b40220f7252998110ab1f8eae25d6f5f6df83680e3c4a4efcf024ff13c79626dc99f1bd172d6bf4bc14f_1280.jpg',
                'category_id': 1
            },
            {
                'code': 'PVC-120',
                'name_ar': 'بديل الرخام بيج وأبيض وأسود',
                'name_en': 'Beige, White and Black Marble Panel',
                'description_ar': 'بديل رخام بألوان متعددة بأبعاد 60×120 سم',
                'description_en': 'Multi-color marble alternative 60×120 cm',
                'price': 45.00,
                'dimensions': '60×120 سم',
                'material_ar': 'PVC',
                'material_en': 'PVC',
                'features_ar': 'مقاوم للماء، سهل التنظيف، أشكال متنوعة',
                'features_en': 'Waterproof, easy to clean, various patterns',
                'stock_quantity': 150,
                'is_featured': True,
                'image_url': 'https://pixabay.com/get/g608bb8d422d3216c5cf6229b3af268335541a9c7c707fd626c4d67828f244e451a7344d0f68143ff5ba040d4aa7a3c5cd81cd2392adcd78a517c92664e5018a6_1280.jpg',
                'category_id': 2
            },
            {
                'code': 'CB-189',
                'name_ar': 'شيبورد 189 بني محروق',
                'name_en': 'Chipboard 189 Burnt Brown',
                'description_ar': 'شيبورد بني محروق سماكة 8 ملم - 77 لوح',
                'description_en': 'Burnt brown chipboard 8mm thickness - 77 panels',
                'price': 35.00,
                'dimensions': '120×240 سم × 8 ملم',
                'material_ar': 'خشب مضغوط',
                'material_en': 'Compressed wood',
                'stock_quantity': 77,
                'image_url': 'https://pixabay.com/get/g36a1921e8269ec974816c85501c614ef21c78e81174712d895cc54355883d16d3772de62d3644ed95e7f4f6f3353cc8ba281c08b748675f472154e5dcc30e5a2_1280.jpg',
                'category_id': 3
            },
            {
                'code': 'FR-002',
                'name_ar': 'براويز 2 سم',
                'name_en': '2cm Decorative Frames',
                'description_ar': 'براويز ديكورية بعرض 2 سم - 120 قطعة',
                'description_en': '2cm decorative frames - 120 pieces',
                'price': 15.00,
                'dimensions': '2 سم عرض',
                'material_ar': 'PVC',
                'material_en': 'PVC',
                'stock_quantity': 120,
                'image_url': 'https://pixabay.com/get/ge98b60af3baefaf58bed21caa5f303c9e8a70ec4cc34ff6b031392d9094720a1c28c9ff6a5631237e7799dc2488d141c29dee43421a316d064a847b4ecf101f1_1280.jpg',
                'category_id': 4
            }
        ]
        
        for prod_data in products_data:
            product = Product(**prod_data)
            db.session.add(product)
        
        # Create sample blog posts
        blog_posts_data = [
            {
                'title_ar': 'كيف تختار بديل الرخام المناسب؟',
                'title_en': 'How to Choose the Right Marble Alternative?',
                'slug': 'choose-marble-alternative',
                'content_ar': 'عند اختيار بديل الرخام، يجب مراعاة عدة عوامل مهمة...',
                'content_en': 'When choosing marble alternatives, several important factors should be considered...',
                'excerpt_ar': 'دليل شامل لاختيار أفضل بديل رخام لمنزلك',
                'excerpt_en': 'Complete guide to choosing the best marble alternative for your home',
                'image_url': 'https://pixabay.com/get/g608bb8d422d3216c5cf6229b3af268335541a9c7c707fd626c4d67828f244e451a7344d0f68143ff5ba040d4aa7a3c5cd81cd2392adcd78a517c92664e5018a6_1280.jpg'
            },
            {
                'title_ar': 'خطوات تركيب بديل الخشب بنفسك',
                'title_en': 'DIY Wood Panel Installation Steps',
                'slug': 'diy-wood-panel-installation',
                'content_ar': 'تركيب بديل الخشب عملية بسيطة يمكن القيام بها بنفسك...',
                'content_en': 'Installing wood alternatives is a simple process you can do yourself...',
                'excerpt_ar': 'تعلم كيفية تركيب بديل الخشب خطوة بخطوة',
                'excerpt_en': 'Learn how to install wood alternatives step by step',
                'image_url': 'https://pixabay.com/get/g70327e9caba8e9f5020d946f7eefad413c2d18cbffe4946a71fd6f1d8ee76d5be383fd49e788e9adb2f2280d330f3cda473acf96b38f23d9f60a7388f81c7e0e_1280.jpg'
            }
        ]
        
        for post_data in blog_posts_data:
            blog_post = BlogPost(**post_data)
            db.session.add(blog_post)
        
        # Create sample gallery images
        gallery_data = [
            {
                'title_ar': 'تطبيق بديل الخشب في غرفة المعيشة',
                'title_en': 'Wood Panel Application in Living Room',
                'image_url': 'https://pixabay.com/get/g3fcaeab766a11f6d7635a9bbdb2960bd4d5d0024f677d156d3333069d2431e40e7379ad4835aa8e18858286d348424904ec163738880eac084a849cc7b80262a_1280.jpg',
                'category_id': 1,
                'is_featured': True
            },
            {
                'title_ar': 'تطبيق بديل الرخام في الحمام',
                'title_en': 'Marble Alternative in Bathroom',
                'image_url': 'https://pixabay.com/get/g0a107e5ca3aad5e717ccbaf6ccf50864ad9e59abdf051cb76405ac90afe155846eecf99ea7b8749db7498c7c327ed586fdd1467759d881fc61864fb162fdc7a9_1280.jpg',
                'category_id': 2,
                'is_featured': True
            }
        ]
        
        for img_data in gallery_data:
            gallery_img = GalleryImage(**img_data)
            db.session.add(gallery_img)
        
        db.session.commit()

def get_cart_items(session_id):
    """Get cart items for a session"""
    return CartItem.query.filter_by(session_id=session_id).all()

def calculate_cart_total(cart_items):
    """Calculate total price for cart items"""
    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity
    return total

def send_order_confirmation_email(order):
    """Send order confirmation email"""
    try:
        msg = Message(
            subject=f'تأكيد الطلب - موزايك ديكور - {order.order_number}',
            recipients=[order.customer_email],
            html=f'''
            <div dir="rtl" style="font-family: Arial, sans-serif;">
                <h2>شكراً لك على طلبك من موزايك ديكور</h2>
                <p>عزيزي/عزيزتي {order.customer_name},</p>
                <p>تم استلام طلبك بنجاح برقم: <strong>{order.order_number}</strong></p>
                <p>إجمالي المبلغ: <strong>{order.total_amount} ش.ج</strong></p>
                <p>سيتم التواصل معك قريباً لتأكيد الطلب وتحديد موعد التوصيل.</p>
                <p>شكراً لثقتك بنا</p>
                <p>موزايك ديكور</p>
            </div>
            '''
        )
        mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {e}")
