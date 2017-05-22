BOJv4
===

## Getting Started

### Basic lib

```
sudo apt-get install libjpeg-turbo8-dev zlib1g-dev python-pip
```
### Virtual environment

Make sure you are using a virtual environment of some sort (e.g. `virtualenv` or
`pyenv`).

```
cat >> prepare.sh << EOF
pip install virtualenv
mkdir BOJ
cd BOJ
virtualenv --no-site-packages venv
EOF
chmod +x prepare.sh
./prepare.sh
```

### Clone the project

```
source venv/bin/activate
git clone https://github.com/BUPT-OJ-V4/BOJ-V4.git
cd BOJ-V4
pip install -r requirements.txt 
cp bojv4/scr_settings.py bojv4/secret_settings.py  # 拷贝一份私密配置，否则系统无法运行
```

### Run the project

Make sure you get root permissions.

```        
mkdir -p /var/log/oj
./manage.py migrate
./manage.py loaddata sites
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
- 权限控制最重要的接口
```
https://django-guardian.readthedocs.org/en/stable/api/guardian.shortcuts.html
```
- 向表单里面添加非fields的值
```
ojuser/forms.py
class GroupProfileForm(forms.ModelForm):
```

- 后台进程管理
    - 包括redis\nsq\django-server\judge\judge-result等
```
sudo supervisorctl #查看管理进程
```
