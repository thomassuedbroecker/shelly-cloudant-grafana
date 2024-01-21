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
echo " Build and start containers with Podman compose " 
echo "- 'Grafana'"
echo "- 'Shelly3EM-Cloudant-Grafana'"
echo "************************************"

check_podman

# 1. Load application environment configurations
source $(pwd)/../../code/.env

# 2. Set application docker context
cd $HOME_PATH/../../code
export PODMAN_CONTEXT="$(pwd)"
cd $HOME_PATH

# 3. Start compose
podman-compose version
echo "**************** BUILD ******************" 
podman-compose -f ./podman_compose.yaml build
echo "**************** START ******************" 
podman-compose -f ./podman_compose.yaml up # --detach

#podman-compose -f ./podman_compose.yaml stop
