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
make firstrun
```

Open a web browser and point to one of the following urls : 

- http://[dockerhostip]/centreon (user:admin, password:centreon)

Go to Administration -> Extension and activate the centreon-nagvis module

Then nagvis maps are available in View -> Nagvis

You can manage maps pointing your browseer to http://[dockerhostip]/nagvis. You are authenticated with centreon_nagvis user credentials and have a role of manager. This role allow to manage maps. If you want to act as an admin, logout from centreon and authenticate as the user admin with password admin. 

## Manage start/stop

you can use the Makefile to manage start stop and restart of the ces container

```
make start 
make stop
make restart
```

Note that you must use the firstrun target before using those targets. The firstrun target is a one time use and must not be used again. 

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

## Manage services in container

Services (daemons) are managed through supervisord. You can start, stop or restart daemons through the command line or through a web interface. credentials for web interface are user: admin and password: admin. This can be changed in Makefile before building the image. To access the web interface you need to bind tcp port 9001 to you docker host ( -p 9001:9001). Then just use your favorite browser to point to http://[dockerhost]:9001

## Data storage 

Data are stored in a data_volume named cesdata. If you remove the ces container you will not loose all of the data. But if you plan to migrate the container do not forget to migrate the data container.  