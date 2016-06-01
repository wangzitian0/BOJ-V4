# BOJv4

## Getting Started

Make sure you are using a virtual environment of some sort (e.g. `virtualenv` or
`pyenv`).

```
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata sites
./manage.py runserver
```

vi bojv4/secret_settings.py

```
EMAIL_HOST = 'mail.bupt.edu.cn'
EMAIL_PORT = 25

EMAIL_HOST_USER = 'wangzitian0@bupt.edu.cn'
EMAIL_HOST_PASSWORD = ''

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
```

姿势汇总
```
TemplateView实现多个表单的验证
ojuser/views.py
class GroupUpdateView(TemplateView):
```
权限控制最重要的接口
```
https://django-guardian.readthedocs.org/en/stable/api/guardian.shortcuts.html
```
向表单里面添加非fields的值
```
ojuser/forms.py
class GroupProfileForm(forms.ModelForm):
```
