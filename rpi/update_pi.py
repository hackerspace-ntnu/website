import requests, os, uuid

RPI_SERVER = "http://localhost:8000"


def get_mac():
    mac_addr = hex(uuid.getnode()).replace('0x', '')
    return ":".join(mac_addr[i: i + 2] for i in range(0, 11, 2))


def get_hostname():
    url = RPI_SERVER + "/rpi/lifesign"
    client = requests.session()
    client.get(RPI_SERVER + "/admin/login/")
    csrftoken = client.cookies['csrftoken']
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": RPI_SERVER + "/admin",
    }
    mac = get_mac()
    data = {
        "mac_address": mac,
        "csrfmiddlewaretoken": csrftoken
    }
    hostname = client.post(url, headers=headers, data=data).text
    print(hostname)
    return hostname if 10 > len(hostname) > 0 else None


if __name__ == "__main__":
    get_hostname()
