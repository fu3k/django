#######################################################################################
#mysite
-----mysite/settings.py------------------------------------------------------
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

#######################################################################################
#mysite
-----webapp/settings.py------------------------------------------------------
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'techie.apps.TechieConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'webapp',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST':'localhost',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'techie/static')
    ]
STATIC_ROOT=os.path.join(BASE_DIR,'assets')

MEDIA_URL='/MEDIA/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')

######################################################################################################
#
