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

[TO BE DONE]