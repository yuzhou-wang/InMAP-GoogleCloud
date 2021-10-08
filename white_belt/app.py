# HTTP server
# app.py
from typing import List, Optional

from fastapi import FastAPI
from whitebelt_service import WhiteBeltService, Coordinate

app = FastAPI()
white_belt_service = WhiteBeltService()

@app.get("/white_belt/single")
def read_item(emis_type: str, source_lat: float, source_lon: float, receptor_lat: float, receptor_lon: float, stack_height: float):
    return white_belt_service.calculate(...)

@app.get("/white_belt/batch")
def read_item(emis_type: str, source: List[Coordinate], receptor: List[Coordinate], stack_height: float):
    return white_belt_service.calculate_batch(...)
