#!/bin/bash

# **************** Global variables
export HOME_PATH=$(pwd)

# **********************************************************************************
# Functions definition
# **********************************************************************************

function check_podman () {
    ERROR=$(podman ps 2>&1)
    RESULT=$(echo $ERROR | grep 'Cannot' | awk '{print $1;}')
    VERIFY="Cannot"
    if [ "$RESULT" == "$VERIFY" ]; then
        echo "Podman is not running. Stop script execution."
        exit 1 
    fi
}

#**********************************************************************************
# Execution
# *********************************************************************************

echo "************************************"
echo " Build and start containers with Podman" 
echo "- 'Custom Grafana'"
echo "************************************"

# 1. load application environment configurations
source $(pwd)/../../code/.env

# 2. set qa service docker context
cd $HOME_PATH/../../code
chmod 777 ./docker/grafana_shelly_cloudant_connector.sh 
chmod 777 ./docker/grafana_generate_env-config.sh
chmod 777 ./docker/grafana_run.sh
export PODMAN_CONTEXT="$(pwd)"
cd $HOME_PATH

# **************** Verify container
echo "************************************"
echo " Verify container locally"
echo "************************************"

echo "************************************"
echo " Build and run grafana"
echo "************************************"
podman image list
podman container list
podman container stop -f  "grafana-local-verification"
podman container rm -f "grafana-local-verification"
podman image rm -f "grafana-local-verification:v1.0.0"

podman build -t "grafana-local-verification:v1.0.0" -f "${PODMAN_CONTEXT}/docker/Dockerfile_custom_grafana" ${PODMAN_CONTEXT}
pwd

podman container list

podman run --name="grafana-local-verification" \
            -it \
            -e SHELLY_URL=${SHELLY_URL} \
            -e SHELLY_USER=${SHELLY_USER} \
            -e SHELLY_PASSWORD=${SHELLY_PASSWORD} \
            -e SHELLY_ID=${SHELLY_ID} \
            -e CLOUDANT_URL=${CLOUDANT_URL} \
            -e CLOUDANT_DB_NAME=${CLOUDANT_DB_NAME} \
            -e IBMCLOUD_APIKEY=${IBMCLOUD_APIKEY} \
            -e IBMCLOUD_URL=${IBMCLOUD_URL} \
            -e APP_USER=${APP_USER} \
            -e APP_APIKEY=${APP_APIKEY} \
            -e APP_LOG=${APP_LOG} \
            -e GF_SECURITY_ADMIN_USER=${GF_SECURITY_ADMIN_USER} \
            -e GF_SECURITY_ADMIN_PASSWORD=${GF_SECURITY_ADMIN_PASSWORD} \
            -e GF_INSTALL_PLUGINS=${GF_INSTALL_PLUGINS} \
            -p 3000:3000 \
            "localhost/grafana-local-verification:v1.0.0"

podman logs grafana-local-verification
podman port --all 