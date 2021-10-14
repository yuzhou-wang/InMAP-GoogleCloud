# import dataclass
import dataclasses as dataclass
from typing import List

import geopandas as gpd
from shapely.geometry import Point, Polygon, LinearRing
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
from typing import List, Dict
import pandas as pd

@dataclass.dataclass
class Coordinate:
    latitude: float
    longitude: float

class WhiteBeltService:
    ## select specific isrm slice
    def select_slice(stack_height: float, pollutant: str):
    # validate parameters
        emis_type = ["SOA", "PrimaryPM25", "pNH4", "pSO4", "pNO3"]
        if pollutant not in emis_type:
            raise Exception("varname not a valid emission type")
    # chose layer from stack_height
        if stack_height < 57:
            layer = 0
        elif stack_height < 379:
            layer = 1
        else:
            layer = 2
    # generate filename
        filename = pollutant+"L"+str(layer)+".nc"
    # read file
        isrm_slice_file = Dataset(filename, mode='r')
        isrm_slice = isrm_slice_file.variables[pollutant][0]
        return isrm_slice

    ## conversion from latitude longitude to isrm grid value  
    def latlon_to_isrm(lat:float, lon:float):
        # create point from latitude and longitude
        pt = Point(lon, lat)
        
        # file down potential isrm grid matches with bounds
        if(latlon_cross['lat0'].dtype != 'float64'):
            latlon_cross['lat0'] = latlon_cross['lat0'].apply(pd.to_numeric, downcast='float', errors='coerce')
        if(latlon_cross['lon0'].dtype != 'float64'):
            latlon_cross['lon0'] = latlon_cross['lon0'].apply(pd.to_numeric, downcast='float', errors='coerce')

        sm_latlon = latlon_cross[latlon_cross['lon0'] > lon - 1]
        sm_latlon = sm_latlon[sm_latlon['lon0'] < lon + 1]
        sm_latlon = sm_latlon[sm_latlon['lat0'] > lat - 1]
        sm_latlon = sm_latlon[sm_latlon['lat0'] < lat + 1]
        
        # loop through isrm grids and create polygons, return index of match
        for i in sm_latlon.index.tolist():
            coords = [(sm_latlon['lon0'][i], sm_latlon['lat0'][i]),
                    (float(sm_latlon['lon1'][i]), float(sm_latlon['lat1'][i])),
                    (float(sm_latlon['lon2'][i]), float(sm_latlon['lat2'][i])),
                    (float(sm_latlon['lon3'][i]), float(sm_latlon['lat3'][i]))]
        
            lr = LinearRing(coords)
            poly = Polygon(lr)
        
            if poly.contains(pt): 
                return i
        
        raise Exception("No match, expand selection bounds")

    ## A function to calcaulate concentration change from emission reduction   
    def emission_concentration(isrm_slice: List, source_lat: float, source_lon: float, receptor_lat: float, receptor_lon: float, reduction_value: float):
        ## Reduction values in tonne/year          
        CONV_CONST = 31710
        source = latlon_to_isrm(source_lat, source_lon, latlon_cross)
        receptor = latlon_to_isrm(receptor_lat, receptor_lon, latlon_cross)
                    
        # value given is in t/yr
        isrm_value = isrm_slice[source][receptor]
            
        final_delta = isrm_value * CONV_CONST * reduction_value
        return final_delta   

    def white_belt(stack_height: float, pollutant: str, source_lat: float, source_lon: float, receptor_lat: float, receptor_lon: float, reduction_value: float):
        isrm_slice = select_slice(stack_height, pollutant)
        concentration_change = emission_concentration(isrm_slice, source_lat, source_lon, receptor_lat, receptor_lon, reduction_value, latlon_cross)
        return concentration_change

    ## TODO: I don't understand this part, we can discuss about it.
    def __init__(self) -> None:
        # Run all precalculated/reusable operations
        self.isrm_pm25_l0 = select_slice('PM25L0.nc')
        self.latlon_cross = pd.read_csv("latlon_cross.csv")
        
        all_slices = []
        for slice in slices:
            slice_name = ...

            # TODO: Load data
            client = StorageClient()
            client.download(f"gs://nmap-trial/isrm_slice/{slice_name}")
            ...

        slices_combined = select_slice(all_slices)

    def calculate(emis_type: str, source_lat: float, source_lon: float, receptor_lat: float, receptor_lon: float, stack_height: float):
        # TODO: Load data depending on stack-height and emission-type
        # Size of slices: 10 GB (Get a 16 GB machine)
        

        # TODO: Calls white_belt

    def calculate_batch(emis_type: str, source: List[Coordinate], receptor: List[Coordinate], stack_height: float):
        