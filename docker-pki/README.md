# Secure your dockers hosts the easy way

Most of the following was issued from docker online documentation (https://docs.docker.com/articles/https/). What this repository is bringing to you is an easy way to make your docker hosts more secure with ssl/tls encryption and tls client authentication. Saying that it is not intendend to be used with large docker installations, because in this case you will need a real pki. But if you own just a dozen of docker hosts it will work fine. 

Most of the config templates were found on the amazing  openssl pki tutorial : http://pki-tutorial.readthedocs.org/en/latest/index.html

# Big thx

A realy big thx to Jessica B. Hamrick https://github.com/jhamrick who pointed my errors in building this. See this gist about the original script : https://gist.github.com/jhamrick/ac0404839b5c7dab24b5

# Create the CA

First of all Edit the Makefile and modify the following to match YOUR organization

```
ORGANIZATION=BOX4PROD
DOMAIN=box4prod.com
DAYS=3650
SIZE=2048
```

Create the CA

```
make ca
```

# Create the docker/swarm hosts certificates

```
make servercert HOST=[your server hostname 1]
make servercert HOST=[your server hostname 2]
make servercert HOST=[your server hostname 3]
```

you can create as many swarm certificate as you want with the name you want

# Deploy certificates on your docker nodes

- Create a certificates bundle 

```
make bundle HOST=[your server hostname]
```

All you need can be found in bundles/[your server hostname]

- Edit /etc/default/docker so DOCKER_OPTS will match the following

```
DOCKER_OPTS="-H tcp://0.0.0.0:2375 --tlsverify --tlscacert=/etc/pki/docker/ca.pem --tlscert=/etc/pki/docker/[your server hostname].cert --tlskey=/etc/pki/docker/[your server hostname].key"
```

- Restart your docker daemon

```
sudo service docker restart
```

# use certificates with docker cli

- Create a certificates bundle 

```
make bundle HOST=[your server hostname]
```

- copy your certificates to ~/.docker/ . ONLY CERT AND CA CERTIFICATES NOT THE KEY

- Add the following to your ~/.bashrc file

```
DOCKER_HOST=tcp://[your hostname]:2375
DOCKER_TLS_VERIFY=1
```

- reload your ~/.bashrc file

```
source ~/.bashrc
```

## swarm certificates

[TO BE DONE]