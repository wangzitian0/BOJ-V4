# heheda

## Getting Started

Make sure you are using a virtual environment of some sort (e.g. `virtualenv` or
`pyenv`).

```
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata sites
./manage.py runserver
```
网站基本信息在fixture/sites。json里面，loaddata sites之后会自动设置

user模板被放在/heheda/templates/account

邮件模板在/heheda/templates/account/email




## 自己创建 heheda/secret_settings.py ##

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "dev.db",
    }
}

EMAIL_HOST = 'mail.bupt.edu.cn'

# Port for sending e-mail.
EMAIL_PORT = 25

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = 'xxx@bupt.edu.cn'
EMAIL_HOST_PASSWORD = 'xxx'
#EMAIL_USE_TLS = False 

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```
