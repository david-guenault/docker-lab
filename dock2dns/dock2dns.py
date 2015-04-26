#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
import json
import sys
import requests
import time
import optparse
import logging
import threading
import os
import re

from docker import Client
from docker import tls
from docker import errors


class Dock2dns():
    def __init__(self, socket=None, etcd=None, domain=None, ttl=0, retry=5, sleep=2, debug=None, tls=False, ca=False,
                 cert=False, key=False):
        self.socket = socket
        self.etcd = etcd
        self.domain = domain
        self.ttl = ttl
        self.retry = retry
        self.sleep = sleep
        self.debug = debug
        self.ca = ca
        self.key = key
        self.cert = cert
        self.tls = tls
        self.client = None
        self.connect()

    def connect(self):
        if self.tls:
            tls_config = tls.TLSConfig(client_cert=(self.cert, self.key), verify=self.ca)
            self.client = Client(base_url=self.socket, tls=tls_config)
        else:
            self.client = Client(base_url=self.socket)
        self.log(self.client)

    @staticmethod
    def log(message):
        sys.stdout.write(str(message))
        sys.stdout.write("\n")
        sys.stdout.flush()

    @staticmethod
    def loadenv():
        (proto, host, port, tlsverify, ca, key, cert) = (None, None, None, None, None, None, None)
        tlsverify = os.getenv("DOCKER_TLS_VERIFY")
        envhost = os.getenv("DOCKER_HOST")
        if envhost:
            try:
                (proto, host, port) = filter(lambda f: len(f) > 0,
                                             re.split(r"^(tcp|socket|https)://(\w+):(\d+)", envhost))
            except:
                pass
        if tlsverify:
            certpath = os.getenv("DOCKER_CERT_PATH")
            ca = "%s/ca.pem" % certpath
            cert = "%s/cert.pem" % certpath
            key = "%s/key.pem" % certpath
            proto = "https"

        return proto, host, port, tlsverify, ca, key, cert

    @staticmethod
    def resolvesocket(socket):
        (proto, host, port) = filter(lambda f: len(f) > 0, re.split(r"^(tcp|socket|https)://(\w+):(\d+)", socket))
        return proto, host, port

    def req(self, method, uri, data=None):
        self.log("Req %s %s %s" % (uri, method, data))
        payload = {}

        if data:
            payload["value"] = json.dumps(data)

        payload["ttl"] = self.ttl

        self.log("%s %s %s" % (method, uri, data))

        for r in range(self.retry):
            try:
                requests.request(method, uri, data=payload)
                break
            except:
                self.log("Error req : %s %s %s" % (method, uri, str(payload)))
                time.sleep(self.sleep)
                pass

    def update(self, event):
        pass
        #config = self.inspect(event["id"])

        # if not config:
        #     return
        #
        # if config["Config"]["Hostname"] != "":
        #     dnsname = config["Config"]["Hostname"]
        # else:
        #     dnsname = config["Name"].replace("/", "")
        #
        # uri = "%s/v2/keys/skydns/%s/%s" % (self.etcd, "/".join(self.domain.split(".")[::-1]), dnsname)
        # method = None
        # data = None
        #
        # message = "UPDATE %s %s %s" % (event["status"], dnsname, config["NetworkSettings"]["IPAddress"])
        #
        # if event["status"] == "start":
        #     data = {"Host": config["NetworkSettings"]["IPAddress"]}
        #     method = "PUT"
        # elif event["status"] in ("die", "stop"):
        #     data = {}
        #     method = "DELETE"
        #
        # if method:
        #     treq = threading.Thread(target=self.req, args=(method, uri, data,))
        #     treq.start()

    def listen(self):
        while True:
            e = self.client.events()
            for data in e:
                if data:
                    #self.log("receiving data %s" % str(data))
                    try:
                        event = json.loads(data.decode("utf-8"))
                    except:
                        self.log("Unable to load json from event %s" % str(data))
                        break
                else:
                    self.log("No data in event")
                    break

                if event["status"] in ("start", "die"):
                    # we take the event for processing
                    inspection = self.client.inspect_container(event["id"])
                    if inspection:
                        if inspection["Config"]["Hostname"] != "":
                            dnsname = inspection["Config"]["Hostname"]
                        else:
                            dnsname = inspection["Name"].replace("/", "")

                        uri = "%s/v2/keys/skydns/%s/%s" % (self.etcd, "/".join(self.domain.split(".")[::-1]), dnsname)

                        payload = {}
                        method = None

                        if event["status"] == "start":
                            payload["value"] =  json.dumps({"Host": inspection["NetworkSettings"]["IPAddress"]})
                            #payload["ttl"] = self.ttl
                            method = "PUT"
                        else:
                            payload = {}
                            method = "DELETE"

                        self.log("+-----------------------------------------------------------------------------------")
                        self.log(uri)
                        self.log(json.dumps(payload))
                        self.log(method)

                        try:
                            requests.request(method, uri, data=payload)
                        except:
                            self.log("Unable to query etcd")

                        self.log("+-----------------------------------------------------------------------------------")


if __name__ == '__main__':

    logger = logging.getLogger('dock2dns')
    logger.setLevel(logging.DEBUG)

    parser = optparse.OptionParser('', version="%prog ")
    parser.add_option(
        '--socket',
        dest="socket",
        help="""Docker daemon socket uri (unix://var/run/docker.sock or https://host:port)""")
    parser.add_option('--etcd', dest="etcd", help="""Etcd store uri (http://172.17.42.1:4001)""")
    parser.add_option('--domain', dest="domain",
                      help="""Domain on which discovered containers will be bind to (toto.tld)""")
    # parser.add_option('--debug', dest="debug", action="store_true", default=False, help="""Enable debug logging""")

    # only for TLS (optional)
    parser.add_option('--tls', dest="tls", action="store_true", default=False, help="""Enable TLS verification""")
    parser.add_option('--ca', dest="ca", help="""CA file""")
    parser.add_option('--cert', dest="cert", help="""Certificate file""")
    parser.add_option('--key', dest="key", help="""Key file""")

    opts, args = parser.parse_args()

    # by default get host and tls config from docker environment variables
    # (PROTO, HOST, PORT, TLSVERIFY, CA, KEY, CERT) = Dock2dns.loadenv()

    DEBUG = False

    if tls:
        TLSVERIFY = True
        CA = opts.ca
        CERT = opts.cert
        KEY = opts.key
    else:
        (TLSVERIFY, CA, KEY, CERT) = (False, False, False, False)

    if opts.socket:
        PROTO, HOST, PORT = Dock2dns.resolvesocket(opts.socket)
        if PROTO == "tcp" or PROTO == "https":
            SOCKET = "https://%s:%s" % (HOST, PORT)
        else:
            SOCKET = opts.socket
    else:
        Dock2dns.log("SOCKET is mandatory")
        sys.exit(2)

    if opts.etcd:
        ETCD = opts.etcd
    else:
        ETCD = "http://172.17.42.1:4001"

    if opts.domain:
        DOMAIN = opts.domain
    else:
        DOMAIN = "dock2dns.lan"

    TTL = None

    d2d = Dock2dns(
        socket=SOCKET,
        etcd=ETCD,
        domain=DOMAIN,
        ttl=5,
        retry=5,
        sleep=2,
        debug=DEBUG,
        tls=TLSVERIFY,
        ca=CA,
        cert=CERT,
        key=KEY)

    d2d.listen()
