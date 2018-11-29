#!/usr/bin/env python

import dns.resolver
import re
import requests


login = ''
password = ''
host = ''


def get_current_ip():
    r = requests.get("http://checkip.dyndns.com")
    matches = re.findall(r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', r.text)
    if (len(matches)):
        return matches[0]
    return False


def get_host_ip(host):
    myResolver = dns.resolver.Resolver()
    myAnswers = myResolver.query(host, "A")
    try:
        ip = str(myAnswers[0])
    except:
        ip = ''
    return ip


def update_dnsexit(login, password, host, myip):
    url = "https://www.dnsexit.com/RemoteUpdate.sv"
    params = {
        'login': login,
        'password': password,
        'host': host,
        'myip': myip
    }
    return requests.get(url, params=params)


def update_if_needed(login, password, host):
    ip = get_current_ip()
    set_ip = get_host_ip(host)
    if (ip != set_ip):
        result = update_dnsexit(login, password, host, ip)
        print(result.text)


if __name__ == "__main__":
    update_if_needed(login, password, host)
