import requests 
from .load_env import load_cloudant_env, load_apikey_env
from .requests_ibmcloud_token import get_token
import sys

import logging

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

def get_service_instance_information():

    cloudant_env, verification = load_cloudant_env()
    
    if (verification):
        # 1. Load environment variables
        url = cloudant_env["CLOUDANT_URL"]

        # 2. Get apikey
        token, verification_token = get_token()
        apikey = "Bearer " + token["result"]

        if (verification_token["status"] == True):
            # 2. Build the header with authenication       
            headers = {
                    "Authorization": apikey
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
        data="no access token available"

    return { "result": data} , {"status":verification} 

def get_database_information():
    
    cloudant_env, verification = load_cloudant_env()
    
    if (verification):
        # 1. Load environment variables
        url = cloudant_env["CLOUDANT_URL"]
        db_name = cloudant_env["CLOUDANT_DB_NAME"]

        # 2. Build path
        url_path = url + "/_dbs_info" 
        
        # 3. Get apikey
        token, verification_token = get_token()
        apikey = "Bearer " + token["result"]
        
        if (verification_token["status"] == True):
            # 4. Build the header with authenication 
            try:         
                headers = {
                        "Authorization": apikey,
                        "Content-Type": "application/json"
                }

                payload = { "keys": [ db_name ]}

                # 5. Invoke REST API
                response = requests.post(
                        url_path,
                        json=payload,
                        headers=headers
                )

                # 6. Verify result
                if (response.status_code == 200):
                        data_all=response.json()
                        data = data_all
                        verification = True
                else:
                        verification = False
                        data=response.json()

            except Exception as e:

                error = {"exception `db information`": e }                  
                response = str(error)
                verification = False
                return { "result": response }, {"status":verification} 
    else:
        verification = False
        data="no access token available"

    return { "result": data} , {"status":verification} 

def create_database():
    
    cloudant_env, verification = load_cloudant_env()
    
    if (verification):
        # 1. Load environment variables
        url = cloudant_env["CLOUDANT_URL"]
        db_name = cloudant_env["CLOUDANT_DB_NAME"]

        # 2. Build path
        url_path = url + "/" + db_name 
        
        # 3. Get apikey
        token, verification_token = get_token()
        apikey = "Bearer " + token["result"]
        
        if (verification_token["status"] == True):
            # 4. Build the header with authenication 
            try:         
                headers = {
                        "Authorization": apikey,
                        "Content-Type": "application/json"
                }

                payload = { "keys": [ db_name ]}

                # 5. Invoke REST API
                response = requests.put(
                        url_path,
                        headers=headers
                )

                # 6. Verify result
                if (response.status_code == 200):
                        data_all=response.json()
                        data = data_all
                        verification = True
                else:
                        verification = False
                        data=response.json()

            except Exception as e:

                error = {"exception `db create data`": e }                  
                response = str(error)
                verification = False
                return { "result": response }, {"status":verification} 
    else:
        verification = False
        data="no access token available"
    
    retrun_data = {
                    "data":data,
                    "database_name":db_name       
                  }

    return { "result": retrun_data} , {"status":verification} 

def save_data(data):
    
    cloudant_env, verification = load_cloudant_env()
    
    if (verification):
        # 1. Load environment variables
        url = cloudant_env["CLOUDANT_URL"]
        db_name = cloudant_env["CLOUDANT_DB_NAME"]

        # 2. Build path
        url_path = url + "/" + db_name
        
        # 3. Get apikey
        token, verification_token = get_token()
        apikey = "Bearer " + token["result"]
        
        if (verification_token["status"] == True):
            # 4. Build the header with authenication 
            try:         
                headers = {
                        "Authorization": apikey,
                        "Content-Type": "application/json"
                }

                payload = data

                logging.debug(f"Payload:\n{payload}\n\n")

                # 5. Invoke REST API
                response = requests.post(
                        url_path,
                        json=payload,
                        headers=headers
                )

                # 6. Verify result
                if (response.status_code == 201):
                        data = response.json()
                        verification = True
                else:
                        verification = False
                        data = response.json()

            except Exception as e:
                error = {"exception `db save data`": e }                  
                response = str(error)
                verification = False
                return { "result": response }, {"status":verification} 
    else:
        verification = False
        data="no access token available"

    return { "result": data} , {"status":verification} 

def get_all_indexes():
    
    cloudant_env, verification = load_cloudant_env()
    
    if (verification):
        # 1. Load environment variables
        url = cloudant_env["CLOUDANT_URL"]
        db_name = cloudant_env["CLOUDANT_DB_NAME"]

        # 2. Build path
        url_path = url + "/" + db_name + "/_index"
        
        # 3. Get apikey
        token, verification_token = get_token()
        apikey = "Bearer " + token["result"]
        
        if (verification_token["status"] == True):
            # 4. Build the header with authenication 
            try:         
                headers = {
                        "Authorization": apikey,
                        "Content-Type": "application/json"
                }

                # 5. Invoke REST API
                response = requests.get(
                        url_path,
                        headers=headers
                )

                # 6. Verify result
                if (response.status_code == 200):
                        data_all=response.json()
                        data = data_all
                        verification = True
                else:
                        verification = False
                        data=response.json()

            except Exception as e:

                error = {"exception `db all indexes`": e }                  
                response = str(error)
                verification = False
                return { "result": response }, {"status":verification} 
    else:
        verification = False
        data="no access token available"

    return { "result": data} , {"status":verification} 

def get_all_design_docs():
    
    cloudant_env, verification = load_cloudant_env()
    
    if (verification):
        # 1. Load environment variables
        url = cloudant_env["CLOUDANT_URL"]
        db_name = cloudant_env["CLOUDANT_DB_NAME"]

        # 2. Build path
        url_path = url + "/" + db_name + "/_design_docs"
        
        # 3. Get apikey
        token, verification_token = get_token()
        apikey = "Bearer " + token["result"]
        
        if (verification_token["status"] == True):
            # 4. Build the header with authenication 
            try:         
                headers = {
                        "Authorization": apikey,
                        "Content-Type": "application/json"
                }

                # 5. Invoke REST API
                response = requests.get(
                        url_path,
                        headers=headers
                )

                # 6. Verify result
                if (response.status_code == 200):
                        data_all=response.json()
                        data = data_all
                        verification = True
                else:
                        verification = False
                        data=response.json()

            except Exception as e:

                error = {"exception `db design docs`": e }                  
                response = str(error)
                verification = False
                return { "result": response }, {"status":verification} 
    else:
        verification = False
        data="no access token available"

    return { "result": data} , {"status":verification} 

def get_all_docs():
    
    cloudant_env, verification = load_cloudant_env()
    
    if (verification):
        # 1. Load environment variables
        url = cloudant_env["CLOUDANT_URL"]
        db_name = cloudant_env["CLOUDANT_DB_NAME"]

        # 2. Build path
        url_path = url + "/" + db_name + "/_all_docs"
        
        # 3. Get apikey
        token, verification_token = get_token()
        apikey = "Bearer " + token["result"]
        
        if (verification_token["status"] == True):
            # 4. Build the header with authenication 
            try:         
                headers = {
                        "Authorization": apikey,
                        "Content-Type": "application/json"
                }

                payload = { "include_docs": "true" }

                # 5. Invoke REST API
                response = requests.post(
                        url_path,
                        json=payload,
                        headers=headers
                )

                # 6. Verify result
                if (response.status_code == 200):
                        data_all=response.json()
                        data = data_all
                        verification = True
                else:
                        verification = False
                        data=response.json()

            except Exception as e:

                error = {"exception `db all docs`": e }                  
                response = str(error)
                verification = False
                logging.info(f"{data}\n\n") 
                return { "result": response }, {"status":verification} 
    else:
        verification = False
        data="no access token available"

    return { "result": data} , {"status":verification} 

def get_view(_design_doc_view, _view_name):
    
    cloudant_env, verification = load_cloudant_env()
    
    if (verification):
        # 1. Load environment variables
        url = cloudant_env["CLOUDANT_URL"]
        db_name = cloudant_env["CLOUDANT_DB_NAME"]

        # 2. Build path
        url_path = url + "/" + db_name + "/_design/" + _design_doc_view + "/_view/" + _view_name
        
        # 3. Get apikey
        token, verification_token = get_token()
        apikey = "Bearer " + token["result"]
        
        if (verification_token["status"] == True):
            # 4. Build the header with authenication 
            try:         
                headers = {
                        "Authorization": apikey,
                        "Content-Type": "application/json"
                }

                # 5. Invoke REST API
                response = requests.get(
                        url_path,
                        headers=headers
                )

                # 6. Verify result
                if (response.status_code == 200):
                        data_all=response.json()
                        data = data_all
                        verification = True
                else:
                        verification = False
                        data=response.json()

            except Exception as e:

                error = {"exception `db view data`": e }                  
                response = str(error)
                verification = False
                logging.info(f"{data}\n\n") 
                return { "result": response }, {"status":verification} 
    else:
        verification = False
        data="no access token available"

    return { "result": data} , {"status":verification} 

def search_data(_design_doc_search, _design_search_idx, search_topic, search_string ):

    cloudant_env, verification = load_cloudant_env()
    if (verification):
        # 1. Load environment variables
        url = cloudant_env["CLOUDANT_URL"]
        db_name = cloudant_env["CLOUDANT_DB_NAME"]

        # 2. Build path
        url_path = url + "/" + db_name + "/_design/" + _design_doc_search + "/_search/" + _design_search_idx
        
        # 3. Get apikey
        token, verification_token = get_token()
        apikey = "Bearer " + token["result"]
        
        if (verification_token["status"] == True):
            # 4. Build the header with authenication 
            try:         
                headers = {
                        "Authorization": apikey,
                        "Content-Type": "application/json"
                }

                query = search_topic + ":" + search_string

                # Information: https://cloud.ibm.com/docs/Cloudant?topic=Cloudant-cloudant-search
                params = { "include_docs": "false", 
                           "limit": 200,
                           "query": query }

                # 5. Invoke REST API
                response = requests.get( url_path,
                                         params=params,
                                         headers=headers
                                       )

                # 6. Verify result
                if (response.status_code == 200):
                        data_all=response.json()
                        data = data_all
                        verification = True
                else:
                        verification = False
                        data=response.json()

            except Exception as e:

                error = {"exception `db search data`": e }                  
                response = str(error)
                verification = False
                logging.info(f"{data}\n\n") 
                return { "result": response }, {"status":verification} 
    else:
        verification = False
        data="no access token available"

    return { "result": data} , {"status":verification} 

def search_custom_data(_design_doc_search, _design_search_idx, search_string ):

    cloudant_env, verification = load_cloudant_env()
    if (verification):
        # 1. Load environment variables
        url = cloudant_env["CLOUDANT_URL"]
        db_name = cloudant_env["CLOUDANT_DB_NAME"]

        # 2. Build path
        url_path = url + "/" + db_name + "/_design/" + _design_doc_search + "/_search/" + _design_search_idx
        
        # 3. Get apikey
        token, verification_token = get_token()
        apikey = "Bearer " + token["result"]
        
        if (verification_token["status"] == True):
            # 4. Build the header with authenication 
            try:         
                headers = {
                        "Authorization": apikey,
                        "Content-Type": "application/json"
                }

                query = search_string

                # Information: https://cloud.ibm.com/docs/Cloudant?topic=Cloudant-cloudant-search
                params = { "include_docs": "false", 
                           "limit": 200,
                           "query": query }

                # 5. Invoke REST API
                response = requests.get( url_path,
                                         params=params,
                                         headers=headers
                                       )

                # 6. Verify result
                if (response.status_code == 200):
                        data_all=response.json()
                        data = data_all
                        verification = True
                else:
                        verification = False
                        data=response.json()

            except Exception as e:

                error = {"exception `db custom data`": e }                  
                response = str(error)
                verification = False
                logging.info(f"{data}\n\n") 
                return { "result": response }, {"status":verification} 
    else:
        verification = False
        data="no access token available"

    return { "result": data} , {"status":verification} 
