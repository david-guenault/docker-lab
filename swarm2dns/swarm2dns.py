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
import threading

class Swarm2dns():

    def __init__(self, socket = None, etcd = None, domain = None, ttl = 0, retry = 5, sleep = 2, debug = None):
        self.socket = socket
        self.etcd = etcd
        self.domain = domain
        self.ttl = ttl
        self.retry = retry
        self.sleep = float(sleep)
        self.debug = debug
        self.createClient()
        self.nodes = []

    def createClient(self):
        self.log("Connection to swarm daemon %s" % self.socket)
        currentretry = 0
        while currentretry < self.retry:
            try:
                self.client =  Client(base_url = self.socket)
                self.nodes = self.getnodes()
                self.log("Connected to %s" % self.socket)
                currentretry = 0
                break
            except:
                self.log("Failed to connect to swarm daemon (%s/%s)" % (currentretry, self.retry))
                currentretry += 1
                time.sleep(self.sleep)

        if currentretry > 0:
            self.log("Unable to connect to swarm daemon after %s retries. Exiting" % currentretry)
            sys.exit(2)

    def info(self):
        return self.client.info()

    def getnodes(self):
        infos = self.info()
        self.nodes = infos["DriverStatus"][1:]

    def log(self,message):
        try:
            sys.stdout.write(str(message))
            sys.stdout.write("\n")
            sys.stdout.flush()
        except:
            pass

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

        self.log("%s %s %s" % (method,uri,data))

        for r in range(self.retry):   
            try:
                r = requests.request(method, uri, data = payload)
                break
            except:
                time.sleep(self.sleep)
                pass

    def update(self, event):

        # get first etcd node available and acting as a master

        config = self.inspect(event["id"]) 


        if not config:
            return

        if config["Config"]["Hostname"] != "":
            dnsname = config["Config"]["Hostname"]
        else:
            dnsname = config["Name"].replace("/","")

        print dnsname

        # uri = "%s/v2/keys/skydns/%s/%s" % (self.etcd, "/".join(self.domain.split(".")[::-1]), dnsname )

        method = None
        data = None


        if event["status"] == "start":
            method = "PUT"
        

            # data = { "Host" : config["NetworkSettings"]["IPAddress"] }

            # prepare to add public dns entries
            hosts = []
            for port,portdatas in config["NetworkSettings"]["Ports"].items():
                for portdata in portdatas:
                    hosts.append(portdata["HostIp"])

            for host in set(hosts):
                publicuri = "%s/v2/keys/skydns/%s/%s" % (self.etcd, "/".join(self.domain.split(".")[::-1]), dnsname )
                data = { "Host" : host }

                print "%s %s %s" % (method, publicuri, str(data))

            # # private uri
            # privateuri = "%s/v2/keys/skydns/%s/%s" % (self.etcd, "/".join(self.domain.split(".")[::-1]), dnsname )
            # print host, privateuri


        elif event["status"] in ("die", "stop"):
            data = {}
            method = "DELETE"

        
        # message = "UPDATE %s %s %s" % (event["status"], dnsname, config["NetworkSettings"]["IPAddress"])
        # self.log(message)
        # if method:

        #     message = "%s %s %s" % (method,uri,str(data))
        #     self.log(message)
        
        # if method:
        #     treq = threading.Thread(target = self.req, args = (method,uri,data,))
        #     treq.start()

    def listen(self):
        while True:
            try:
                e = self.client.events()
                for data in e:
                    eventdata = json.loads(data)
                    self.update(eventdata)
            except requests.exceptions.ConnectionError:
                print "Lost connection to swarm daemon retrying"
                self.createClient()
                self.listen()
    
if __name__ == '__main__':

    logger = logging.getLogger('dock2dns')
    logger.setLevel(logging.DEBUG)

    parser = optparse.OptionParser('', version="%prog ")
    parser.add_option('--socket', dest="socket", help="""Swarm host:port""")
    parser.add_option('--etcd', dest="etcd", help="""Etcd host:port""")
    parser.add_option('--domain', dest="domain", help="""Domain on which discovered containers will be bind to (toto.tld)""")
    parser.add_option('--debug', dest="debug", action="store_false", default=False, help="""Enable debug logging""")
    parser.add_option('--retry', dest="retry", help="""How many retries when connection failed""", default=5)
    parser.add_option('--sleep', dest="sleep", help="""Sleep time in seconds between retries""", default=2)
    
    
    opts, args = parser.parse_args() 

    if opts.socket:
        SOCKET = opts.socket
    else:
        SOCKET = "tcp://localhost:2376"

    if opts.etcd:
        ETCD = opts.etcd
    else:
        ETCD = "http://localhost:4001"

    if opts.domain:
        DOMAIN = opts.domain
    else:
        DOMAIN = "doc2dns.lan"

    DEBUG = opts.debug

    TTL = None 

    d2d = Swarm2dns(socket= SOCKET, etcd = ETCD, domain = DOMAIN, ttl = None, retry = opts.retry, sleep = opts.sleep, debug=DEBUG)
    d2d.listen()
