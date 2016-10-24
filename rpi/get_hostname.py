import requests, os, uuid

def get_mac():
    mac_addr = hex(uuid.getnode()).replace('0x','')
    return ":".join(mac_addr[i: i+2] for i in range(0,11,2))

def get_hostname():
    url = "http://localhost:8000/rpi/add"
    client = requests.session()
    client.get("http://localhost:8000/admin/login/")
    csrftoken = client.cookies['csrftoken']
    headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer":"http://localhost:8000/admin",
            }
    data = {
        "mac": get_mac(),
        "csrfmiddlewaretoken":csrftoken
    }
    hostname = client.post(url, headers=headers, data=data).text
    print(hostname)
    return hostname if 10 > len(hostname) > 0 else None

if __name__ == "__main__":
    hostname = get_hostname()
    if hostname==None:
        exit()
    #os.system("hostname {}".format(hostname))
    print("Setting hostname to {}".format(hostname))
    # Legg til ny bruker med samme navn som hostname
    #os.system("sudo useradd -g users -p tset -s /bin/bash -m test")#{} -s /bin/bash -m {}".format(hostname[::-1],hostname))
    # Fjern login for root
    #os.system("sudo usermod -s /bin/nologin test")#root")
    # Slett en brukerkonto
    # os.system("sudo userdel --remove test")
