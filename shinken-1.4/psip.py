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
import yaml 
import re
import os

class figproject():

    def __init__(self, file = None, socket = None, project = None):
        self.file = file
        self.socket = socket
        self.client =  Client(base_url = self.socket)

        if not project:
            self.project  = self.loadProject() 
        else:
            self.project = project

        self.projectname = re.sub("[^\w]","",os.path.abspath(os.path.dirname(sys.argv[0])).split("/")[-1])

    def log(self,message):
        try:
            sys.stdout.write(message)
            sys.stdout.write("\n")
            sys.stdout.flush()
        except:
            pass

    def loadProject(self):
        stream = file(self.file)
        return yaml.load(stream)  

    def inspect(self, id):
        try:
            inspect = self.client.inspect_container(id)
            return inspect 
        except:
            return None

    def showIP(self):

        containers = self.client.containers()

        projectcontainers = []

        self.log("+%s+%s+%s+" % (40*"-",20*"-",15*"-"))
        self.log("|%40s|%20s|%15s|" % ("Container Name","Name","IP"))
        self.log("+%s+%s+%s+" % (40*"-",20*"-",15*"-"))
        for container in containers:
            for name in container["Names"]:
                if name.startswith("/%s" % self.projectname) and not ":" in name and name.count("/") == 1:
                    ip = self.inspect(container["Id"])["NetworkSettings"]["IPAddress"]
                    self.log("|%40s|%20s|%15s|" % (name[1:], name.split("_")[1], ip))
        self.log("+%s+%s+%s+" % (40*"-",20*"-",15*"-"))

    
if __name__ == '__main__':

    logger = logging.getLogger('dock2dns')
    logger.setLevel(logging.DEBUG)

    parser = optparse.OptionParser('', version="%prog ")
    parser.add_option('--file', dest="file", help="""fig.yml project file""",default="fig.yml")
    parser.add_option('--socket', dest="socket", help="""fig.yml project file""", default="unix://var/run/docker.sock")
    parser.add_option("--project", dest="project", help="""project name""", default=None)
   
    opts, args = parser.parse_args() 

    if opts.file:
        FILE = opts.file

    if opts.project:
        PROJECT = opts.project
    else:
        PROJECT = None

    if opts.socket:
        SOCKET = opts.socket

    f = figproject(file = FILE, socket = SOCKET, project = PROJECT)
    f.showIP()
