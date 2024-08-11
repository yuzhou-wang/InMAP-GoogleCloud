# HTTP server
# app.py
from typing import List, Optional

from fastapi import FastAPI, Request
from WhiteBeltService import WhiteBeltService, Coordinate
from LlmQuery import LlmQuery
from LlmInmap import LlmInmap

app = FastAPI()
white_belt_service = WhiteBeltService()
llm_query = LlmQuery()
llm_inmap = LlmInmap()

@app.post("/white_belt/single")
#def read_item(stack_height: float = 0, pollutant: str = "pNO3", source_lat: float = 47.6097, source_lon: float = -122.3422, receptor_lat: float = 47.6555, receptor_lon: float = -122.3032, reduction_value: float = 1):
async def white_belt_single(info: Request):
    req_info = await info.json()

    return white_belt_service.calculate(stack_height=req_info["stack_height"], 
    pollutant=req_info["pollutant"], source_lat=req_info["source_lat"], 
    source_lon=req_info["source_lon"], receptor_lat=req_info["receptor_lat"], receptor_lon=req_info["receptor_lon"], reduction_value=req_info["reduction_value"])

# uvicorn app:app --host 0.0.0.0 --port 4444
# curl -XPOST -d '{"stack_height":0,"pollutant":"PrimaryPM25","source_lat":47.6097, "source_lon":-122.3422, "receptor_lat":47.6555, "receptor_lon":-122.3032,"reduction_value":1}' 'http://localhost:4444/white_belt/single'

#@app.get("/white_belt/batch")
#def read_item(emis_type: str, source: List[Coordinate], receptor: List[Coordinate], stack_height: float):
#    return white_belt_service.calculate_batch(...)

# llm function
@app.post("/white_belt/llm")
#def read_item(stack_height: float = 0, pollutant: str = "pNO3", source_lat: float = 47.6097, source_lon: float = -122.3422, receptor_lat: float = 47.6555, receptor_lon: float = -122.3032, reduction_value: float = 1):
async def llm_query_app(info: Request):
    req_info = await info.json()

    return llm_query.generate_content(user_input=req_info["user_input"])

# curl -XPOST -d '{"my_input":"return me a dictionary of lat and lon of UC Berkeley"}' 'http://localhost:4444/white_belt/llm'
# curl -XPOST -d '{"my_input":"return me a dictionary of lat and lon of San Jose Mineta International Airport"}' 'http://localhost:4444/white_belt/llm'
##curl -XPOST -d '{"my_input":"assume that you are an input interpreter: you will be given a question like how the emission at place X affects the air pollution at place Y. You are expected to output a dictionary as json format. In this json dictionary, there are two keys, source_place and pollution_place. The source_place has the information of place X, while the pollution_place has the information of place Y. In each key, it is a dictionary that has three key-value combination. The first key is original_value which is the original input of places. The second key is zipcode which is the geocoded zipcode of the places. The third key is coordinates which is the geocoded coordinates of the places. How is the emission at San Francisco airport affects the pollution in UC berkeley?"}' 'http://0.0.0.0:4444/white_belt/llm'

## curl -XPOST -d '{"my_input":"assume that you are an input interpreter: you will be given a question like how the emission at place X affects the air pollution at place Y. You are expected to output a dictionary as json format. In this json dictionary, there are three keys, source_place, receptor_place, and emission value. The source_place has the information of place X. The pollution_place has the information of place Y. The emission value has the information of emission. For source_place and receptor_place, each include a dictionary that has three key-value combination. The first key is original_value which is the original input of places. The second key is zipcode which is the geocoded zipcode of the places. The third key is coordinates which is the geocoded coordinates of the places. For emission key, if the question include emission information such at 1 ton/year or 1 ton, please return the value, otherwise, return 1 ton/year (default). How is the emission at San Francisco airport affects the pollution in UC berkeley?."}' 'http://0.0.0.0:4444/white_belt/llm'

## curl -XPOST -d '{"my_input":"assume that you are an input interpreter: you will be given a question like how the emission at place X affects the air pollution at place Y. You are expected to output a dictionary as json format. In this json dictionary, there are three keys, source_place, receptor_place, and emission value. The source_place has the information of place X. The pollution_place has the information of place Y. The emission value has the information of emission. For source_place and receptor_place, each include a dictionary that has three key-value combination. The first key is original_value which is the original input of places. The second key is zipcode which is the geocoded zipcode of the places. The third key is coordinates which is the geocoded coordinates of the places. For emission key, if the question include emission information such at 1 ton/year or 1 ton, please return the value, otherwise, return 1 ton/year (default). how is the 2 ton/year emission at San Francisco airport affects the pollution in UC berkeley?."}' 'http://0.0.0.0:4444/white_belt/llm'

## curl -XPOST -d '{"user_input":"How is the 2 ton/year emission at San Francisco airport affects the pollution in UC berkeley?."}' 'http://0.0.0.0:4444/white_belt/llm'

@app.post("/white_belt/llm_inmap")
async def llm_inmap_app(info: Request):
    req_info = await info.json()

    input_dict = llm_inmap.dict_from_llm(user_input_inmap = req_info["user_input_inmap"])
    return llm_inmap.inmap_from_dict(input_dict = input_dict)

## curl -XPOST -d '{"user_input_inmap":"How is the 2 ton/year emission at San Francisco airport affects the pollution in UC berkeley?."}' 'http://0.0.0.0:4444/white_belt/llm_inmap'

## curl -XPOST -d '{"user_input_inmap":"How is the Stanford campus affected by San Jose airport?."}' 'http://0.0.0.0:4444/white_belt/llm_inmap'