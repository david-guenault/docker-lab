# Shinken 2 HA lab

Note : you must use the dock2dns lab to resolve host. Build the project and start it before using this lab

# Prerequisites

This lab is based on the following images: 

- dguenault/shinken-base:2.2
- dguenault/thruk:latest

Build those images before using this lab. 

# Grab configuration from shinken base image

You can use the extractconfig target from the makefile

```
make extractconfig
```