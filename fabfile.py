from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, sudo


env.user='elder'
env.hosts=['10.105.242.83:22']
env.password='qwerty123456'

def deploy():
    run('cd ~ && python Login.py')
    if exists('~/BOJ-V4/.git'):
        sudo('cd ~/BOJ-V4 && git pull origin master')
    else:
        sudo('cd ~ && git clone git@github.com:BUPT-OJ-V4/BOJ-V4.git')
        sudo('cd ~/BOJ-V4 && pip install -r requirements.txt')

    run('cd ~ && python Logout.py')




