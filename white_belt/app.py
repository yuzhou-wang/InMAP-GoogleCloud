# HTTP server
# app.py
from typing import List, Optional

from fastapi import FastAPI, Request
from WhiteBeltService import WhiteBeltService, Coordinate

app = FastAPI()
white_belt_service = WhiteBeltService()

@app.post("/white_belt/single")
#def read_item(stack_height: float = 0, pollutant: str = "pNO3", source_lat: float = 47.6097, source_lon: float = -122.3422, receptor_lat: float = 47.6555, receptor_lon: float = -122.3032, reduction_value: float = 1):
async def white_belt_single(info: Request):
    req_info = await info.json()

    return white_belt_service.calculate(stack_height=req_info["stack_height"], 
    pollutant=req_info["pollutant"], source_lat=req_info["source_lat"], 
    source_lon=req_info["source_lon"], receptor_lat=req_info["receptor_lat"], receptor_lon=req_info["receptor_lon"], reduction_value=req_info["reduction_value"])

# uvicorn app:app --host 0.0.0.0 --port 4444
# curl -XPOST -d '{"stack_height":0,"pollutant47.6097, "source_lon":-122.3422, "receptor_lat":47.6555, "receptor_lon":-122.3032,"reduction_value":1}' 'http://localhost:4444/white_belt/single'

#@app.get("/white_belt/batch")
#def read_item(emis_type: str, source: List[Coordinate], receptor: List[Coordinate], stack_height: float):
#    return white_belt_service.calculate_batch(...)
