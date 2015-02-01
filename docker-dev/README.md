# Build and run docker from sources

This is for MY test purpose

- Try the latest version from master

```
make clone && sudo make build && sudo make backupdocker && sudo make switch2dev
docker version

```

- Restore original docker version

```
sudo make switch2stable
docker version
Client version: 1.4.1
Client API version: 1.16
Go version (client): go1.3.3
Git commit (client): 5bc2ff8
OS/Arch (client): linux/amd64
Server version: 1.4.1
Server API version: 1.16
Go version (server): go1.3.3
Git commit (server): 5bc2ff8
```
