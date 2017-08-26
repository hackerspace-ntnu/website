from fabric.api import env, run, cd
from fabric.context_managers import prefix
from fabric.operations import sudo

env.hosts = ['hackerspace-ntnu.no']
root_folder = '/devops/'
project_folder = '/website'


def deploy(project='prod', branch='master'):
    git(project, branch)
    requirements(project)
    django(project)
    gunicorn(project)
    nginx()


def git(project='prod', branch='master'):
    with cd(root_folder + project + project_folder):
        sudo('git stash', user='git')
        sudo('git fetch --all', user='git')
        sudo('git checkout %s' % branch, user='git')
        sudo('git reset --hard origin/%s' % branch, user='git')


def requirements(project='prod'):
    with cd(root_folder + project + project_folder), prefix('. ../%senv/bin/activate' % project):
        run('pip install -r requirements.txt')
        run('pip install -r prod_requirements.txt')


def django(project='prod'):
    with cd(root_folder + project + project_folder), prefix('. ../%senv/bin/activate' % project):
        run('python manage.py makemigrations')
        run('python manage.py migrate')
        run('python manage.py collectstatic --no-input')


def gunicorn(project='prod'):
    sudo('systemctl restart %s' % project)


def nginx():
    sudo('systemctl restart nginx')


def restart(project='prod'):
    gunicorn(project)
    nginx()
