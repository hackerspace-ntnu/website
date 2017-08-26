from fabric.api import env, run, cd, abort
from fabric.operations import sudo

env.hosts = ['secrets.nsa.gov']
root_folder = '/devops/containers/'

def init():
    sudo('mkdir -p %s' % root_folder)
    sudo('touch %s/.env' % root_folder)
    install_nginx()
    install_letsencrypt()

def install_letsencrypt():
    sudo('apt-get update')
    sudo('apt-get install software-properties-common')
    sudo('add-apt-repository ppa:certbot/certbot')
    sudo('apt-get update')
    sudo('apt-get install python-certbot-nginx ')

    sudo("ufw allow 'Nginx Full'")
    sudo("ufw delete allow 'Nginx HTTP'")

    sudo('openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048')

def create_certificate(subdomain, domains=('hackerspace-ntnu.no', 'hackerspace.idi.ntnu.no')):
    cert_domains = []
    for domain in domains:
        cert_domains.append('%s.%s' % (subdomain, domain))
        cert_domains.append('www.%s.%s' % (subdomain, domain))
    cert_str = ''.join([' -d %s' % cert_domain for cert_domain in cert_domains])
    sudo('certbot certonly --webroot-path /var/www/html %s' % cert_str)

def create_server(name='test'):
    with cd(root_folder):
        sudo('mkdir ' + name)
        with cd(root_folder + name):
            sudo('git clone https://github.com/hackerspace-ntnu/docker-services.git')
            sudo('git clone https://github.com/hackerspace-ntnu/website.git')
            sudo('cp ' + root_folder + '.env docker-services')
            update_nginx(name)
            create_certificate(name)
            updateserver(name)
            with cd(root_folder + name + '/docker-services'):
                run('docker-compose docker-compose.yml up -d')

def update_nginx(name='test'):
    pass

def install_nginx():
    pass

def update_server(name='test'):
    pass

def delete_server(name='test'):
    with cd(root_folder):
        sudo('rm -rf '+name)
