from .load_env import load_apikey_env
from .requests_cloudant import get_view, search_data, search_custom_data
import json
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

def convert_search_all_data(search_topic,search_string):
    # predefinied search
    designdoc_name = "design_search_idx_results_emeters_all"
    search_name = "search_idx_results_emeters_all"
    
    try: 
     
       data, validation = search_data(designdoc_name,search_name,search_topic,search_string)
       
       if (validation["status"] == True): 
          # Build needed dataformat for the Grafana JSON integration
          # [{"columns":columns,
          #          "rows":rows,
          #          "type":"table"
          #          }
          #        ]
          verification = True
          columns = [
                        {"text":"time", "type":"time"},
                        {"text":"total-power", "type":"time"},
                        {"text":"phase1-total", "type":"number"},
                        {"text":"phase1-power", "type":"number"},
                        {"text":"phase1-total-returned", "type":"number"},
                        {"text":"phase2-total", "type":"number"},
                        {"text":"phase2-power", "type":"number"},
                        {"text":"phase2-total-returned", "type":"number"},
                        {"text":"phase3-total", "type":"number"},
                        {"text":"phase3-power", "type":"number"},
                        {"text":"phase3-total-returned", "type":"number"}
                    ]

          # convert return value to needed JSON format
          data_json_text = json.dumps(data)
          input_json = json.loads(data_json_text)
          rows = []
          
          for item in input_json["result"]["rows"]:
              value = item["fields"]
              entry = [value["date"],
                       value["total_power"],
                       value["phase1_total"],value["phase1_power"],value["phase1_total_returned"],
                       value["phase2_total"],value["phase2_power"],value["phase2_total_returned"],
                       value["phase3_total"],value["phase3_power"],value["phase3_total_returned"]
                      ]
              rows.append(entry)

          data = [{"columns":columns,
                    "rows":rows,
                    "type":"table"
                  }
                 ]
          logging.debug(f"{data}\n\n")
       else:                 
                    error = {"error": "validation failed" }                  
                    data  = str(error)
                    verification = False        
                    return { "data":data}, {"status":verification }  
           
              
    except Exception as e:

        error = {"exception `gr convert search all`": e }                  
        data  = str(error)
        verification = False
        logging.info(f"{data}\n\n")       
        return { "data":data, "status": verification }  
       
    return data, {"status":verification }

def convert_search_custom_all_data(search_string):
    # predefinied search
    designdoc_name = "design_search_idx_results_emeters_all"
    search_name = "search_idx_results_emeters_all"
    
    try: 
     
       data, validation = search_custom_data(designdoc_name,search_name,search_string)
       
       if (validation["status"] == True): 
          # Build needed dataformat for the Grafana JSON integration
          # [{"columns":columns,
          #          "rows":rows,
          #          "type":"table"
          #          }
          #        ]
          verification = True
          columns = [
                        {"text":"time", "type":"time"},
                        {"text":"total-power", "type":"number"},
                        {"text":"phase1-total", "type":"number"},
                        {"text":"phase1-power", "type":"number"},
                        {"text":"phase1-total-returned", "type":"number"},
                        {"text":"phase2-total", "type":"number"},
                        {"text":"phase2-power", "type":"number"},
                        {"text":"phase2-total-returned", "type":"number"},
                        {"text":"phase3-total", "type":"number"},
                        {"text":"phase3-power", "type":"number"},
                        {"text":"phase3-total-returned", "type":"number"}
                    ]

          # convert return value to needed JSON format
          data_json_text = json.dumps(data)
          input_json = json.loads(data_json_text)
          rows = []
          
          for item in input_json["result"]["rows"]:
              value = item["fields"]
              entry = [value["date"],
                       value["total_power"],                      
                       value["phase1_total"],value["phase1_power"],value["phase1_total_returned"],
                       value["phase2_total"],value["phase2_power"],value["phase2_total_returned"],
                       value["phase3_total"],value["phase3_power"],value["phase3_total_returned"]
                      ]
              rows.append(entry)

          data = [{"columns":columns,
                    "rows":rows,
                    "type":"table"
                  }
                 ]
          logging.debug(f"{data}\n\n")
       else:                 
                    error = {"error": "validation failed" }                  
                    data  = str(error)
                    verification = False        
                    return { "data":data}, {"status":verification }  
           
              
    except Exception as e:

        error = {"exception `gr convert search custom`": e }                  
        data  = str(error)
        verification = False
        logging.info(f"{data}\n\n")       
        return { "data":data, "status": verification }  
       
    return data, {"status":verification }

def convert_view_all_data():
    # predefinied view
    designdoc_name = "design_view_all_docs"
    view_name = "view_all_docs"
    
    try: 
     
       data, validation = get_view(designdoc_name,view_name)
       
       if (validation["status"] == True): 
          # Build needed dataformat for the Grafana JSON integration
          # [{"columns":columns,
          #          "rows":rows,
          #          "type":"table"
          #          }
          #        ]
          verification = True
          columns = [
                        {"text":"time", "type":"time"},
                        {"text":"total-power", "type":"number"},
                        {"text":"phase1-total", "type":"number"},
                        {"text":"phase1-power", "type":"number"},
                        {"text":"phase1-total-returned", "type":"number"},
                        {"text":"phase2-total", "type":"number"},
                        {"text":"phase2-power", "type":"number"},
                        {"text":"phase2-total-returned", "type":"number"},
                        {"text":"phase3-total", "type":"number"},
                        {"text":"phase3-power", "type":"number"},
                        {"text":"phase3-total-returned", "type":"number"}
                    ]

          # convert return value to needed JSON format
          data_json_text = json.dumps(data)
          input_json = json.loads(data_json_text)
          rows = []
          
          for item in input_json["result"]["rows"]:
              value = item["value"]
              entry = [value["date"],
                       value["total_power"],
                       value["phase1_total"],value["phase1_power"],value["phase1_total_returned"],
                       value["phase2_total"],value["phase2_power"],value["phase2_total_returned"],
                       value["phase3_total"],value["phase3_power"],value["phase3_total_returned"]
                      ]
              rows.append(entry)

          data = [{"columns":columns,
                    "rows":rows,
                    "type":"table"
                  }
                 ]
          logging.debug(f"{data}\n\n")
       else:                 
                    error = {"error": "validation failed" }                  
                    data  = str(error)
                    verification = False        
                    return { "data":data}, {"status":verification }  
           
              
    except Exception as e:

        error = {"exception `gr convert view`": e }                  
        data  = str(error)
        verification = False
        logging.info(f"{data}\n\n")          
        return { "data":data, "status": verification }  
       
    return data, {"status":verification }

def empty_data():
     columns = [
                    {"text":"Time", "type":"time"},
                    {"text":"Phase 1 - Total", "type":"number"},
                    {"text":"Phase 1 - Power", "type":"number"},
                    {"text":"Phase 1 - Total power", "type":"number"},
                    {"text":"Phase 1 - Total returned", "type":"number"},
                    {"text":"Phase 2 - Total", "type":"number"},
                    {"text":"Phase 2 - Power", "type":"number"},
                    {"text":"Phase 2 - Total power", "type":"number"},
                    {"text":"Phase 2 - Total returned", "type":"number"},
                    {"text":"Phase 3 - Total", "type":"number"},
                    {"text":"Phase 3 - Power", "type":"number"},
                    {"text":"Phase 3 - Total power", "type":"number"},
                    {"text":"Phase 3 - Total returned", "type":"number"},
                ]
     rows = ["0000-00-00_00-00-00",0,0,0,0,0,0,0,0,0,0,0,0]
     data = [{"columns":columns,
              "rows":rows,
              "type":"table"
             }
            ]
     return data

def json_datasource_metric_payload_options():
    value = [{ 
                "label": "namespace",
                "value": "shelly3em"
             },
             {
                "label": "metric",
                "value": "shelly3em"   
             },
             {
                "label": "instanceId",
                "value": "shelly3em-cloudant-grafana-connection-server"   
             }
             ]
    return value

def json_datasource_variable():
    value = [{"__text":"search_option", "__value":"search"},
             {"__text":"search_topic", "__value":"date"},
             {"__text":"search_string", "__value":"2024*"}
            ]
    return value
 
def json_datasource_metrics():
    value = [{
                "label": "Shelly 3EM metric", # Optional. If the value is empty, use the value as the label
                "value": "namespace", # The value of the option.
                "payloads": [{ # Configuration parameters of the payload.
                                "label": "Shelly 3EM metric", # The label of the payload. If the value is empty, use the value as the label.
                                "name": "namespace", # The name of the payload. If the value is empty, use the name as the label.
                                "type": "select", # If the value is select, the UI of the payload is a radio box. If the value is multi-select, the UI of the payload is a multi selection box; if the value is input, the UI of the payload is an input box; if the value is textarea, the UI of the payload is a multiline input box. The default is input.
                                "placeholder": "Please select shelly metric source", # Input box / selection box prompt information.
                                "reloadMetric": "true", # Whether to overload the metrics API after modifying the value of the payload.
                                "width": 10, # Set the input / selection box width to a multiple of 8px. 
                                "options": [{ # If the payload type is select / multi-select, the list is the configuration of the option list.
                                              "label": "namespace", # The label of the payload select option.
                                              "value": "shelly3em", # The label of the payload value.
                                            },
                                            {
                                              "label": "metric", # The label of the payload select option.
                                              "value": "view", # The label of the payload value.  
                                            },
                                            {
                                              "label": "instanceId",
                                              "value": "shelly3em-cloudant-grafana-connection-server"   
                                            }]
                            },
                            {
                                "name": "metric",
                                "type": "select"
                            },
                            {
                                "name": "instanceId",
                                "type": "select"
                            }]
             },
             {
                "value": "Shelly3EMmetricLast",
                "payloads": [{
                                "name": "namespache",
                                "type": "select"
                            },
                            {
                                "name": "metric",
                                "type": "select"
                            },
                            {
                                "name": "instanceId",
                                "type": "select"
                            }]
              }]
    return value