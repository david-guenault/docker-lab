# Secure your dockers hosts the easy way

Most of the following was issued from docker online documentation (https://docs.docker.com/articles/https/). What this repository is bringing to you is an easy way to make your docker hosts more secure with ssl/tls encryption and tls client authentication. Saying that it is not intendend to be used with large docker installations, because in this case you will need a real pki. But if you own just a dozen of docker hosts it will work fine. 

# Create the CA

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

# example

I have 3 docker hosts with the legacy configuration (node1,node2,node3). node1 is the hostname. I do not have a dns server so every host get the nearly same /etc/hosts file

- node1 /etc/hosts file

```
127.0.0.1   localhost
127.0.1.1   node1   
10.10.0.5   node1
10.10.0.22  node2
10.20.0.21  node3   
```

- node2 /etc/hosts file

```
127.0.0.1   localhost
127.0.1.1   node2 
10.10.0.5   node1
10.10.0.22  node2
10.20.0.21  node3   
```

- node3 /etc/hosts file

```
127.0.0.1   localhost
127.0.1.1   node3
10.10.0.5   node1
10.10.0.22  node2
10.20.0.21  node3   
```

- Create the required certificates

```
make ca
make server SERVER=node1
make server SERVER=node2
make server SERVER=node3
make client CLIENT=clinode1
make client CLIENT=clinode2
make client CLIENT=clinode3
```

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



