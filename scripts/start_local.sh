# **************** Global variables
export HOME_PATH=$(pwd)

# Python env
python3 -m venv --upgrade-deps "$HOME_PATH"/../code/shelly-cloudant-grafana-env-3.12
source "$HOME_PATH"/../code/shelly-cloudant-grafana-env-3.12/bin/activate

cd "$HOME_PATH/../code"
python3 -m pip install -r requirements.txt
python3 -m pip install schedule


cd $HOME_PATH

# Application - variables
source "$HOME_PATH"/../code/.env

# **********************************************************************************
# Functions definition
# **********************************************************************************

# TBD

#**********************************************************************************
# Execution
# *********************************************************************************

python3 "$HOME_PATH/../code/shelly-3em-cloudant-connector.py"
