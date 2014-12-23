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
            project = os.path.abspath(os.path.dirname(sys.argv[0]))

        self.setpath(file,project)        


    def setpath(self, file, project):
        
        if not os.path.exists(project):
            self.log("Project %s not found" % project)
            sys.exit(2)

        if not os.path.isdir(project):
            self.log("Project %s is not a folder" % project)
            sys.exit(2)


        self.projectpath = os.path.abspath(project)
        self.projectname = re.sub("[^\w]","",self.projectpath.split("/")[-1])

        if not os.path.exists("%s/%s" % (self.projectpath, file)):
            self.log("Project file %s/%s does not exist" % (self.projectpath, file))
            sys.exit(2)
        else:
            self.file = "%s/%s" % (self.projectpath, file)


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

        self.log("Project : %s" % self.projectname)

        self.log("+%s+%s+%s+" % (40*"-",20*"-",15*"-"))
        self.log("|%40s|%20s|%15s|" % ("Container Name","Name","IP"))
        self.log("+%s+%s+%s+" % (40*"-",20*"-",15*"-"))
        for container in containers:
            for name in container["Names"]:
                if name.startswith("/%s" % self.projectname) and not ":" in name and name.count("/") == 1:
                    ip = self.inspect(container["Id"])["NetworkSettings"]["IPAddress"]
                    self.log("|%40s|%20s|%15s|" % (name[1:], name.split("_")[1], ip))
        self.log("+%s+%s+%s+" % (40*"-",20*"-",15*"-"))

def help():
    print "Display ip addresses of a fig project"
    
if __name__ == '__main__':

    logger = logging.getLogger('dock2dns')
    logger.setLevel(logging.DEBUG)

    cmd = "usage: %prog [--project=project folder] [--file=fig project file] [--socket=docker socket path or uri]"

    parser = optparse.OptionParser(version="%prog ", usage=cmd, description="Display ip addresses of fig project running containers")
    parser.add_option('--file', dest="file", help="""fig project file""",default="fig.yml")
    parser.add_option('--socket', dest="socket", help="""docker socket""", default="unix://var/run/docker.sock")
    parser.add_option("--project", dest="project", help="""project path""", default=None)
   
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
