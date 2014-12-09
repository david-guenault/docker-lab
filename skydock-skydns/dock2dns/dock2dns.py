#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
import json
import time
import sys
from docker import Client
import requests
import time
import optparse

def inspect(id):
    try:
        inspect = client.inspect_container(id)
        return inspect 
    except:
        return None

def req(method,uri,data = None, ttl = None ,retry=5,sleep=2):

    payload = {}

    if data:
        payload["value"] = json.dumps(data)
    if ttl:
        payload["ttl"] = ttl

    for r in range(retry):   
        try:
            print method, uri, payload 
            r = requests.request(method, uri, data = payload)
            break
        except:
            time.sleep(sleep)
            pass

def update(event):
    config = inspect(event["id"]) 

    if not config:
        return

    if config["Config"]["Hostname"] != "":
        dnsname = config["Config"]["Hostname"]
    else:
        dnsname = config["Name"].replace("/","")

    uri="%s/v2/keys/skydns/%s/%s" % (ETCD, "/".join(DOMAIN.split(".")[::-1]), dnsname )

    if event["status"] == "start":
        data = { "Host" : config["NetworkSettings"]["IPAddress"] }
        req('PUT', uri, data = data, ttl = TTL)
    elif event["status"] in ("die", "stop"):
        req('DELETE', uri)
        pass

def listen(client=None,domain=None):
    if not client or not domain:
        print "No client or domain defined"
        return False

    while True:
        e = client.events()
        for data in e:
            eventdata = json.loads(data)
            update(eventdata)
    
if __name__ == '__main__':

    parser = optparse.OptionParser('', version="%prog ")
    parser.add_option('--socket', dest="socket", help="""Docker daemon socket uri (unix://var/run/docker.sock)""")
    parser.add_option('--etcd', dest="etcd", help="""Etcd store uri (http://172.17.42.1:4001)""")
    parser.add_option('--domain', dest="domain", help="""Domain on which discovered containers will be bind to (toto.tld)""")
   
    opts, args = parser.parse_args() 

    if opts.socket:
        SOCKET = opts.socket
    else:
        SOCKET = "unix://var/run/docker.sock"

    if opts.etcd:
        ETCD = opts.etcd
    else:
        ETCD = "http://172.17.42.1:4001"

    if opts.domain:
        DOMAIN = opts.domain
    else:
        DOMAIN = "dock2dns.lan"

    TTL = None 

    client = Client(base_url = SOCKET)
    listen(client,DOMAIN)    
