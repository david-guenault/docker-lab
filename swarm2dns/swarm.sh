basepath=$(readlink -f $(dirname $0))
docker rm swarm
docker run -ti --rm --name swarm -v $basepath/cluster.conf:/cluster.conf -p 2376:2376 dguenault/swarm:latest manage --discovery file:///cluster.conf -H 0.0.0.0:2376
