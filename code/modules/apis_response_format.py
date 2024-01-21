from pydantic import BaseModel
from typing import List

### Sub type specifictions

#class Document(BaseModel):
#     text: str 
#     title: str 
#     document_url: str

class BasicResult(BaseModel):
    result: str

class Result(BaseModel):
    result: List[dict]

class Status (BaseModel):
    status: bool

### Responses

class Get_ibmcloud_config(BaseModel):
    ibmcloud_config: dict 
    validation: bool

class IBMCloud_info(BaseModel):
    data: dict
    validation: dict

class Get_access_token(BaseModel):
    token: BasicResult
    validation: Status

class Health(BaseModel):
    status: str

class Cloudant_response(BaseModel):
    data: dict
    validation: dict

class Shelly_response(BaseModel):
    data: dict
    validation: dict

class Schedule_response(BaseModel):
    schedule: bool