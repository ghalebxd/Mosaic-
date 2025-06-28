// Main JavaScript for Mosaic Decor Website
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all features
    initScrollEffects();
    initLazyLoading();
    initSearchFunctionality();
    initCartFunctionality();
    initProductQuickView();
    initNewsletterPopup();
    initTooltips();
    initSmoothScrolling();
    initBackToTop();
    initOfflineMode();
});

// Scroll Effects
function initScrollEffects() {
    let ticking = false;
    
    function updateScrollEffects() {
        const scrollTop = window.pageYOffset;
        const navbar = document.querySelector('.navbar');
        
        // Navbar background on scroll
        if (scrollTop > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        // Parallax effect for hero section
        const hero = document.querySelector('.hero-section');
        if (hero) {
            const speed = scrollTop * 0.5;
            hero.style.transform = `translateY(${speed}px)`;
        }
        
        ticking = false;
    }
    
    function requestScrollUpdate() {
        if (!ticking) {
            requestAnimationFrame(updateScrollEffects);
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', requestScrollUpdate);
}

// Lazy Loading for Images
function initLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// Search Functionality
function initSearchFunctionality() {
    const searchInputs = document.querySelectorAll('input[type="text"][name="search"]');
    
    searchInputs.forEach(input => {
        let searchTimeout;
        
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length > 2) {
                searchTimeout = setTimeout(() => {
                    performSearch(query);
                }, 300);
            }
        });
    });
}

function performSearch(query) {
    // Add search suggestions or live search results
    console.log('Searching for:', query);
    // Implementation would depend on backend API
}

// Cart Functionality
function initCartFunctionality() {
    // Update cart count in navbar
    updateCartCount();
    
    // Add to cart buttons
    document.querySelectorAll('[data-product-id]').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const quantity = this.dataset.quantity || 1;
            addToCart(productId, quantity);
        });
    });
}

function addToCart(productId, quantity = 1) {
    // Show loading state
    const button = document.querySelector(`[data-product-id="${productId}"]`);
    if (button) {
        button.classList.add('loading');
        button.disabled = true;
    }
    
    // Simulate API call
    setTimeout(() => {
        updateCartCount();
        showNotification('تم إضافة المنتج إلى السلة', 'success');
        
        if (button) {
            button.classList.remove('loading');
            button.disabled = false;
        }
    }, 1000);
}

function updateCartCount() {
    // Get cart count from localStorage or API
    const cartCount = getCartCount();
    const cartBadges = document.querySelectorAll('.cart-count');
    
    cartBadges.forEach(badge => {
        badge.textContent = cartCount;
        badge.style.display = cartCount > 0 ? 'inline' : 'none';
    });
}

function getCartCount() {
    // Return cart count from localStorage or session
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    return cart.reduce((total, item) => total + item.quantity, 0);
}

// Product Quick View
function initProductQuickView() {
    document.querySelectorAll('.quick-view-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            showProductQuickView(productId);
        });
    });
}

function showProductQuickView(productId) {
    // Create and show quick view modal
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">معاينة سريعة</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="text-center">
                        <div class="spinner-border text-primary" role="status">
                            <span class="sr-only">جاري التحميل...</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    // Load product data
    loadProductData(productId).then(product => {
        modal.querySelector('.modal-body').innerHTML = generateQuickViewHTML(product);
    });
    
    // Clean up on close
    modal.addEventListener('hidden.bs.modal', () => {
        document.body.removeChild(modal);
    });
}

function loadProductData(productId) {
    // Simulate API call
    return new Promise(resolve => {
        setTimeout(() => {
            resolve({
                id: productId,
                name: 'بديل الخشب 17 سم',
                price: 25.00,
                image: '/static/images/product-placeholder.jpg',
                description: 'وصف المنتج هنا...'
            });
        }, 1000);
    });
}

function generateQuickViewHTML(product) {
    return `
        <div class="row">
            <div class="col-md-6">
                <img src="${product.image}" class="img-fluid" alt="${product.name}">
            </div>
            <div class="col-md-6">
                <h4>${product.name}</h4>
                <p class="text-muted">${product.description}</p>
                <p class="h5 text-primary">${product.price} ش.ج</p>
                <button class="btn btn-primary" onclick="addToCart(${product.id})">
                    <i class="fas fa-cart-plus me-2"></i>إضافة للسلة
                </button>
            </div>
        </div>
    `;
}

// Newsletter Popup
function initNewsletterPopup() {
    const hasSeenPopup = localStorage.getItem('newsletter_popup_seen');
    
    if (!hasSeenPopup) {
        setTimeout(() => {
            const modal = document.getElementById('newsletterModal');
            if (modal) {
                const bsModal = new bootstrap.Modal(modal);
                bsModal.show();
                localStorage.setItem('newsletter_popup_seen', 'true');
            }
        }, 30000); // Show after 30 seconds
    }
}

// Tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Smooth Scrolling
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Back to Top Button
function initBackToTop() {
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopBtn.className = 'btn btn-primary position-fixed';
    backToTopBtn.style.cssText = `
        bottom: 90px;
        left: 20px;
        z-index: 999;
        width: 45px;
        height: 45px;
        border-radius: 50%;
        display: none;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    `;
    
    document.body.appendChild(backToTopBtn);
    
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });
}

// Offline Mode
function initOfflineMode() {
    window.addEventListener('online', () => {
        showNotification('تم استعادة الاتصال بالإنترنت', 'success');
    });
    
    window.addEventListener('offline', () => {
        showNotification('لا يوجد اتصال بالإنترنت', 'warning');
    });
}

// Notification System
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Form Validation
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    // Email validation
    const emailFields = form.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        if (field.value && !isValidEmail(field.value)) {
            field.classList.add('is-invalid');
            isValid = false;
        }
    });
    
    // Phone validation
    const phoneFields = form.querySelectorAll('input[type="tel"]');
    phoneFields.forEach(field => {
        if (field.value && !isValidPhone(field.value)) {
            field.classList.add('is-invalid');
            isValid = false;
        }
    });
    
    return isValid;
}

function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function isValidPhone(phone) {
    const regex = /^(\+970|970|0)(5[0-9]|2[0-9])[0-9]{7}$/;
    return regex.test(phone.replace(/\s|-/g, ''));
}

// WhatsApp Integration
function openWhatsApp(message = '') {
    const phoneNumber = '970591234567';
    const defaultMessage = 'مرحباً، أود الاستفسار عن منتجاتكم';
    const finalMessage = message || defaultMessage;
    const url = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(finalMessage)}`;
    window.open(url, '_blank');
}

// Product Sharing
function shareProduct(title, url, image) {
    if (navigator.share) {
        navigator.share({
            title: title,
            url: url,
            text: 'شاهد هذا المنتج الرائع من موزايك ديكور'
        }).catch(console.error);
    } else {
        // Fallback to copy URL
        navigator.clipboard.writeText(url).then(() => {
            showNotification('تم نسخ رابط المنتج', 'success');
        }).catch(() => {
            showNotification('فشل في نسخ الرابط', 'danger');
        });
    }
}

// Search Suggestions
function initSearchSuggestions() {
    const searchInputs = document.querySelectorAll('input[name="search"]');
    
    searchInputs.forEach(input => {
        const suggestions = document.createElement('div');
        suggestions.className = 'search-suggestions position-absolute bg-white border rounded shadow-sm';
        suggestions.style.cssText = `
            top: 100%;
            left: 0;
            right: 0;
            z-index: 1000;
            display: none;
            max-height: 300px;
            overflow-y: auto;
        `;
        
        input.parentElement.style.position = 'relative';
        input.parentElement.appendChild(suggestions);
        
        input.addEventListener('input', function() {
            const query = this.value.trim();
            if (query.length > 1) {
                loadSearchSuggestions(query, suggestions);
            } else {
                suggestions.style.display = 'none';
            }
        });
        
        // Hide suggestions when clicking outside
        document.addEventListener('click', function(e) {
            if (!input.contains(e.target) && !suggestions.contains(e.target)) {
                suggestions.style.display = 'none';
            }
        });
    });
}

function loadSearchSuggestions(query, container) {
    // Mock suggestions - replace with actual API call
    const mockSuggestions = [
        'بديل الخشب 17 سم',
        'بديل الرخام بيج',
        'شيبورد بني',
        'براويز ديكورية'
    ].filter(item => item.includes(query));
    
    if (mockSuggestions.length > 0) {
        container.innerHTML = mockSuggestions.map(suggestion => 
            `<div class="suggestion-item p-2 border-bottom cursor-pointer hover:bg-light" onclick="selectSuggestion('${suggestion}')">${suggestion}</div>`
        ).join('');
        container.style.display = 'block';
    } else {
        container.style.display = 'none';
    }
}

function selectSuggestion(suggestion) {
    const searchInput = document.querySelector('input[name="search"]:focus');
    if (searchInput) {
        searchInput.value = suggestion;
        searchInput.form.submit();
    }
}

// Performance Monitoring
function initPerformanceMonitoring() {
    // Monitor page load time
    window.addEventListener('load', () => {
        const loadTime = performance.now();
        console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);
        
        // Send analytics if needed
        if (loadTime > 3000) {
            console.warn('Page load time is slow');
        }
    });
    
    // Monitor largest contentful paint
    if ('PerformanceObserver' in window) {
        const observer = new PerformanceObserver((list) => {
            const entries = list.getEntries();
            const lastEntry = entries[entries.length - 1];
            console.log('LCP:', lastEntry.startTime);
        });
        
        observer.observe({ entryTypes: ['largest-contentful-paint'] });
    }
}

// Error Handling
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    
    // Show user-friendly error message for critical errors
    if (e.error && e.error.stack && e.error.stack.includes('critical')) {
        showNotification('حدث خطأ في النظام. يرجى إعادة تحميل الصفحة.', 'danger');
    }
});

// Service Worker Registration
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
        .then(registration => {
            console.log('SW registered:', registration);
        })
        .catch(error => {
            console.log('SW registration failed:', error);
        });
}

// Accessibility Improvements
function initAccessibility() {
    // Skip to main content link
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'تخطي إلى المحتوى الرئيسي';
    skipLink.className = 'sr-only sr-only-focusable btn btn-primary position-absolute';
    skipLink.style.top = '10px';
    document.body.insertBefore(skipLink, document.body.firstChild);
    
    // Announce page changes for screen readers
    const announcer = document.createElement('div');
    announcer.setAttribute('aria-live', 'polite');
    announcer.setAttribute('aria-atomic', 'true');
    announcer.className = 'sr-only';
    document.body.appendChild(announcer);
    
    window.announceChange = function(message) {
        announcer.textContent = message;
    };
}

// Initialize accessibility on DOM ready
document.addEventListener('DOMContentLoaded', initAccessibility);

// Export functions for external use
window.MosaicDecor = {
    showNotification,
    addToCart,
    shareProduct,
    openWhatsApp,
    validateForm
};
