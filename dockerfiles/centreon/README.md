# Fully featured centreon in seconds

This project allow you to setup a fully featured centreon docker container in seconds. It come with: 

 - centreon
 - centreon-engine
 - centreon-broker
 - nagios-plugins
 - centreon-plugins
 - nagvis
 - centreon-clapi
 - centreon-nagvis

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

You can manage maps pointing your browseer to http://[dockerhostip]/nagvis. You are authenticated with centreon_nagvis user credentials and have a role of manager. This role allow to manage maps. If you want to act as an admin, logout from centreon and authenticate as the user admin with password admin. 

## Customize

The makefile allow to customize the following: 

 - SSHPASSWORD : container ssh root password 
 - SUPERVISORUSER : supervisord web interface user (tcp port 9001)
 - SUPERVISORPASSWORD : supervisord web interface password
 - NAGVISUSER : nagvis user used to share credentials with centreon
 - NAGVISPASSWORD : nagvis password 
 - NAGVISDBUSER : nagvis centreon database user (read only)
 - NAGVISDBPASSWORD : nagvis centreon database password
 - NAGVISADMINUSER : nagvis admin user 
 - NAGVISADMINPASSWORD : nagvis admin passord
 - NAGVISPASSWORDSALT : salt for sha1 hash password storage in nagvis sqlite database

