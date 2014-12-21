Build the images
==========

```
make build
```

Note: You can modify everything you need in dockerfiles/shinken-{arbiter|poller|broker|scheduler|receiver|reactionner}-1.4 and dockerfiles/shinken-1.4. 

Run the project
=========

```
fig up -d
```

Stop project
=======

```
fig stop
```

Cleanup project containers
================

```
fig rm --force
```

Cleanup images
==========

```
make clean
```

