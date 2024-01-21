#!/bin/bash

echo "1. List content of current directory"
pwd
ls -a

export APP_APIKEY_ENCODED=$(echo -n "${APP_APIKEY}" | base64)
echo ${APP_APIKEY}
echo ${APP_APIKEY_ENCODED}

#echo "2. Change execution"
#cd /app
#chmod 777 grafana_shelly_cloudant_connector.sh 
#chmod 777 grafana_generate_env-config.sh
#chmod 777 grafana_run.sh

#find / -name grafana.ini
#cat /etc/grafana/grafana.ini

echo "3. Start supervisord"
cd /usr/bin/
supervisord -c /etc/supervisord.conf