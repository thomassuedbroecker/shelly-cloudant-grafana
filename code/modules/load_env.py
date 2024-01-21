import os
import logging
import sys

##################################
# Configure Logging
# load config 
if (os.environ.get("APP_LOG") == None):
        APPLOG = "INFO"
else:
        APPLOG = os.environ.get("APP_LOG")
# set logging
if (str(APPLOG)=="DEBUG"):
     logging.basicConfig(stream=sys.stdout,level=logging.DEBUG)
elif (str(APPLOG)=="INFO"):
     logging.basicConfig(stream=sys.stdout,level=logging.INFO)
elif (str(APPLOG)=="WARNING"):
     logging.basicConfig(stream=sys.stdout,level=logging.WARNING)
else:
     logging.basicConfig(stream=sys.stdout,level=logging.INFO)

def load_ibmcloud_env():
       if (os.environ.get("IBMCLOUD_APIKEY") == None):
            IBMCLOUD_APIKEY = ''
       else:
            IBMCLOUD_APIKEY = os.environ.get("IBMCLOUD_APIKEY")
        
       if (os.environ.get("IBMCLOUD_URL") == None):
            IBMCLOUD_URL = ''
       else:
            IBMCLOUD_URL = os.environ.get("IBMCLOUD_URL")

       if ((IBMCLOUD_APIKEY=='') or (IBMCLOUD_URL=='')):
            configurationStatus = False
       else:
            configurationStatus = True
    
       configurationJSON = { "IBMCLOUD_APIKEY": IBMCLOUD_APIKEY,
                             "IBMCLOUD_URL": IBMCLOUD_URL}
       
       logging.debug(f"{configurationJSON}")
       
       return configurationJSON, configurationStatus

def load_cloudant_env():

        if (os.environ.get("CLOUDANT_URL") == None):
               CLOUDANT_URL = ''
        else:
               CLOUDANT_URL = os.environ.get("CLOUDANT_URL")

        if (os.environ.get("CLOUDANT_DB_NAME") == None):
               CLOUDANT_DB_NAME = ''
        else:
               CLOUDANT_DB_NAME = os.environ.get("CLOUDANT_DB_NAME")
       
        if ((CLOUDANT_URL=='') or (CLOUDANT_DB_NAME=='')):
                configurationStatus = False
        else:
                configurationStatus = True
        
        configurationJSON = { "CLOUDANT_URL": CLOUDANT_URL,
                              "CLOUDANT_DB_NAME": CLOUDANT_DB_NAME                            
                            }
        
        logging.debug(f"{configurationJSON}")

        return configurationJSON, configurationStatus

def load_shelly_env():

        if (os.environ.get("SHELLY_URL") == None):
               SHELLY_URL = ''
        else:
               SHELLY_URL = os.environ.get("SHELLY_URL")

        if (os.environ.get("SHELLY_USER") == None):
               SHELLY_USER = ''
        else:
               SHELLY_USER = os.environ.get("SHELLY_USER")

        if (os.environ.get("SHELLY_PASSWORD") == None):
               SHELLY_PASSWORD = ''
        else:
               SHELLY_PASSWORD= os.environ.get("SHELLY_PASSWORD")

        if (os.environ.get("SHELLY_ID") == None):
               SHELLY_ID = ''
        else:
               SHELLY_ID= os.environ.get("SHELLY_ID")
       
        if ((SHELLY_URL=='') or (SHELLY_USER=='') or
            (SHELLY_PASSWORD=='') or (SHELLY_ID=='')):
                configurationStatus = False
        else:
                configurationStatus = True
        
        configurationJSON = { "SHELLY_URL": SHELLY_URL,
                              "SHELLY_USER": SHELLY_USER,
                              "SHELLY_PASSWORD": SHELLY_PASSWORD,
                              "SHELLY_ID": SHELLY_ID                                
                            }
        
        logging.debug(f"{configurationJSON}")

        return configurationJSON, configurationStatus

def load_apikey_env():
    if (os.environ.get("APP_USER") == None):
            USER = "admin"
    else:
            USER = os.environ.get("APP_USER")
    
    if (os.environ.get("APP_APIKEY") == None):
            APIKEY = "apikey"
    else:
            APIKEY = os.environ.get("APP_APIKEY")

    if (os.environ.get("APP_LOG") == None):
            APPLOG = "INFO"
    else:
            APPLOG = os.environ.get("APP_LOG")
    
    if ((USER=="admin") or 
        (APIKEY=="apikey")):
            authenicationStatus = False
    else:
            authenicationStatus = True
    
    authenicationJSON = { "USER": USER,
                          "APIKEY":APIKEY,
                          "APPLOG":APPLOG
                        }
    
    logging.debug(f"{authenicationJSON}")

    return authenicationJSON, authenicationStatus