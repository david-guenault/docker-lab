# Certificates for use with SHINKEN

create shinken daemons certificates the easy way. 

# Quick start

```
make ca cert bundle
```

The certificates are located in the bundles/shinken folder.

# Create the CA

First of all Edit the Makefile and modify the following to match YOUR organization

```
ORGANIZATION=SHINKEN
DOMAIN=shinken-monitoring
TLD=org
UNIT=IT
DAYS=3650
SIZE=2048
OPENSSL=/usr/bin/openssl
HOST=shinken
```

# Create the CA

```
make ca
```

# Create the shinken daemons certificates

```
make cert
```

# Create a bundle

```
make bundle
```

Everything you need is in bundles/shinken

# Deploy server certificates on your shinken daemons

- copy the content of the bundles/shinken folder to the /etc/shinken/certs folder of each shinken server. 

- Edit each of the ini file located in /etc/shinken/daemons and uncomment the following lines 

```
use_ssl=1
ca_cert=/etc/shinken/certs/ca.pem
server_cert=/etc/shinken/certs/server.cert
server_key=/etc/shinken/certs/server.key
```

- Edit each daemon configuration (arbiters/*.cfg pollers/*.cfg reactionners/*.cfg receiver/*.cfg scheduler/*.cfg broker/*.cfg) and set the use_ssl directive to 1

- Edit the /etc/shinken/shinken.cfg file and set use_ssl to 1 and uncomment the following lines

```
use_ssl=1
# WARNING : Put full paths for certs
ca_cert=/etc/shinken/certs/ca.pem
server_cert=/etc/shinken/certs/server.cert
server_key=/etc/shinken/certs/server.key
```

- restart ALL of your shinken daemons

# Regenerate certificates

Just rerun the Create the shinken daemons certificates step and Deploy step