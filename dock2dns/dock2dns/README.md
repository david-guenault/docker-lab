This is a really simple way to do dns discovery for docker based projects prototyping. It rely on my experience with docker, skydock, skydns and fig. 

Skydock/skydns is a realy nice piece of software for dns based service discovery. It allow to quickly put in place a basic dns discovery solution with docker. The problem is that it does not work well with fig orchestration tool (well not the exact way i need it to be working). Other problem is that skydock/skydns is no longuer actively maintained and is behind skydns2 upstream version. 

What i wanted was a realy basic automatic dns registration along a basic orchestration tool. I use it to quickly build multi docker containers labs that need to talk each others without configuring anything. 

Start the dock2dns fig project (domain default to dock2dns.lan) to provide dns registration then start another fig project and everything is working out of the box. The only specific configuration is about configuring hostname in fig config file and link resolv.conf file. 

Exemple : 

in the following example, 2 busybox containers are started. Once you enter the b1 container, you can ping b2 or b2.dock2dns.lan without configuring anything else. The images are not modified and can be reused for other projects. This is simple and non intrusive. 

resolv.conf

nameserver 172.17.42.1 
domain dock2dns.lan 

fig.yml

b1:
    image: busybox 
    name: b1 
    hostname: b1 
    volumes:
        - /etc/localtime:/etc/localtime:ro
        - resolv.conf:/etc/resolv.conf
    entrypoint: top

b2:
    image: busybox 
    name: b2 
    hostname: b2 
    volumes:
        - /etc/localtime:/etc/localtime:ro
        - resolv.conf:/etc/resolv.conf
    entrypoint: top



