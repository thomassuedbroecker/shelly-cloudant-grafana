from pydantic import BaseModel

##############
# Cloudant
class Cloudant_view(BaseModel):
    view_name: str
    designdoc_name: str

class Cloudant_search(BaseModel):
    search_name: str
    designdoc_name: str
    search_topic: str
    search_string: str

##############
# JSON Grafana !"not used"! at the moment
class Grafana_json_payload_options(BaseModel):
    metric: str
    payload: dict
    name:str

class Grafana_json_query(BaseModel):
    search_name: str
    search_topic: str
    search_string: str
