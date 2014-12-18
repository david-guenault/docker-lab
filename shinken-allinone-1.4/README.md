shinken 1.4 all in one lab
==========================
<img alt="shinken" src="http://www.shinken-monitoring.org/img/NinjaGreen.png" height="128px">
<img alt="mongodb" src="http://upload.wikimedia.org/wikipedia/en/thumb/e/eb/MongoDB_Logo.png/640px-MongoDB_Logo.png" width="256px">
<img alt="thruk" src="http://www.thruk.org/images/logo_thruk.png">

Lab with one shinken container (embed ssh, snmp, nagios-plugins-all, manubulon plugins and check_netint.pl plugin), one mongodb container for shinken web user preferences storage and one container the thruk frontend.

Prerequisites
=============

- dock2dns up and running. 

Images 
======
This lab is based on the following images :

- official mongodb image
- thruk image from docker-lab
- shinken 1.4 image from docker-lab

Run
===

```
fig up -d 
```

Stop
====

```
fig stop
```

Access the guis
===============

- Shinken webui : make webui
- Thruk : make thruk
- Supervisor for shinken container : make supervisor
