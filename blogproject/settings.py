"""
Django settings for blogproject project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR 是 settings.py 在配置开头前面定义的变量，记录的是工程根目录 blogproject\ 的值（注意是最外层的 blogproject\ 目录）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k45wv%%@!dj3@5d6rw)uznp7zybeax_ypq-t#xqmqx4y$_6z^*'

# SECURITY WARNING: don't run with debug turned on in production!
# 注释掉
# DEBUG = True
# 注释掉
# ALLOWED_HOSTS = []

# 增加
# import socket

# SITE_ID = 1

# 项目的根目录
# 简化后面的操作
# PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

# 得到主机名
# def hostname():
#     sys = os.name
#     if sys == 'nt':
#         hostname = os.getenv('computername')
#         return hostname
#
#     elif sys == 'posix':
#         host = os.popen('echo $HOSTNAME')
#         try:
#             hostname = host.read()
#             return hostname
#         finally:
#             host.close()
#     else:
#         raise RuntimeError('Unkwon hostname')

#调试和模板调试配置
#主机名相同则为开发环境，不同则为部署环境
#ALLOWED_HOSTS只在调试环境中才能为空
# if socket.gethostname().lower() == hostname().lower():
#     DEBUG = TEMPLATE_DEBUG = True
#     ALLOWED_HOSTS = []
# else:
    # ALLOWED_HOSTS 是允许访问的域名列表，域名前加一个点表示允许访问该域名下的子域名，比如 www.zmrenwu.com、test.zmrenwu.com 等二级域名同样允许访问。如果不加前面的点则只允许访问 zmrenwu.com。
    # ALLOWED_HOSTS = [
    #     '.277127311.top',
    #     '127.0.0.1',
    #     'localhost ',
    # ]
    # DEBUG = TEMPLATE_DEBUG = False

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost ', '.277127311.top']


#数据库配置
MYDB = {
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'books',  #你的数据库名称
        'USER': 'root',  #你的数据库用户名
        'PASSWORD': '',  #你的数据库密码
        'HOST': '',  #你的数据库主机，留空默认为localhost
        'PORT': '3306',  #你的数据库端口
    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 'NAME': os.path.join(PROJECT_ROOT, 'db/db.sqlite3').replace('\\', '/'),
    }
}

#数据库配置
DATABASES = {
    'default': MYDB.get('sqlite'),
}





# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'comments',# 评论
    'haystack',# 提供搜索功能的 django 第三方应用
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

ROOT_URLCONF = 'blogproject.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'blogproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
# 给静态文件url一个后缀，在templates里用到的。
# 映射到静态文件的url
#  STATIC_URL的含义与MEDIA_URL类似
STATIC_URL = '/static/'
# STATIC_ROOT 指明了静态文件的收集目录，即项目根目录（BASE_DIR）下的 static 文件夹。
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# 总的static目录
# 可以使用命令 manage.py collectstatic 自动把所有静态文件全部复制到STATIC_ROOT中
# 如果开启了admin，这一步是很必要的，不然部署到生产环境的时候会找不到样式文件
# 不要把你项目的静态文件放到这个目录。这个目录只有在运行manage.py collectstatic时才会用到
# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')


# HAYSTACK_CONNECTIONS 的 ENGINE 指定了 django haystack 使用的搜索引擎，这里我们使用了 blog.whoosh_cn_backend.WhooshEngine
# PATH 指定了索引文件需要存放的位置，我们设置为项目根目录 BASE_DIR 下的 whoosh_index 文件夹（在建立索引时会自动创建）。
# HAYSTACK_SEARCH_RESULTS_PER_PAGE 指定如何对搜索结果分页，这里设置为每 10 项结果为一页。
# HAYSTACK_SIGNAL_PROCESSOR 指定什么时候更新索引，这里我们使用 haystack.signals.RealtimeSignalProcessor，作用是每当有文章更新时就更新索引。由于博客文章更新不会太频繁，因此实时更新没有问题。
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'blog.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
