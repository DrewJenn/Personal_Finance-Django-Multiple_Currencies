from pathlib import Path
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1', 'https://4cfa-2600-8807-9105-b100-a80f-15b3-eac1-4f']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djmoney',
    'Personal_Finance_APP',
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

ROOT_URLCONF = 'Personal_Finance_APP.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Personal_Finance.wsgi.application'


# Database default sqlite

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'Personal_Finance_APP/static',]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/Personal_Finance_APP/login_page/'
LOGOUT_REDIRECT_URL = '/'  
CSRF_TRUSTED_ORIGINS = [
    'https://a23c-2600-8807-9105-b100-6063-a7-7294-d305.ngrok-free.app',  # Add your ngrok URL here (while using ngrok change when server goes live)
    'http://localhost:4040', 
]

CURRENCIES = ('AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN',
               'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHF', 'CLF',
                'CLP', 'CNH', 'CNY', 'COP', 'CRC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN',
                'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HTG',
                'HUF', 'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF',
                'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA',
                'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MXV', 'MYR', 'MZN', 'NAD', 'NGN',
                'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON',
                'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLE', 'SLL', 'SOS', 'SRD',
                'STN', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TWD',
                'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XCD',
                'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMW')

CURRENCY_CHOICES = [('USD', 'USD $'), ('EUR', 'EUR €'), ('AED', 'AED د.إ'), ('AFN', 'AFN ؋'), 
                   ('ALL', 'ALL Lek'), ('AMD', 'AMD ֏'), ('ANG', 'ANG ƒ'), ('AOA', 'AOA Kz'), ('ARS', 'ARS $'), 
                   ('AUD', 'AUD $'), ('AWG', 'AWG ƒ'), ('AZN', 'AZN ₼'), ('BAM', 'BAM KM'), ('BBD', 'BBD $'), 
                   ('BDT', 'BDT ৳'), ('BGN', 'BGN лв'), ('BHD', 'BHD د.ب'), ('BIF', 'BIF Fr'), ('BMD', 'BMD $'),
                   ('BND', 'BND $'), ('BOB', 'BOB Bs'), ('BRL', 'BRL R$'), ('BSD', 'BSD $'), ('BWP', 'BWP P'),
                    ('BYN', 'BYN Br'), ('BZD', 'BZD $'), ('CAD', 'CAD $'), ('CDF', 'CDF Fr'), ('CHF', 'CHF CHF'),
                    ('CLF', 'CLF UF'), ('CLP', 'CLP $'), ('CNH', 'CNH ¥'), ('CNY', 'CNY ¥'), ('COP', 'COP $'),
                    ('CRC', 'CRC ₡'), ('CUP', 'CUP ₱'), ('CVE', 'CVE $'), ('CZK', 'CZK Kč'), ('DJF', 'DJF Fr'),
                    ('DKK', 'DKK kr'), ('DOP', 'DOP RD$'), ('DZD', 'DZD د.ج'), ('EGP', 'EGP ج.م'), ('ERN', 'ERN Nfk'),
                    ('FJD', 'FJD $'), ('FKP', 'FKP £'), ('GBP', 'GBP £'), ('GEL', 'GEL ₾'), ('GHS', 'GHS ₵'),
                    ('GIP', 'GIP £'), ('GMD', 'GMD D'), ('GNF', 'GNF Fr'), ('GTQ', 'GTQ Q'), ('GYD', 'GYD $'),
                    ('HKD', 'HKD $'), ('HNL', 'HNL L'), ('HTG', 'HTG G'), ('HUF', 'HUF Ft'), ('IDR', 'IDR Rp'),
                    ('ILS', 'ILS ₪'), ('INR', 'INR ₹'), ('IQD', 'IQD د.ع'), ('IRR', 'IRR ﷼'), ('ISK', 'ISK kr'),
                    ('JMD', 'JMD $'), ('JOD', 'JOD د.ا'), ('JPY', 'JPY ¥'), ('KES', 'KES Sh'), ('KGS', 'KGS сом'),
                    ('KHR', 'KHR ៛'), ('KMF', 'KMF Fr'), ('KPW', 'KPW ₩'), ('KRW', 'KRW ₩'), ('KWD', 'KWD د.ك'),
                    ('KYD', 'KYD $'), ('KZT', 'KZT ₸'), ('LAK', 'LAK ₭'), ('LBP', 'LBP ل.ل'), ('LKR', 'LKR Rs'),
                    ('LRD', 'LRD $'), ('LSL', 'LSL L'), ('LYD', 'LYD ل.د'), ('MAD', 'MAD د.م'), ('MDL', 'MDL L'),
                    ('MGA', 'MGA Ar'), ('MKD', 'MKD ден'), ('MMK', 'MMK K'), ('MNT', 'MNT ₮'), ('MOP', 'MOP P'),
                    ('MRU', 'MRU UM'), ('MUR', 'MUR Rs'), ('MVR', 'MVR ރ'), ('MWK', 'MWK K'), ('MXN', 'MXN $'),
                    ('MXV', 'MXV UDI'), ('MYR', 'MYR RM'), ('MZN', 'MZN MT'), ('NAD', 'NAD $'), ('NGN', 'NGN ₦'),
                    ('NIO', 'NIO C$'), ('NOK', 'NOK kr'), ('NPR', 'NPR रु'), ('NZD', 'NZD $'), ('OMR', 'OMR ر.ع.'),
                    ('PAB', 'PAB B/.'), ('PEN', 'PEN S/.'), ('PGK', 'PGK K'), ('PHP', 'PHP ₱'), ('PKR', 'PKR Rs'),
                    ('PLN', 'PLN zł'), ('PYG', 'PYG ₲'), ('QAR', 'QAR ر.ق'), ('RON', 'RON lei'), ('RSD', 'RSD РСД'), 
                    ('RUB', 'RUB ₽'), ('RWF', 'RWF Fr'), ('SAR', 'SAR ر.س'), ('SBD', 'SBD $'), ('SCR', 'SCR ₨'), 
                    ('SDG', 'SDG ج.س'), ('SEK', 'SEK kr'), ('SGD', 'SGD $'), ('SHP', 'SHP £'), ('SLE', 'SLE Le'),
                    ('SLL', 'SLL Le'), ('SOS', 'SOS Sh'), ('SRD', 'SRD $'), ('STN', 'STN Db'), ('SVC', 'SVC $'), 
                    ('SYP', 'SYP ل.س'), ('SZL', 'SZL L'), ('THB', 'THB ฿'), ('TJS', 'TJS ЅМ'), ('TMT', 'TMT ман'),
                    ('TND', 'TND د.ت'), ('TOP', 'TOP T$'), ('TRY', 'TRY ₺'), ('TTD', 'TTD $'), ('TWD', 'TWD NT$'),
                    ('TZS', 'TZS Sh'), ('UAH', 'UAH ₴'), ('UGX', 'UGX USh'), ('USD', 'USD $'), ('UYU', 'UYU $'), 
                    ('UZS', 'UZS сўм'), ('VES', 'VES Bs.S'), ('VND', 'VND ₫'), ('VUV', 'VUV Vt'), ('WST', 'WST T'),
                    ('XAF', 'XAF CFA'), ('XCD', 'XCD $'), ('XDR', 'XDR'), ('XOF', 'XOF CFA'), ('XPF', 'XPF CFP'),
                    ('YER', 'YER ﷼'), ('ZAR', 'ZAR R'), ('ZMW', 'ZMW ZK'),]



