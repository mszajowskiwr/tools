# Redis server with iptables to DROP traffic

## Starting

```
docker-compose up --build
```

Default port is `6379`, default password is `redis-password`. The container is exposed to host, to connect you can simply run:
```
redis-cli -a redis-password
```
from your local machine.


## Toggling traffic

```
docker exec redis-customized_wrredis_1 /bin/bash /usr/local/bin/disable_traffic.sh
docker exec redis-customized_wrredis_1 /bin/bash /usr/local/bin/enable_traffic.sh
```
