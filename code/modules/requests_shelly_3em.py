import requests
import base64 
from .load_env import load_shelly_env, load_apikey_env
from datetime import datetime
import logging
import sys

##################################
# Configure Logging
log_config, log_validation = load_apikey_env()
if (str(log_config["APPLOG"])=="DEBUG"):
     logging.basicConfig(stream=sys.stdout,level=logging.DEBUG)
elif (str(log_config["APPLOG"])=="INFO"):
     logging.basicConfig(stream=sys.stdout,level=logging.INFO)
elif (str(log_config["APPLOG"])=="WARNING"):
     logging.basicConfig(stream=sys.stdout,level=logging.WARNING)
else:
     logging.basicConfig(stream=sys.stdout,level=logging.INFO)

def get_consumption_data():

    shelly_env, verification = load_shelly_env()

    now = datetime.now()
    # Format needed for Grafana 
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

    if (verification):

        # 1. Load environment variables
        url = shelly_env["SHELLY_URL"] + "/status"
        user = shelly_env["SHELLY_USER"]
        password = shelly_env["SHELLY_PASSWORD"]
        id = shelly_env["SHELLY_ID"]

        # 2. Get build auth
        auth = user + ":" + password
        auth_bytes = auth.encode("ascii")
        authbase64_bytes = base64.b64encode(auth_bytes)
        authbase64_string = authbase64_bytes.decode("ascii")
        base_auth = "Basic " + authbase64_string

        # 3. Build the header with authenication       
        headers = {
                    "Content-Type": "application/json",
                    "Authorization": base_auth
        }

        # 3. Invoke REST API
        response = requests.get(
                    url,
                    headers=headers
        )

        # 4. Verify result
        if (response.status_code == 200):
                    data_all = response.json()
                    emeters = data_all["emeters"]                    
                    total_power = data_all["total_power"]
                    data = { "emeters" : emeters,
                             "date": dt_string,
                             "total_power": total_power
                    }
                    verification = True
        else:
                    verification = False
                    data=response.json()
    else:
        verification = False
        data="no shelly config"
    
    return { "result": data} , {"status":verification} 

def get_single_consumption(phase):

    shelly_env, verification = load_shelly_env()
    
    if (verification):

        # 1. Load environment variables
        url = shelly_env["SHELLY_URL"] + "/emeter/" + phase
        user = shelly_env["SHELLY_USER"]
        password = shelly_env["SHELLY_PASSWORD"]
        id = shelly_env["SHELLY_ID"]

        # 2. Get build auth
        auth = user + ":" + password
        auth_bytes = auth.encode("ascii")
        authbase64_bytes = base64.b64encode(auth_bytes)
        authbase64_string = authbase64_bytes.decode("ascii")
        base_auth = "Basic " + authbase64_string
        #print(f"{base_auth}")

        # 3. Build the header with authenication       
        headers = {
                    "Content-Type": "application/json",
                    "Authorization": base_auth
        }

        # 3. Invoke REST API
        response = requests.get(
                    url,
                    headers=headers
        )

        # 4. Verify result
        if (response.status_code == 200):
                    data_all=response.json()
                    data = data_all
                    verification = True
        else:
                    verification = False
                    data=response.json()
    else:
        verification = False
        data="no shelly config"
    
    logging.debug(f"{data}")
    
    return { "result": data} , {"status":verification} 
