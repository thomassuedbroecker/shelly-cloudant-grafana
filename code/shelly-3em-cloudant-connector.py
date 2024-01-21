from fastapi import Depends, HTTPException, FastAPI, Response, Request, File, UploadFile
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
from fastapi.openapi.utils import get_openapi
from typing import Annotated, Any
import schedule
import json
import logging
import sys

##################################
# Custom modules
from modules.load_env import load_apikey_env, load_cloudant_env, load_shelly_env
from modules.requests_ibmcloud_token import get_token, load_ibmcloud_env
from modules.apis_response_format import Get_access_token, Get_ibmcloud_config, Health, Cloudant_response, Shelly_response, IBMCloud_info, Schedule_response
from modules.apis_payload import Cloudant_view, Cloudant_search
from modules.requests_cloudant import get_service_instance_information, get_database_information, save_data, get_all_indexes, get_all_docs, get_view, search_data, search_custom_data, create_database, get_all_design_docs
from modules.requests_shelly_3em import get_consumption_data
from modules.requests_json_grafana_datasource import convert_view_all_data, empty_data, json_datasource_metric_payload_options, json_datasource_metrics, convert_search_all_data, convert_search_custom_all_data, json_datasource_variable

##################################
# Set basic auth as security
security = HTTPBasic()
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    data, verification = load_apikey_env()
    
    if ( verification == False):
                    error = {"error": "verification failed" }                  
                    print(f"Error: {error} Data: {data}")
                    apikey=""
                    user=""
    else:
        apikey = data["APIKEY"]
        user = data["USER"]
  
    if ((credentials.username != user) or (credentials.password != apikey)):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                            detail="incorrect user or apikey",
                            headers={"WWW-Authenticate":"Basic"})   
     
    return credentials.username

##################################
# Create API with basic security
app = FastAPI(dependencies=[Depends(authenticate)])
#app.debug = True

##########################################################################
# Functions

###########
# Cloudant

# Invoke a Cloudant view to display data.
def view_all():
    validation = False
    try:    
       data, validation = convert_view_all_data() 
       if (validation['status'] == False):
                    error = {"error": "validation failed" }                  
                    print(f"{error}")
                    validation = False
                    data = empty_data() 
       else:
           validation = True
           
    except Exception as e:       
        error = {"exception `func view_all`": e }                  
        print(f"{error}")
        validation = False
        data = empty_data()

    return data, validation

# Invoke a Cloudant configurable search index to display data.
def search_all(search_topic,search_string):
    validation = False
    try:    
       data, validation = convert_search_all_data(search_topic,search_string)
       if (validation['status'] == False):
                    error = {"error": "validation failed" }                  
                    print(f"{error}")
                    validation = False
                    data = empty_data() 
       else:
           validation = True
           
    except Exception as e:       
        error = {"exception `func search_all`": e }                  
        print(f"{error}")
        validation = False
        data = empty_data()

    return data, validation

def search_all_custom(search_string):
    validation = False
    try:    
       data, validation = convert_search_custom_all_data(search_string)
       if (validation['status'] == False):
                    error = {"error": "validation failed" }                  
                    print(f"{error}")
                    validation = False
                    data = empty_data() 
       else:
           validation = True
           
    except Exception as e:       
        error = {"exception `func search all custom`": e }                  
        print(f"{error}")
        validation = False
        data = empty_data()

    return data, validation

############
# Schedule status to save shelly data
# 1. Class to handle the status
class ScheduleStatusClass:

  def __init__(self, status):
    self.schedule_status = status
  
  def getStatus(self):
    return self.schedule_status
  
  def setStatus(self, status):
    self.schedule_status = status
    return self.schedule_status
  
  def __str__(self):
    return f"{self.schedule_status}"
# 2. Set initial status
schedule_status = ScheduleStatusClass(status=False)
# 3. Save Shelly data
def save_shelly_data_job():
    try:      
       data, validation = get_consumption_data()      
       if (validation["status"] == True):
           try:
                data, validation = save_data(data)           
           except Exception as e:          
                       error = {"exception `func save shelly`": e } 
                       data  = str(error)
                       verification = False         
                       return { "data":data, "status":verification } 
       else:
            error = { "error": "validation failed" } 
            data  = str(error)
            verification = False

    except Exception as e:       
        error = {"exception `func save shelly job`": e }                  
        data  = str(error)
        verification = False        
        return { "data": data, "status": verification }     

    return { "data":data, "validation":validation }

#############
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

#################################################################
# Endpoints
     
@app.get("/")
def root_show_configuration_status():
    """
    This endpoint verifies the configuration status of `Shelly-Cloudant-Grafana-connection-server`.
    """
    config, validation = load_apikey_env()
    if (validation):
        status_application = "configured"
    else:
        status_application = "unconfigured"
    
    config, validation = load_cloudant_env()
    if (validation):
        status_cloudant = "configured"
    else:
        status_cloudant = "unconfigured"

    config, validation = load_ibmcloud_env()
    if (validation):
        status_ibmcloud = "configured"
    else:
        status_ibmcloud = "unconfigured"

    config, validation = load_shelly_env()
    if (validation):
        status_shelly = "configured"
    else:
        status_shelly = "unconfigured"
        
    status = {
         "status_application":status_application,
         "status_cloudant":status_cloudant,
         "status_ibmcloud":status_ibmcloud,
         "status_shelly":status_shelly
    }
    
    return{"status": status}

@app.get("/health", response_model=Health) 
def provide_health_status() -> Any:
    """
    This endpoint implements the health status to enable\n
    that the `Shelly-Cloudant-Grafana-connection-server` runs on a container management platform like Kubernetes.
    """
    return { "status": "ok"}

###########
# Schedule
@app.get("/schedule_start", response_model=Schedule_response) 
def schedule_start():
    """
    This endpoint starts the `hourly` schedule to save `Shelly data`. \n 
    _Info:_ Using the `Overload` functionality for `functions` in Python for the function `schedule_start`.\n 
    https://www.scaler.com/topics/function-overloading-in-python/
    """
    logging.debug(f"Schedule start - before: {schedule_status.getStatus()}")
    schedule_status.setStatus(True)
    logging.debug(f"Schedule start - after: {schedule_status.getStatus()}")
    schedule.every(1).hours.do(save_shelly_data_job)
    while (schedule_status.getStatus() == True):
         schedule.run_pending()
    
    return {"schedule": schedule_status.getStatus() }

@app.get("/schedule_stop", response_model=Schedule_response) 
def schedule_start():
    """
    This endpoint stops the schedule to save Shelly data. \n 
    _Info:_ Using the Overload` functionality for `functions` in Python for the function `schedule_start`.\n 
    https://www.scaler.com/topics/function-overloading-in-python/
    """
    
    logging.debug(f"Schedule stop - before: {schedule_status.getStatus()}")
    schedule_status.setStatus(False)
    logging.debug(f"Schedule stop - before: {schedule_status.getStatus()}")
    return {"schedule": schedule_status.getStatus() }

@app.get("/schedule_get_status", response_model=Schedule_response) 
def schedule_start():
    """
    This endpoint returns the schedule status to save Shelly data. \n    
    _Info:_ Using the Overload` functionality for `functions` in Python for the function `schedule_start`.\n 
    https://www.scaler.com/topics/function-overloading-in-python/
    """
    status = schedule_status.getStatus()
    logging.debug(f"Schedule status: {schedule_status.getStatus()}")
    return {"schedule": status }

###########
# IBM Cloud
@app.get("/ibmcloud_get_cloudant_service_information", response_model=IBMCloud_info)
def ibmcloud_cloudant_service_information() -> Any:
    """
    This endpoint provides the Cloudant service configuration information.
    """
    data, validation = get_service_instance_information()
    
    return {"data": data, "validation": validation }

@app.get("/ibmcloud_get_config", response_model=Get_ibmcloud_config)
def get_ibmcloud_configuration() -> Any:
    """
    This endpoint provides the configuration for IBM Cloud.
    """
    config, validation = load_ibmcloud_env()
    return {"ibmcloud_config":config, "validation":validation }

@app.get("/ibmcloud_get_access_token", response_model=Get_access_token)
def get_an_ibmcloud_access_token() -> Any:
    """
    This endpoint returns an IBM Cloud access token for the account configure in the environment variables.
    """
    data, validation = get_token()
    return {"token":data, "validation":validation }

###########
# Database

@app.post("/db_create_doc_from_file_/", response_model=Cloudant_response)
async def post_db_create_doc_from_file(   file: Annotated[UploadFile, File(description="A `JSON` file to create a new document entry in the database.")]
                                      ) -> Any:
    """
    This endpoint creates new documents in the Cloudant database based on JSON files.\n
    A new document can be any typ of document as long it is in JSON.\n
    This endpoint is for creating the needed index, query, and view of the application\n
    These needed files are located in the cloned GitHub repo  folder `[Project]/code/cloudant_config`.
    - `upload-1-view*.json`
    - `upload-2-search*.json`
    """ 
    data =  await file.read()
    # convert return value to needed JSON format
    # From binary to text
    data_string = data.decode('ascii')
    # From binary to te
    logging.debug(f"Text:\n{data_string}\n\n")
    document_json = json.loads(data_string)
    logging.debug(f"JSON load:\n{document_json}\n\n")
    data, validation = save_data(document_json)
    logging.debug(f"{data}")

    return_data = { "data": data,
                    "filename": file.filename         
    }

    return {"data": return_data, "validation": validation }

@app.get("/db_create_cloudant_database", response_model=Cloudant_response)
def get_db_create_database() -> Any:
    """
    This endpoint creates a `Cloudant database` \n 
    based on the environment variable `CLOUDANT_DB_NAME` in the `.env` file.
    """
    data, validation = create_database()
    
    return {"data": data, "validation": validation }

@app.get("/db_get_cloudant_information", response_model=Cloudant_response)
def get_db_information() -> Any:
    """
    This endpoint provides the `Cloudant database` configuration information.
    """
    data, validation = get_database_information()
    
    return {"data": data, "validation": validation }

@app.get("/db_get_all_indexes", response_model=Cloudant_response)
def get_all_db_indexes() -> Any:
    """
    This endpoint provides existing indexes in the `Cloudant database`.
    """
    try: 
     
       data, validation = get_all_indexes()
       
    except Exception as e:       
        error = {"exception": e }                  
        data  = str(error)
        verification = False        
        return { "data":data, "status":verification }     

    return { "data":data, "validation":validation }

@app.get("/db_get_all_design_docs", response_model=Cloudant_response)
def get_all_db_design_docs() -> Any:
    """
    This endpoint provides existing design docs in the `Cloudant database`.
    """
    try: 
     
       data, validation = get_all_design_docs()
       
    except Exception as e:       
        error = {"exception": e }                  
        data  = str(error)
        verification = False        
        return { "data":data, "status":verification }     

    return { "data":data, "validation":validation }

@app.post("/db_get_view", response_model=Cloudant_response)
async def get_db_view(cloudant_view:Cloudant_view) -> Any:
    """
    This endpoint provides the access to Cloudant views.
    These are the current values you can use:
    - _designdoc_name_ : `design_view_all_docs`
    - _view_name_ : `view_all_docs`
    """
    try: 
     
       data, validation = get_view(cloudant_view.designdoc_name, cloudant_view.view_name)
       
    except Exception as e:       
        error = {"exception": e }                  
        data  = str(error)
        verification = False        
        return { "data":data, "status":verification }     

    return { "data":data, "validation":validation }

@app.post("/db_search", response_model=Cloudant_response)
async def db_search(cloudant_search:Cloudant_search) -> Any:
    """
    This endpoint provides search options with following options.
    - _designdoc_name_ : `design_search_idx_results_emeters_all`
    - _search_name_ : `search_idx_results_emeters_all`
    - _search_topic_ : `date`
    - _search_string_ : `2024*`
    """
    try: 
     
       data, validation = search_data(cloudant_search.designdoc_name, 
                                      cloudant_search.search_name,
                                      cloudant_search.search_topic,
                                      cloudant_search.search_string )
       
    except Exception as e:       
        error = {"exception": e }                  
        data  = str(error)
        verification = False        
        return { "data":data, "status":verification }     

    return { "data":data, "validation":validation }

@app.post("/db_search_custom", response_model=Cloudant_response)
async def db_search_custom(cloudant_search:Cloudant_search) -> Any:
    """
    This endpoint provides search options with following options.
    - _designdoc_name_ : `design_search_idx_results_emeters_all`
    - _search_name_ : `search_idx_results_emeters_all`
    - _search_string_ : `(total_power:{2000 TO Infinity]) AND (date:\"2024-01*\")`
    """
    try: 
     
       data, validation = search_custom_data(cloudant_search.designdoc_name, 
                                      cloudant_search.search_name,
                                      cloudant_search.search_string )
       
    except Exception as e:       
        error = {"exception": e }                  
        data  = str(error)
        verification = False        
        return { "data":data, "status":verification }     

    return { "data":data, "validation":validation }

###########
# Shelly
@app.get("/shelly_get_all_docs", response_model=Shelly_response)
def get_all_shelly_docs() -> Any:
    """
    This endpoint gets all `Shelly docs` from the the Cloudant database.
    """
    try: 
     
       data, validation = get_all_docs()
       
    except Exception as e:       
        error = {"exception": e }                  
        data  = str(error)
        verification = False        
        return { "data":data, "status":verification }     

    return { "data":data, "validation":validation }

@app.get("/shelly_save_data", response_model=Shelly_response)
def save_shelly_data() -> Any:
    """
    This endpoint saves the `Shelly data` in following `JSON` format.
    ```json
    {
        "emeters": [
            {
                "power": 337.36,
                "pf": 0.86,
                "current": 1.77,
                "voltage": 222.25,
                "is_valid": True,
                "total": 13098.7,
                "total_returned": 0.3
            },
            {
                "power": 9.44,
                "pf": 0.65,
                "current": 0.07,
                "voltage": 223.68,
                "is_valid": True,
                "total": 6781.7,
                "total_returned": 0.0
            },
            {
                "power": 212.4,
                "pf": 0.92,
                "current": 1.04,
                "voltage": 222.73,
                "is_valid": True,
                "total": 8667.1,
                "total_returned": 0.0
            }
        ],
        "date": "25-12-2023_15-27-13",
        "total_power": 559.2
    }
    ```
    """
    return save_shelly_data_job()

###########
# Grafana `JSON GrafanaJsonDatasource`
@app.post("/metrics")
async def grafana_json_datasource_metrics(response: Response, request: Request) -> Any:
    """
    This endpoint is related to grafana integration and define the metrics that can be select in Grafana.
    """
    body = await request.body()
    logging.debug(f"\nRequest body:\n{type(body)}\n")
    try:
        body_data = json.loads(body)
        logging.debug(f"\nRequest body:\n{body_data}\n")
    except Exception as e:       
        error = {"exception": e }                  
        logging.debug(f"{error}")
        response.status_code = HTTP_500_INTERNAL_SERVER_ERROR 

    return json_datasource_metrics()

@app.post("/metric-payload-options")
async def grafana_json_datasource_metric_payload_options( response: Response, request: Request) -> Any:
    """
    This endpoint is related to Grafana `JSON` integration. \n
    The endpoint returns the metrics payload options.
    """
    body = await request.body()
    logging.debug(f"\nRequest body:\n{type(body)}\n")
    try:
        if type(body) == bytes: 
             body_data = json.loads(body)
             logging.debug(f"\nRequest body:\n{body_data}\n")
        else:
            error = {"error": "no content in the request" }                  
            logging.debug(f"{error}")
            response.status_code = HTTP_500_INTERNAL_SERVER_ERROR 
    except Exception as e:       
        error = {"exception": e }                  
        logging.debug(f"{error}")
        response.status_code = HTTP_500_INTERNAL_SERVER_ERROR 
   
    return json_datasource_metric_payload_options()

@app.post("/query")
async def grafana_json_datasource_query(response: Response, request: Request) -> Any: 
    """
    This endpoint is related to Grafana `JSON` integration and selects the query.\n
    
    ! **The post request format is currently not implemented.** !\n

    1. In Grafana you need to insert provide following query data in the payload.
       You have the `search_option`: 
       * `search`: Here you can provide a `search_topic` and a `search_string` for this single topic.
       * `view`: Just returns all existing data in the database.
       * `custom`: You can define your custom search string

    ```json
    {
        "search_option":"search", # search, 
                                  # view, 
                                  # custom
        "search_topic":"date", # data, total_power, 
                               # phase1>3_total, phase1>3_total_returned
                               # phase1>3_power
        "search_string":"\"2024-01-03*\""
    }
    ```

    2. This is the full JSON format that is send from Grafana.

    ```json
      { "app": "panel-editor", 
        "requestId": "Q101", 
        "timezone": "browser", 
        "panelId": 1, 
        "dashboardUID": "None", 
        "range": {"from": "2024-01-07T13:34:33.167Z", 
                  "to": "22024-01-07T19:34:33.167Z2", 
                  "raw": {"from": "now-6h", 
                          "to": "now"}
                  }, 
        "timeInfo": "", 
        "interval": "10s", 
        "intervalMs": 10000, 
        "targets": [ { "datasource":{
                                     "type": "simpod-json-datasource", 
                                     "uid": "a9c0a9de-0e0b-4e5d-add7-05caa550b8a5"
                                    }, 
                                    "refId": "A", 
                                    "editorMode": "code", 
                                    "payload":{
                                        "search_option":"search",
                                        "search_topic":"date",
                                        "search_string":"\"2024-01-03*\""
                                    }, 
                                    "target": "shelly3emmetric"
                      }
                    ], 
        "maxDataPoints": 1760, 
        "scopedVars": {"__interval": {"text": "10s", 
                                        "value": "10s"}, 
                        "__interval_ms": { "text": "10000", 
                                           "value": 10000
                                        }
                        }, 
        "startTime": 1704656073167, 
        "rangeRaw": {"from": "now-6h", 
                     "to": "now"
                    }, 
        "filters": [], 
        "adhocFilters": []
     }
    ```
    """

    body = await request.body()
    
    try:
        logging.debug(f"\nRequest body:\n{type(body)}\n")
        if type(body) == bytes: 
            body_data = json.loads(body)
            logging.debug(f"\nRequest body:\n{body_data}\n")
            targets = body_data["targets"]
            payload = targets[0]["payload"]
            logging.debug(f"\n{payload}")

            if (payload["search_option"]=="view"):
                data, verification = view_all()
                if(verification == False):
                            error = {"error": "view_all" }                  
                            print(f"{error}")
                            response.status_code = HTTP_500_INTERNAL_SERVER_ERROR 
                            data = empty_data()

            elif (payload["search_option"]=="search"):
                searchtopic = payload["search_topic"]
                searchstring = payload["search_string"]
                data, verification = search_all(searchtopic, searchstring)
                if(verification == False):
                            error = {"error": "search_all" }                  
                            print(f"{error}")
                            response.status_code = HTTP_500_INTERNAL_SERVER_ERROR 
                            data = empty_data()
            elif (payload["search_option"]=="custom"):
                searchtopic = payload["search_topic"]
                searchstring = payload["search_string"]
                data, verification = search_all_custom(searchstring)
                if(verification == False):
                            error = {"error": "search_all_custom" }                  
                            print(f"{error}")
                            response.status_code = HTTP_500_INTERNAL_SERVER_ERROR 
                            data = empty_data()
            else:
                error = {"error": "unvailid search option" }                  
                logging.debug(f"{error}")
                response.status_code = HTTP_500_INTERNAL_SERVER_ERROR 
                data = empty_data()
        else:
            error = {"error": "no content in the request" }                  
            logging.debug(f"{error}")
            data = empty_data()
            response.status_code = HTTP_500_INTERNAL_SERVER_ERROR 
  
    except Exception as e:       
        error = {"exception query": e }                  
        print(f"{error}")
        response.status_code = HTTP_500_INTERNAL_SERVER_ERROR 
        data = empty_data()  

    return data

@app.post("/variable")
async def grafana_json_datasource_variable(response: Response, request: Request) -> Any: 
    """
    This endpoint is related to Grafana `JSON` integration. \n
    The endpoint returns the variable values.
    """
    body = await request.body()
    logging.debug(f"\nRequest body:\n{type(body)}\n")
    try:
        if type(body) == bytes: 
             body_data = json.loads(body)
             logging.debug(f"\nRequest body:\n{body_data}\n")
        else:
            error = {"error": "no content in the request" }                  
            logging.debug(f"{error}")
            response.status_code = HTTP_500_INTERNAL_SERVER_ERROR 
             
    except Exception as e:       
        error = {"exception": e }                  
        logging.debug(f"{error}")
        response.status_code = HTTP_500_INTERNAL_SERVER_ERROR 
   
    return json_datasource_variable()


######################################
# Open API defintion
def custom_openapi():
    
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Shelly3EM-Cloudant-Grafana-connection-server",
        version="1.0.0",
        description="`Shelly 3EM Cloudant Grafana connection server` provides functionality to interact with and manage data in a Cloudant database, retrieve IBM Cloud configuration information, and schedule tasks to save Shelly data.",
        routes=app.routes,
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__=="__main__":
    import uvicorn
    from uvicorn.config import LOGGING_CONFIG
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s - %(client_addr)s - %(request_line)s %(status_code)s %(message)s"
    uvicorn.run(app,host="0.0.0.0",port=8081)