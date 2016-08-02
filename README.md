# BOJv4

## Getting Started

Make sure you are using a virtual environment of some sort (e.g. `virtualenv` or
`pyenv`).

```
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata sites
```

拷贝一份私密配置，否则系统无法运行

```
cp bojv4/scr_settings.py bojv4/secret_settings.py

```

运行临时服务器查看效果
```
./manage.py runserver 0.0.0.0:8080

```

## 姿势汇总
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
