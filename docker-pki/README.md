# Secure your dockers hosts the easy way

Most of the following was issued from docker online documentation (https://docs.docker.com/articles/https/). What this repository is bringing to you is an easy way to make your docker hosts more secure with ssl/tls encryption and tls client authentication. Saying that it is not intendend to be used with large docker installations, because in this case you will need a real pki. But if you own just a dozen of docker hosts it will work fine. 

# Big thx

A realy big thx to Jessica B. Hamrick https://github.com/jhamrick who pointed my errors in building this. See this gist about the original script : https://gist.github.com/jhamrick/ac0404839b5c7dab24b5

# Create the CA

First of all Edit the Makefile and modify the following to match YOUR organization

```
COUNTRY=FR
STATE=Languedoc Roussillon
LOCALITY=Perpignan
ORGANIZATION=BOX4PROD
DAYS=3650
```

Create the CA

```
make ca
```

# Create the docker hosts certificates

```
make cert TYPE=daemon HOST=[your server hostname 1]
make cert TYPE=daemon HOST=[your server hostname 2]
make cert TYPE=daemon HOST=[your server hostname 3]
```

Note that the SERVER value must match the target hostname (you can get it with hostname -s command)

# Create a docker client certificate

```
make cert TYPE=client HOST=[your client hostname]
```

# Create a swarm client/server certificate

```
make cert TYPE=swarm HOST=[your swarm hostname]
```

you can create as many swarm certificate as you want with the name you want

# Deploy certificates

## daemon certificates

- Create a place to store your certificates and deploy them on each nodes

```
mkdir -p /etc/pki/docker
cp CA/daemon-[YOURHOSTNAME]/*.pem /etc/pki/docker
cp CA/ca.pem /etc/pki/docker
chmod -R 600  /etc/pki/docker/*.pem
```

- Edit /etc/default/docker so DOCKER_OPTS will match the following

```
DOCKER_OPTS="-H tcp://0.0.0.0:2375 --tlsverify --tlscacert=/etc/pki/docker/ca.pem --tlscert=/etc/pki/docker/cert.pem --tlskey=/etc/pki/docker/key.pem --label storage=node1"
```

- Restart your docker daemon

```
sudo service docker restart
```

## client certificates

- copy your client certificates to ~/.docker/

```
cp CA/certs/client-[your client name]/*.pem ~/.docker/
cp CA/ca.pm ~/.docker
```
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