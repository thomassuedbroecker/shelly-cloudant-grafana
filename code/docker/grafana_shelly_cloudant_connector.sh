#!/bin/bash

CURRENT_USER=$(whoami)
echo "Current user: $CURRENT_USER"

echo "*********************"
echo "** Create enviroment file "
echo "*********************"

HOME_PATH=$(pwd)
echo "Home: ${HOME_PATH}"
cd /app
/bin/bash grafana_generate_env-config.sh > /app/.env
#source .env
#cat .env

echo "*********************"
echo "** Start Python server"
echo "*********************"
echo "Home: $(pwd)"
ls -a
python shelly-3em-cloudant-connector.py