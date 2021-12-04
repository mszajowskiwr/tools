# Redis server with iptables to DROP traffic

To start:

```
docker-compose up
```

To toggle traffic:

```
docker exec redis-customized_wrredis_1 /bin/bash /usr/local/bin/disable_traffic.sh
docker exec redis-customized_wrredis_1 /bin/bash /usr/local/bin/enable_traffic.sh
```
