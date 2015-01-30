# Secure your dockers hosts the easy way

Most of the following was issued from docker online documentation (https://docs.docker.com/articles/https/). What this repository is bringing to you is an easy way to make your docker hosts more secure with ssl/tls encryption and tls client authentication. Saying that it is not intendend to be used with large docker installations, because in this case you will need a real pki. But if you own just a dozen of docker hosts it will work fine. 

# Create the CA

First of all Edit the Makefile and modify the following to match YOUR organization

```
COUNTRY=FR
STATE=Languedoc Roussillon
LOCALITY=Perpignan
ORGANIZATION=BOX4PROD
```

Create the CA

```
make ca
```

# Create the docker hosts certificates

```
make server SERVER=[your server hostname 1]
make server SERVER=[your server hostname 2]
make server SERVER=[your server hostname 3]
```

Note that the SERVER value must match the target hostname (you can get it with hostname -s command)

# Create a docker client certificate

```
make client CLIENT=[your certificate name]
```

you can create as many client certificate as you want with the name you want

# Deploy certificates

The resulting hierarchy is created once you created all of your certificates.

```
.
├── CA
│   ├── ca-key.pem
│   ├── ca.pem
│   ├── crl
│   ├── index
│   └── serial
├── client
│   └── node1
│       ├── ca.pem
│       ├── cert.pem
│       └── key.pem
└── server
    ├── node1
    │   ├── ca.pem
    │   ├── server-cert.pem
    │   └── server-key.pem
    ├── node2
    │   ├── ca.pem
    │   ├── server-cert.pem
    │   └── server-key.pem
    └── node3
        ├── ca.pem
        ├── server-cert.pem
        └── server-key.pem
```

- The CA folder old the certification of authority that is able to sign certificates (both servers and clients). This one must be protected ! If you lost this one you can start over ;-)
- the server folder old the servers certificates
- the client folder old the clients certificates

## Deploy on servers

for each of your server you must copy the related folder to the server (via scp for exemple). Then login to your server and issue the following command as root or with sudo

```
sudo /path/to/certificates/folder/setup.sh
```

Job done ! 

## Deploy on clients

To be done .... :-)

# Full example

I have 3 docker hosts with the legacy configuration (node1,node2,node3). Each of the host is configured in DNS or at least have a configured /etc/hosts file allowing to resolve by name the others hosts. 


- Create the required certificates. For this example i issue the commands from node1 but this should be executed from your laptop for example. 

```
make ca
make server SERVER=node1
make server SERVER=node2
make server SERVER=node3
make client CLIENT=node1
make client CLIENT=node2
make client CLIENT=node3
```

Now deploy the server folders to their respective hosts and issue the following command as root (or sudo)

```
# example for node2 from node1
scp server/node2 frogx@node2:/home/frogx/
ssh frogx@node2 
sudo ./node2/setup.sh
rm -Rf node2
```
Then deploy the client folders to their respective hosts and issue the following command as the user that will use the client

```
# example for node2 from node1
scp client/node2 frogx@node2:/home/frogx/
ssh frogx@node2 
sudo ./node2/setup.sh
rm -Rf node2
```

Finally do some tests

```
# version of the local docker
$ docker version
Client version: 1.4.1
Client API version: 1.16
Go version (client): go1.3.3
Git commit (client): 5bc2ff8
OS/Arch (client): linux/amd64
Server version: 1.4.1
Server API version: 1.16
Go version (server): go1.3.3
Git commit (server): 5bc2ff8

# version of a remote docker
$ docker -H tcp://node2:2375 version
Client version: 1.4.1
Client API version: 1.16
Go version (client): go1.3.3
Git commit (client): 5bc2ff8
OS/Arch (client): linux/amd64
Server version: 1.4.1
Server API version: 1.16
Go version (server): go1.3.3
Git commit (server): 5bc2ff8
```
