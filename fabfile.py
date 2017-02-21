from fabric.api import env, run, cd

env.hosts = ['hackerspace-ntnu.no']
root_folder = '/devops/docker-services/'
projects = {
        'potet': {
            'repo_folder': 'website'
        },
        'prod': {
            'repo_folder': 'website'
        }
}

def pull():
    with cd(root_folder):
        run('git pull')

def deploy(project, ref='master'):
    with cd(root_folder + project + '/' + projects[project]['repo_folder'] + '/'):
        run('git fetch --all')
        run('git checkout {0}'.format(ref))
        run('git reset --hard origin/{0}'.format(ref))
    with cd(root_folder+project):
        run('docker-compose stop website proxy')
        run('docker-compose rm website proxy')
        run('docker-compose build website proxy')
        run('docker-compose up -d website proxy')


def deploycommit(project, commit):
    with cd(root_folder + project + '/' + projects[project]['repo_folder'] + '/'):
        run('git fetch --all')
        run('git checkout {0}'.format(commit))
    with cd(root_folder+project):
        run('docker-compose build website')
        run('docker-compose up -d website proxy')
