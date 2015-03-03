# Secure your dockers hosts the easy way

Most of the following was issued from docker online documentation (https://docs.docker.com/articles/https/). What this repository is bringing to you is an easy way to make your docker hosts more secure with ssl/tls encryption and tls client authentication. Saying that it is not intendend to be used with large docker installations, because in this case you will need a real pki. But if you own just a dozen of docker hosts it will work fine. 

# Big thx

A realy big thx to Jessica B. Hamrick https://github.com/jhamrick who pointed my errors in building this. See this gist about the original script : https://gist.github.com/jhamrick/ac0404839b5c7dab24b5

Most of the config templates were found on the amazing  openssl pki tutorial : http://pki-tutorial.readthedocs.org/en/latest/index.html

# Create the CA

First of all Edit the Makefile and modify the following to match YOUR organization

```
ORGANIZATION=BOX4PROD
DOMAIN=box4prod
TLD=com
UNIT=IT
DAYS=3650
SIZE=2048
CRLHOST=node3
CRLPORT=8080
```

Create the CA

```
make ca
```

# Create the CRL (certificate revocation list)

Note that this is curently not supported in docker server and client

```
make crl
```

# Create the docker hosts certificates

```
make servercert HOST=[your server hostname 1]
```

# create the docker client certificates

```
make clientcert HOST=[your client hostname]
```

# Deploy server certificates on your docker nodes

- Create a server certificates bundle 

```
make dockerserverbundle HOST=[your server hostname]
```

This will create a folder server-[hostname] under bundles folder where you can find the ca certificates, the host certificate and the key. There is also a setup.sh script that will deploy and configure everything for you. Copy the folder on the remote host. Ssh into the host and then issue the setup.sh command. The restart your docker daemon. That's it !


# Deploy client certificates on the host you use to manage your docker nodes

- Create a client certificates bundle 

```
make dockerclientbundle HOST=[your hostname]
```

This will create a folder client-[hostname] under bundles where you can find the ca certificates, the host certificate and the key. There is also a setup.sh script that will deploy and configure everything for you. Copy the folder on the remote host. Ssh into the host and then issue the setup.sh command. Reload your .bashrc file with the following command :

```
source ~/.bashrc
```

# Revoke certificate

CRL are handled by the Makefile. To revoke a certificate you just have to issue the following command. 

```
make revoke TYPE=[client|server] HOST=[host name]
```

Behind the scene: this will revoke the certificate, update the crl and publish the new crl. 