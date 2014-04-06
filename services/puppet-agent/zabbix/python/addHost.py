#!/usr/bin/env python
#-*- coding:utf-8 -*-


import sys
from zabbix_api import ZabbixAPI, Already_Exists
import argparse

server = "http://10.196.10.104/zabbix/"
username = "api"
password = "api123"

try:
    zapi = ZabbixAPI(server=server, path="", log_level=0)
    zapi.login(username, password)
except:
    sys.stderr.write('Can\'t login to Zabbix!\n')
    sys.exit(1)


def addHost(host_ip, template_ids):
    '''Adds a host with templates to Zabbix'''
    hostname = host_ip
    templates = []
    for template in template_ids:
        templates.append({'templateid': template})

    params = {
        "host": hostname,
        "interfaces": [{
            "type": 1,
            "main": 1,
            "useip": 1,
            "ip": host_ip,
            "dns": "",
            "port": "10050"
            }],
        "groups": [{"groupid": "7"}],
        "templates": templates

    }

    try:
        host = zapi.host.create(params)
    except Already_Exists as host_exists:
        sys.stderr.write('Host %(hostname)s already exists! %(exc)s\n' % {'hostname': hostname, 'exc': host_exists})
        sys.exit(1)

    return host

def removeHost(host_ip):
    '''Disables the host and changes the hostname to <previous_hostname>_disabled'''
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Handles adding/removing hosts in Zabbix')
    parser.add_argument('operation', choices=['add', 'remove'], help="Operation to perform")
    parser.add_argument('ip', default='127.0.0.1', help='Host\'s IP')
    parser.add_argument('templates', type=int, nargs='+', help='Host templates or a space seperated array of them')
    args = parser.parse_args()

    if args.operation == 'add':
        addHost(args.ip, args.templates)
    elif args.operation == 'remove':
        removeHost(args.ip)
