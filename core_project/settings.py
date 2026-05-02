import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Klasör Yolları ve Çevresel Değişkenler
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# GÜVENLİK NOTU: Gerçek projede bunu .env içine almalısın
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

# 2. Uygulamalar
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'axes',
    'lms_app',
]

# 3. Ara Katmanlar (Middleware) - Hataları çözen kısım
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'core_project.urls'

# 4. Şablonlar (Templates) - Admin hatasını çözen kısım
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'lms_app' / 'templates'], # Şablon klasörün
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'lms_app.context_processors.cart_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'core_project.wsgi.application'

# 5. LOKAL MSSQL Veritabanı (Windows Authentication ile)
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.environ.get('DB_NAME', 'lms_db'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '1433'),
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            # Trusted_Connection=yes parametresi ile Windows hesabınla giriş yapar
            'extra_params': 'Trusted_Connection=yes;Connection Timeout=30;',
        },
    }
}

# 6. Statik Dosyalar (İstediğin düzeltme burada)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "lms_app" / "static",
]
# Canlıya geçişte (collectstatic) dosyaların toplanacağı yer
STATIC_ROOT = BASE_DIR / "staticfiles"

# 7. Diğer Önemli Ayarlar (Kimlik Doğrulama ve Oturum)
AUTH_USER_MODEL = 'lms_app.CustomUser'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'axes.backends.AxesStandaloneBackend',
]

# Tarayıcı kapatıldığında oturumu (session) otomatik sonlandır (Beni Hatırla özelliği için temel)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# 8. Medya Dosyaları (Yüklenen Resimler İçin)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==========================================
# 9. GERÇEK E-POSTA (SMTP) AYARLARI
# ==========================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Bilgileri güvenli bir şekilde .env dosyasından çekiyoruz
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Maillerin kime aitmiş gibi görüneceği
DEFAULT_FROM_EMAIL = f"KTÜ LMS <{EMAIL_HOST_USER}>"

AXES_FAILURE_LIMIT = 5  # 5 hatalı şifre denemesinde hesabı kilitler
AXES_COOLOFF_TIME = 1  # Hesap 1 saat (veya timedelta(minutes=15) gibi) kilitli kalır
AXES_RESET_ON_SUCCESS = True  # Kullanıcı doğru şifreyle girerse sayacı hemen sıfırlar
AXES_LOCKOUT_TEMPLATE = 'auth/lockout.html'  # Kilitlendiğinde gösterilecek özel ekran

# ==========================================
# OTURUM (SESSION) ZAMAN AŞIMI AYARLARI
# ==========================================

# Kullanıcının hareketsiz kalabileceği maksimum süre (saniye cinsinden). 
# Örnek: 30 dakika = 30 * 60 = 1800 saniye
SESSION_COOKIE_AGE = 1800 

# Kullanıcı sitede her gezindiğinde (yeni bir sayfaya tıkladığında) süreyi baştan başlatır.
# Eğer bu True olmazsa, kullanıcı aktif olsa bile 30 dakika sonra atılır.
SESSION_SAVE_EVERY_REQUEST = True

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']