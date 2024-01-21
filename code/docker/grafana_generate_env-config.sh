#!/bin/bash
########################################
# Create a file based on the environment variables
# given by the dockerc run -e parameter
########################################
cat <<EOF
# Shelly 3EM
export SHELLY_URL=${SHELLY_URL}
export SHELLY_USER=${SHELLY_USER}
export SHELLY_PASSWORD=${SHELLY_PASSWORD}
export SHELLY_ID=${SHELLY_ID}
# IBM Cloudant
export CLOUDANT_URL=${CLOUDANT_URL}
export CLOUDANT_DB_NAME=${CLOUDANT_DB_NAME}
# IBM Cloud
export IBMCLOUD_APIKEY=${IBMCLOUD_APIKEY}
export IBMCLOUD_URL=${IBMCLOUD_URL}
# APP
export APP_USER=${APP_USER}
export APP_APIKEY=${APP_APIKEY}
export APP_LOG=${APP_LOG}
# Grafana
export GF_SECURITY_ADMIN_USER=${GF_SECURITY_ADMIN_USER}
export GF_SECURITY_ADMIN_PASSWORD=${GF_SECURITY_ADMIN_PASSWORD}
export GF_INSTALL_PLUGINS=${GF_INSTALL_PLUGINS} 
EOF
