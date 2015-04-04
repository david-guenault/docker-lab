#!/bin/bash

export APACHE_SERVERADMIN=admin@localhost
export APACHE_SERVERNAME=localhost
export APACHE_SERVERALIAS=localhost
export APACHE_DOCUMENTROOT=/var/www
export APACHE_RUN_USER=www-data
export APACHE_RUN_GROUP=www-data
export APACHE_LOG_DIR=/var/log/apache2
export APACHE_PID_FILE=/var/run/apache2.pid
export APACHE_RUN_DIR=/var/run/apache2
export APACHE_LOCK_DIR=/var/lock/apache2

/usr/sbin/apache2 -DFOREGROUND