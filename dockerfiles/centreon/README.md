# Fully featured centreon in seconds

## Quick start

```
git clone https://github.com/david-guenault/docker-lab
cd docker-lab/dockerfiles/centreon
make build
docker run -d --name ces --hostname ces -p 80:80 dguenault/ces:3.0.0
```

Open a web browser and point to one of the following urls : 

- http://[hostip]/centreon (user:admin, password:centreon)
- http://[hostip]/nagvis (user:admin, password:admin)

