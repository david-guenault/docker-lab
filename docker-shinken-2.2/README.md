# Shinken 2.2 as docker application

## Prerequisites:

### Docker 

You can find documentation about how to install docker at the following location

  - Debian : https://docs.docker.com/installation/debian/
  - Ubuntu : https://docs.docker.com/installation/ubuntulinux/
  - Redhat : https://docs.docker.com/installation/rhel/
  - Centos : https://docs.docker.com/installation/centos/

### Fig

Every gnu/linux flavor should work the same way. Fig is a python application and can be installed the following way (as root user): 
  
  ```
  pip install -U fig
  ```

### nsenter:
  
nsenter is released as a docker container that will put the binary where you want. The only required thing is that it need to be accessible in the PATH. Let say /usr/local/bin/nsenter

  ```
  docker run --rm jpetazzo/nsenter cat /nsenter > /tmp/nsenter 
  chmod +x /tmp/nsenter
  docker rmi jpetazzo/nsenter
  mv /tmp/nsenter /usr/local/bin/nsenter
  ```
nsenter come with a convenient script that make it more simple to use (docker-enter). We have to grab it and put it in a location that is available in the path

   ```
   wget https://raw.githubusercontent.com/jpetazzo/nsenter/master/docker-enter -O /usr/local/bin/docker-enter
   chmod +x /usr/local/bin/docker-enter
   ```

## Building the docker image

There is only one versatile docker image. You can build it by using the provided Makefile (install make before using it). The only thing needed to build the image is an access to internet (for Debian 7 mirror access).

```
make build
```

Once finished you can see that the image has been added to your docker images

```
docker images
REPOSITORY                      TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
shinken/shinken                 2.2                 10f9da402621        16 minutes ago      491.4 MB
```


