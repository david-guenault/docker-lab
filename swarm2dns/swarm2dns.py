#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
import json
import time
import sys
from docker import Client
import requests
from requests import exceptions
import time
import optparse
import logging
import threading
import re

class RequestSimple():

    def __init__(self,retry=None,sleep=None,timeout=2):
        self.__initRequestSimple(retry=retry,sleep=sleep,timeout=timeout)

    def __initRequestSimple(self,retry=None,sleep=None,timeout=2):
        self.retry = retry
        self.sleep = sleep
        self.timeout = timeout

    def debug(self,message):
        try:
            sys.stdout.write(str(message))
            sys.stdout.write("\n")
            sys.stdout.flush()
        except:
            pass

    def __req(self, method, uri, data = None,timeout=2):
        try:
            result = requests.request(method=method, url=uri, data=data)
            self.debug(result.text)
        except requests.exceptions.RequestException:
            self.debug("There was an ambiguous exception that occurred while handling your request.")
            self.debug(method)
            self.debug(uri)
            self.debug(str(data))
        except requests.exceptions.ConnectionError:
            self.debug("A Connection error occurred.")
            self.debug(method)
            self.debug(uri)
            self.debug(str(data))
        except requests.exceptions.HTTPError:
            self.debug("An HTTP error occurred.")
            self.debug(method)
            self.debug(uri)
            self.debug(str(data))
        except  requests.exceptions.URLRequired:
            self.debug("A valid URL is required to make a request.")
            self.debug(method)
            self.debug(uri)
            self.debug(str(data))
        except requests.exceptions.TooManyRedirects:
            self.debug("Too many redirects.")
            self.debug(method)
            self.debug(uri)
            self.debug(str(data))
        except requests.exceptions.Timeout:
            self.debug("The request timed out.")
            self.debug(method)
            self.debug(uri)
            self.debug(str(data))
        except:
            self.debug("Unknown error")
            self.debug(method)
            self.debug(uri)
            self.debug(str(data))
        return None

    def get(self,uri):
        return self.__req(method = "GET", uri = uri)

    def post(self,uri,data):
        return self.__req(method = "POST", uri = uri, data = data)

class Etcdclient():
    def __init__(self,etcd):
        self.etcdclient = None
        self.etcdadmin = None
        self.machines = None
        self.__init(etcd)
        self.req = RequestSimple(retry=2, sleep=1,timeout=2)

    def debug(self,message):
        try:
            sys.stdout.write(str(message))
            sys.stdout.write("\n")
            sys.stdout.flush()
        except:
            pass

    def __init(self,etcd):
        etcdre = r"^(https?)://([^:]+):([\d]+):([\d]+)"
        p = re.compile(etcdre)
        result = p.findall(etcd)
        if len(result) != 1:
            self.debug("Invalid etcd uri definition (%s)" % etcd)
        else:
            proto, host, client, admin = result[0]
            self.etcdclient = "%s://%s:%s" % (proto,host,client)
            self.etcdadmin = "%s://%s:%s" % (proto,host,admin)

    def getmachines(self):
        self.machines = self.req.get(uri = "%s/v2/admin/machines" % self.etcdadmin)
        if not self.machines:
            return False
        else:
            return True

    def updatestatus(self):
        self.getmachines()
        if not self.machines:
            self.debug("Unable to get cluster members")
            return False
        else:
            for record in self.machines:
                if record["state"] == "leader":
                    self.etcdclient = record["clientURL"]
                    self.etcdadmin = record["peerURL"]
            return True

# class Swarm2dns():

#     def __init__(self, socket = None, etcd = None, domain = None, ttl = 0, retry = 5, sleep = 2, debug = None, noexit = False):
#         etcdparts=etcd.split(":")
#         self.socket = socket
#         self.etcd = "%s:%s" % (etcdparts[0],etcdparts[1])
#         self.etcdadmin = "%s:%s" % (etcdparts[0],etcdparts[2])
#         self.etcdpeers = []
#         self.domain = domain
#         self.ttl = ttl
#         self.retry = int(retry)
#         self.noexit = noexit
#         self.sleep = float(sleep)
#         self.debug = debug
#         self.createClient()
#         self.nodes = []
#         self.threads = []

#     def getLeader(self):
#         if not self.etcdadmin.startswith("http"):
#             etcd="http://%s" % self.etcdadmin
#         else:
#             etcd = self.etcdadmin

#         uri = "%s/v2/admin/machines" % etcd

#         try:
#             result = json.loads(self.req("GET",uri).text)
#             self.etcdpeers = []
#             for record in result:
#                 client = record["clientURL"].split("/")[-1:][0]
#                 peer = record["peerURL"].split("/")[-1:][0]
#                 if record["state"] == "leader":
#                     self.log("Found etcd leader (client : %s, peer : %s)" % (client,peer))                    
#                     self.etcd = client
#                     self.etcdadmin = peer
#                 else:
#                     self.log("Adding follower (client : %s, peer : %s) to peers" % (client,peer))                    
#                     self.etcdpeers.append([client,peer])                    
#         except:
#             self.log("Unable to query leader on failed etcd host (client : %s, peer : %s)" % (self.etcd, self.etcdadmin))
#             alt = self.etcdpeers.pop()
#             self.etcd = alt[0]
#             self.etcdadmin = alt[0]
#             self.getLeader()

#     def createClient(self):
#         self.log("Connection to swarm daemon %s" % self.socket)
#         currentretry = 0
#         while currentretry < self.retry:
#             try:
#                 self.client =  Client(base_url = self.socket)
#                 self.nodes = self.getnodes()
#                 self.log("Connected to %s" % self.socket)
#                 currentretry = 0
#                 break
#             except:
#                 self.log("Failed to connect to swarm daemon (%s/%s)" % (currentretry, self.retry))
#                 currentretry += 1
#                 time.sleep(self.sleep)

#         if currentretry > 0:
#             self.log("Unable to connect to swarm daemon after %s retries. Exiting" % currentretry)
#             if self.noexit:
#                 self.createClient()
#             else:
#                 sys.exit(2)

#     def info(self):
#         return self.client.info()

#     def getnodes(self):
#         infos = self.info()
#         self.nodes = infos["DriverStatus"][1:]

#     def log(self,message):
#         try:
#             sys.stdout.write(str(message))
#             sys.stdout.write("\n")
#             sys.stdout.flush()
#         except:
#             pass

#     def inspect(self, id):
#         try:
#             inspect = self.client.inspect_container(id)
#             return inspect 
#         except:
#             return None

#     def req(self, method, uri, data = None):

#         payload = {}

#         if data:
#             payload["value"] = json.dumps(data)
        
#         if self.ttl:
#             payload["ttl"] = self.ttl

#         if not uri.startswith("http"):
#             uri = "http://%s" % uri

#         for r in range(self.retry):
#             try:
#                 result = requests.request(method, uri, data = payload)
#                 self.log("success posting request %s %s %s (try : %s/%s)" % (method,uri,str(payload),r+1,self.retry))
#                 return result
#                 break
#             except:
#                 self.log("Error posting request %s %s %s (try : %s/%s)" % (method,uri,str(payload),r+1,self.retry))
#                 self.log(str(sys.exc_info()))
#                 time.sleep(self.sleep)
#                 pass

#     def update(self, event):

#         # get first etcd node available and acting as a master

#         config = self.inspect(event["id"]) 


#         if not config:
#             return

#         if config["Config"]["Hostname"] != "":
#             dnsname = config["Config"]["Hostname"]
#         else:
#             dnsname = config["Name"].replace("/","")


#         method = None
#         data = None
#         uri = None

#         self.getLeader()

#         if event["status"] == "start":
#             method = "PUT"
#             hosts = []
#             for port,portdatas in config["NetworkSettings"]["Ports"].items():
#                 if portdatas:
#                     for portdata in portdatas:
#                         hosts.append(portdata["HostIp"])

#             for host in set(hosts):
#                 uri = "%s/v2/keys/skydns/%s/%s" % (self.etcd, "/".join(self.domain.split(".")[::-1]), dnsname )
#                 data = { "Host" : host }
#                 treq = threading.Thread(target = self.req, args = (method,uri,data,))
#                 treq.start()

#         elif event["status"] in ("die", "stop"):
#             uri = "%s/v2/keys/skydns/%s/%s" % (self.etcd, "/".join(self.domain.split(".")[::-1]), dnsname )
#             data = {}
#             method = "DELETE"
#             treq = threading.Thread(target = self.req, args = (method,uri,data,))
#             treq.daemon = True
#             self.threads.append(treq)
#             treq.start()
#         else:
#             pass
#             #self.log("Unhandled event %s" % (event["status"]))

#     def listen(self):
#         while True:
#             try:
#                 e = self.client.events()
#                 for data in e:
#                     eventdata = json.loads(data)
#                     self.log(eventdata)
#                     self.update(eventdata)
#             except requests.exceptions.ConnectionError, requests.packages.urllib3.exceptions.ProtocolError:
#                 print "Lost connection to swarm daemon retrying"
#                 self.createClient()
#                 self.listen()
    
if __name__ == '__main__':

    parser = optparse.OptionParser('', version="%prog ")
    # parser.add_option('--socket', dest="socket", help="""Swarm host:port""")
    parser.add_option('--etcd', dest="etcd", help="""Etcd host:portcli:portadmin""")
    # parser.add_option('--domain', dest="domain", help="""Domain on which discovered containers will be bind to (toto.tld)""")
    # parser.add_option('--debug', dest="debug", action="store_false", default=False, help="""Enable debug logging""")
    # parser.add_option('--retry', dest="retry", help="""How many retries when connection failed""", default=5)
    # parser.add_option('--sleep', dest="sleep", help="""Sleep time in seconds between retries""", default=2)
    # parser.add_option('--noexit', dest="noexit", action="store_true", default=False, help="""reset retry counter when try reach retry""")
    
    
    opts, args = parser.parse_args() 

    e = Etcdclient(opts.etcd)
    e.updatestatus()


    # e = Etcdclient()

    # d2d = Swarm2dns(
    #     socket= opts.socket, 
    #     etcd = opts.etcd, 
    #     domain = opts.domain, 
    #     ttl = None, 
    #     retry = opts.retry, 
    #     sleep = opts.sleep, 
    #     debug=opts.debug, 
    #     noexit=opts.noexit)
    
    # d2d.listen()
