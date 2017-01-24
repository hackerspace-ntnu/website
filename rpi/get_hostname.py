import requests
import uuid
import json
import os

RPI_SERVER = 'http://localhost:8000'
RPI_SECRET_KEY = 'topkeklol'


def get_mac():
    mac_addr = hex(uuid.getnode()).replace('0x', '')
    return ':'.join(mac_addr[i: i + 2] for i in range(0, 11, 2))


def get_hostname():
    url = RPI_SERVER + '/rpi/api/'
    client = requests.session()
    client.get(RPI_SERVER + '/admin/login/')
    csrftoken = client.cookies['csrftoken']
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': RPI_SERVER + '/admin',
    }
    mac = get_mac()
    data = {
        'mac_address': mac,
        'csrfmiddlewaretoken': csrftoken,
        'secret_key': 'topkeklol'
    }
    try:
        hostname = json.loads(client.post(url, headers=headers, data=data).text)['name']  # Laster hele json-strengen
        return hostname
    except json.decoder.JSONDecodeError:
        return None


if __name__ == '__main__':
    hostname = get_hostname()
    if hostname == None:
        exit()
    os.system("hostname {}".format(hostname))
    print("Setting hostname to {}".format(hostname))
    # Legg til ny bruker med samme navn som hostname
    os.system("sudo useradd -g users -p hackerspace -s /bin/bash -m {}".format(hostname[::-1], hostname))
    #  Fjern login for root
    os.system("sudo usermod -s /bin/nologin root")
    #  Slett en brukerkonto
    # os.system("sudo userdel --remove test")
