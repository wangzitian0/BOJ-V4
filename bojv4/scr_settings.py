EMAIL_HOST = 'mail.bupt.edu.cn'
EMAIL_PORT = 25

EMAIL_HOST_USER = 'wangzitian0@bupt.edu.cn'
EMAIL_HOST_PASSWORD = 'gg'

#  EMAIL_USE_TLS = False

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Make this unique, and don't share it with anybody.
SECRET_KEY = "=q_e%)utjhv5y*c3rp5uk8xqeo6(1an$w)=7$)wa2+-h=d8q)u"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "dev.db",
    }
}
