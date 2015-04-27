#! /usr/bin/env python
from docker import Client
from docker import tls
from optparse import OptionParser
import json
import sys
import time

UNKNOWN = 3
OK = 0
CRITICAL = 2
WARNING = 1
client = None
containers = None


def connect(proto, host, port, usetls=False, cert=None, key=None, ca=None):
    uri = "%s://%s:%s" % (proto, host, port)
    if options.usetls:
        tls_config = tls.TLSConfig(client_cert=(cert, key), verify=ca)
    else:
        tls_config = None

    return Client(base_url=uri, tls=tls_config)


def log(message):
    sys.stdout.write("%s\n" % str(message))
    sys.stdout.flush()


def getContainerByName(name):
    container = None

    for c in containers:
        for cname in c["Names"]:
            if cname == "/%s" % name:
                return c

    return container


def getStats(Id):
    statobject = client.stats(Id)
    stats = {}
    for s in statobject:
         stats = json.loads(s)
         break
    return stats


def getCpu(container,warn, crit, wait):

    stats1 = getStats(container["Id"])
    time.sleep(wait)
    stats2 = getStats(container["Id"])

    deltacpu = float(stats2["cpu_stats"]["cpu_usage"]["total_usage"]) - float(stats1["cpu_stats"]["cpu_usage"]["total_usage"])
    deltasystem = float(stats2["cpu_stats"]["system_cpu_usage"]) - float(stats1["cpu_stats"]["system_cpu_usage"])

    cpupercent = 0

    if deltacpu > 0 and deltasystem > 0:
        cpupercent = (float(deltacpu) / float(deltasystem)) * float(len(stats1["cpu_stats"]["cpu_usage"]["percpu_usage"])) * float(100)

    if cpupercent < warn:
        code = OK
        message = "cpu usage"

    if warn <= cpupercent <= crit:
        code = WARNING
        message = "cpu usage is %d%%" % (cpupercent)

    if int(cpupercent) > crit:
        code = CRITICAL
        message = "cpu usage is %d%%" % (cpupercent)

    perfdata="cpu_usage=%d%%;%d;%d;0;100" % (cpupercent,warn,crit)

    cpu = {
        "code" : code,
        "message" : message,
        "perfdata" : perfdata
    }

    return cpu

def getNet(container,warn, crit, wait=5, unit="K"):

    stats1 = getStats(container["Id"])
    time.sleep(wait)
    stats2 = getStats(container["Id"])

    bandwidthrx = (float(stats2["network"]["rx_bytes"]) - float(stats1["network"]["rx_bytes"])) / float(wait)
    bandwidthtx = (float(stats2["network"]["tx_bytes"]) - float(stats1["network"]["tx_bytes"])) / float(wait)


    if unit == "B":
        unit = "Bps"
    elif unit == "K":
        bandwidthrx = bandwidthrx / float(1024)
        bandwidthtx = bandwidthrx / float(1024)
        unit = "KBps"
    elif unit == "M":
        bandwidthrx = bandwidthrx / float(1024) / float(1024)
        bandwidthtx = bandwidthrx / float(1024) / float(1024)
        unit = "MBps"
    else:
        unit = "Bps"

    messages=[]

    if bandwidthrx < warn and bandwidthtx < warn:
        code = OK
        messages.append("Net usage")
    else:
        if bandwidthrx >= warn and bandwidthrx <= crit:
            messages.append("RX bandwidth threshold is warning")
            code = WARNING

        if bandwidthtx >= warn and bandwidthtx <= crit:
            messages.append("TX bandwidth threshold is warning")
            code = WARNING

        if bandwidthrx > crit:
            messages.append("RX bandwidth threshold is critical")
            code = CRITICAL

        if bandwidthtx > crit:
            messages.append("TX bandwidth threshold is critical")
            code= CRITICAL

    message = ", ".join(messages)

    perfdata="net_usage_rx=%d%s;%d;%d net_usage_tx=%d%s;%d;%d" % (bandwidthrx, unit, warn, crit, bandwidthtx, unit, warn, crit)

    net = {
        "code" : code,
        "message" : message,
        "perfdata" : perfdata
    }

    return net



def getMemory(container, warn, crit):
    stats = getStats(container["Id"])

    memorypercent=float(stats["memory_stats"]["usage"]*float(100))/float(stats["memory_stats"]["limit"])

    if memorypercent < warn:
        code = OK
        message = "memory usage"

    if warn <= memorypercent <= crit:
        code = WARNING
        message = "memory usage is %d%%" % (memorypercent)

    if int(memorypercent) > crit:
        code = CRITICAL
        message = "memory usage is %d%%" % (memorypercent)

    perfdata="memory_usage=%d%%;%d;%d;0;100" % (memorypercent,warn,crit)

    memory= {
        "message" : message,
        "code" : code,
        "perfdata" : perfdata
    }

    return memory

def getStatusLabel(status):
    if status == UNKNOWN:
        return "UNKNOWN"
    elif status == OK:
        return "OK"
    elif status == WARNING:
        return "WARNING"
    elif status == CRITICAL:
        return "CRITICAL"
    else:
        return "UNKNOWN"


if __name__ == '__main__':
    
    usage = """usage: %prog --host xxx.xxx.xxx.xxx 
    --port 2375 
    --usetls 
    --ca /path/to/ca.pem 
    --cert /path/to/cert.pem 
    --key /path/to/key.pem 
    --name container_name
    --wait time to wait between two statisitic collection (stat = cpu|net)
    --stat stat type (cpu, memory, net)
    --unit unit in perfdata (stat = net only)
    -- warn warning threshold
    --critical critical threshold"""

    parser = OptionParser(usage=usage)
    parser.add_option('--host', dest='host', default=None, type=str)
    parser.add_option('--port', dest='port', default=2375, type=int)
    parser.add_option('--usetls', action="store_true", dest='usetls', default=False)
    parser.add_option('--ca', dest='ca', default=None, type=str)
    parser.add_option('--cert', dest='cert', default=None, type=str)
    parser.add_option('--key', dest='key', default=None, type=str)
    parser.add_option('--name', dest='name', default=None, type=str)
    parser.add_option('--wait', dest='wait', default=2, type=int)
    parser.add_option('--stat', dest='stat', default="cpu", type=str)
    parser.add_option('--unit', dest='unit', default="K", type=str)
    parser.add_option('--warn', dest='warn',default=80, type=int)
    parser.add_option('--crit', dest='crit',default=90, type=int)



    options, args = parser.parse_args()

    if options.usetls and (not options.ca or not options.cert or not options.key):
        log("You must provide ca, cert, key when using tls")
        sys.exit(UNKNOWN)

    if not options.name:
        log("You must provide a container name")
        sys.exit(UNKNOWN)

    if options.usetls:
        proto = "https"
    else:
        if options.port:
            proto = "http"
        else:
            proto = "tcp"

    if options.unit and not options.unit in ["B", "K", "M"]:
        log("Unit must be one of the following :")
        log("B : KiloBytes per second ")
        log("K : KiloBytes per second ")
        log("M : MegaBytes per second ")
        sys.exit(UNKNOWN)

    # create docker connection
    client = connect(proto=proto, host=options.host, port=options.port, usetls=options.usetls, cert=options.cert, key=options.key, ca=options.ca)

    # load containers list
    containers = client.containers()

    # get container by name

    container = getContainerByName(options.name)

    result = None

    if options.stat == "cpu":
        result = getCpu(container=container, warn=options.warn, crit=options.crit, wait=options.wait)
    elif options.stat == "memory":
        result = getMemory(container=container, warn=options.warn, crit=options.crit)
    elif options.stat == "net":
        result = getNet(container=container, warn=options.warn, crit=options.crit, unit=options.unit, wait=options.wait)

    if result:
        print "[%s] %s|%s" % (getStatusLabel(result["code"]),result["message"], result["perfdata"])
        sys.exit(result["code"])
    else:
        print "[UNKNOWN] unable to collect %s stats" % options.stat
        sys.exit(UNKNOWN)




