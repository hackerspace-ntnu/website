FROM ubuntu:18.04

# Commit hash for website
ARG website_revision=master

# website_prod listens for website domain, website_dev listens for any server name
ARG nginx_conf=prod

# ID of application user. Should be set equal to the ID of an external user with sufficient permissions
ARG userid=1001

USER root
# Install required software
RUN apt update -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa 
RUN apt update && apt install nginx vim systemd git python3.9 python3-venv -y --no-install-recommends

# Create application user to prevent website from running as root
RUN useradd --create-home -u $userid dev
WORKDIR /home/dev/website
RUN chown -R dev: /home/dev

# Get source code
USER dev
RUN git init
RUN git remote add origin https://github.com/hackerspace-ntnu/website.git
RUN git fetch origin ${website_revision}
RUN git reset --hard FETCH_HEAD


# Install python requirements
RUN python3.9 -m venv /home/dev/env
RUN chown -R dev: /home/dev
RUN bash /home/dev/env/bin/activate
RUN pip install -r prod_requirements.txt

USER root
# Enable gunicorn service
COPY .docker_assets/gunicorn/gunicorn.service /etc/systemd/system/gunicorn.service
COPY .docker_assets/gunicorn/gunicorn.socket /etc/systemd/system/gunicorn.socket
RUN systemctl daemon-reload
RUN systemctl start gunicorn.socket
RUN systemctl enable gunicorn.socket

# Configure nginx
COPY .docker_assets/nginx/website_${nginx_conf} /etc/nginx/sites-available/website
RUN ln -s /etc/nginx/sites-available/website /etc/nginx/sites-enabled/website
RUN systemctl restart nginx

EXPOSE 80