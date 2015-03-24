# Fully featured centreon in seconds

## Quick start

```
git clone https://github.com/david-guenault/docker-lab
cd docker-lab/dockerfiles/centreon
make configure build
docker run -d --name ces --hostname ces -p 80:80 dguenault/ces:3.0.0
```

Open a web browser and point to one of the following urls : 

- http://[dockerhostip]/centreon (user:admin, password:centreon)

Go to Administration -> Extension and activate the centreon-nagvis module

Then nagvis maps are available in View -> Nagvis

You can manage maps pointing your browseer to http://[dockerhostip]/centreon. You are authenticated with centreon_nagvis user credentials and have a role of manager. This role allow to manage maps. If you want to act as an admin, logout from centreon and authenticate as the user admin with password admin. 
