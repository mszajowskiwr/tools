#!/bin/bash

date_start=$(date +%s)
count=1000000

url="https://payments-integrations-webapp.wremittst.com/payments-integrations-webapp-assets/version"
echo -en "\033]0;${url}\a"

[ $# -eq 1 ] && url=$1;
date_cmd=$(( command -v gdate >/dev/null && echo "gdate" ) || echo "date")

echo "date_cmd==$date_cmd"
for i in `seq $count`; do
    echo -en "\033]0;${url}\a"
    echo -n "$($date_cmd +"%T.%N") ($i): "
    date_step=$(date +%s)
    curl -L "${url}"
    echo " took $(( ($(date +%s) - ${date_step}) ))s ($(( ($(date +%s) - ${date_start}) ))s so far)"
done;
