FROM bitnami/redis:latest

USER root
RUN apt update && apt install -y iptables


ENV REDIS_PASSWORD=${REDIS_PASSWORD:-redis-password}
RUN echo "iptables-legacy -A INPUT -p tcp --dport 6379 -j DROP" > /usr/local/bin/disable_traffic.sh
RUN echo "iptables-legacy -D INPUT -p tcp --dport 6379 -j DROP" > /usr/local/bin/enable_traffic.sh
RUN chmod +x "/usr/local/bin/disable_traffic.sh"
RUN chmod +x "/usr/local/bin/enable_traffic.sh"
