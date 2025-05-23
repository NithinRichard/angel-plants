"""
Django settings for angels_plants project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
env_path = os.path.join(BASE_DIR, '.env')
print(f"Loading .env file from: {env_path}")
load_dotenv(env_path)

# Debug: Print loaded environment variables
print("=== Environment Variables ===")
print(f"RAZORPAY_KEY_ID: {'*' * 8}{os.getenv('RAZORPAY_KEY_ID', 'NOT FOUND')[-4:] if os.getenv('RAZORPAY_KEY_ID') else 'NOT FOUND'}")
print(f"RAZORPAY_KEY_SECRET: {'*' * 8}{os.getenv('RAZORPAY_KEY_SECRET', 'NOT FOUND')[-4:] if os.getenv('RAZORPAY_KEY_SECRET') else 'NOT FOUND'}")
print("===========================")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Payment Settings
PAYMENT_SUCCESS_URL = 'payment:payment_success'
PAYMENT_FAILURE_URL = 'payment:payment_failed'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Allow Vercel deployment
ALLOWED_HOSTS = ['*', '.vercel.app', '.now.sh', 'localhost', '127.0.0.1']

# Authentication
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'store:account'
LOGOUT_REDIRECT_URL = 'store:product_list'

# Razorpay Configuration
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')
RAZORPAY_WEBHOOK_SECRET = os.getenv('RAZORPAY_WEBHOOK_SECRET', '')

# Payment Settings
PAYMENT_SUCCESS_URL = 'payment:payment_success'
PAYMENT_FAILURE_URL = 'payment:payment_failed'
PAYMENT_METHODS = [
    ('razorpay', 'Razorpay'),
    ('cod', 'Cash on Delivery'),
]

# Debug settings for payments
PAYMENT_DEBUG = DEBUG

# Currency settings
CURRENCY = 'INR'
CURRENCY_SYMBOL = '₹'  # Indian Rupee symbol

# Order settings
ORDER_PREFIX = 'ORD'
ORDER_ID_LENGTH = 8  # Length of the random part of the order ID

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'store',
    'payment',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_ckeditor_5',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'angels_plants.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.categories',
                'store.context_processors.cart',
                'store.context_processors.wishlist_count',
                'store.context_processors.contact_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'angels_plants.wsgi.application'

# Database
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Security settings for production
if not DEBUG:
    # HTTPS settings
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # HSTS settings
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Other security headers
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    
    # CSRF trusted origins - update with your production domain
    CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com', 'https://www.yourdomain.com']
    
    # Logging for production
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'logs/django_errors.log'),
            },
            'razorpay_file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'logs/razorpay.log'),
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'ERROR',
                'propagate': True,
            },
            'payment': {
                'handlers': ['razorpay_file'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (you'll need to use an external service like AWS S3 for media files in production)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login/Logout URLs
LOGIN_REDIRECT_URL = 'store:product_list'
LOGOUT_REDIRECT_URL = 'store:product_list'
LOGIN_URL = 'login'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@angelsplants.com')

# Contact Information
CONTACT_EMAIL = os.getenv('CONTACT_EMAIL', 'nithinrichard1@gmail.com')
CONTACT_PHONE = '+91 9848666666'
BUSINESS_ADDRESS = 'Puthenthope Trivandrum Kerala India 695586'
BUSINESS_HOURS = [
    'Monday - Friday: 9:00 AM - 6:00 PM',
    'Saturday: 10:00 AM - 4:00 PM',
    'Sunday: Closed'
]

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# CKEditor 5 Configuration
customColorPalette = [
    {"color": 'hsl(4, 90%, 58%)', "label": 'Red'},
    {"color": 'hsl(340, 82%, 52%)', "label": 'Pink'},
    {"color": 'hsl(291, 64%, 42%)', "label": 'Purple'},
    {"color": 'hsl(262, 52%, 47%)', "label": 'Deep Purple'},
    {"color": 'hsl(231, 48%, 48%)', "label": 'Indigo'},
    {"color": 'hsl(207, 90%, 54%)', "label": 'Blue'},
]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],
    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
                   'code', 'subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                    'bulletedList', 'numberedList', 'todoList', '|', 'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable',],
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                       'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side', '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]
        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells',
                              'tableProperties', 'tableCellProperties'],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph',
                    'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1',
                    'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2',
                    'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3',
                    'title': 'Heading 3', 'class': 'ck-heading_heading3'}
            ]
        }
    },
}

# Session settings
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
CART_SESSION_ID = 'cart'
WISHLIST_SESSION_ID = 'wishlist'
