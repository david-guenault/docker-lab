#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
import json
import time
import sys
from docker import Client
import requests
import time
import optparse
import logging


class Dock2dns():

    def __init__(self, socket = None, etcd = None, domain = None, ttl = 0, retry = 5, sleep = 2):
        self.socket = socket
        self.etcd = etcd
        self.domain = domain
        self.ttl = ttl
        self.retry = retry
        self.sleep = sleep
        self.client =  Client(base_url = self.socket)

    def inspect(self, id):
        try:
            inspect = self.client.inspect_container(id)
            return inspect 
        except:
            return None

    def req(self, method, uri, data = None):

        payload = {}

        if data:
            payload["value"] = json.dumps(data)
        
        payload["ttl"] = self.ttl

        for r in range(self.retry):   
            try:
                print method, uri, payload 
                r = requests.request(method, uri, data = payload)
                break
            except:
                time.sleep(self.sleep)
                pass

    def update(self, event):
        config = self.inspect(event["id"]) 

        if not config:
            return

        if config["Config"]["Hostname"] != "":
            dnsname = config["Config"]["Hostname"]
        else:
            dnsname = config["Name"].replace("/","")

        uri="%s/v2/keys/skydns/%s/%s" % (self.etcd, "/".join(self.domain.split(".")[::-1]), dnsname )

        if event["status"] == "start":
            data = { "Host" : config["NetworkSettings"]["IPAddress"] }
            self.req('PUT', uri, data = data)
        elif event["status"] in ("die", "stop"):
            self.req('DELETE', uri)
            pass

    def listen(self):
        while True:
            e = self.client.events()
            for data in e:
                eventdata = json.loads(data)
                self.update(eventdata)
    
if __name__ == '__main__':

    logger = logging.getLogger('dock2dns')
    logger.setLevel(logging.DEBUG)

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

    d2d = Dock2dns(socket = SOCKET, etcd = ETCD, domain = DOMAIN, ttl = None, retry = 5, sleep = 2)
    d2d.listen()
