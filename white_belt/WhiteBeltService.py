# import dataclass
import dataclasses as dataclass
from typing import List

#import geopandas as gpd
from shapely.geometry import Point, Polygon, LinearRing
import pandas as pd

#import numpy as np
from netCDF4 import Dataset
from typing import List #,Dict
import pandas as pd
from google.cloud import storage


@dataclass.dataclass
class Coordinate:
    latitude: float
    longitude: float

class StorageClient:
    def __init__(self):
        pass
        # self.client = storage.Client()
        # export credentials in your own client following this webpage https://googleapis.dev/python/google-api-core/latest/auth.html

    def download(self,filepath, is_downloaded = True):
        if not is_downloaded:
            wget 
            #destination = "/tmp/" + filepath.split("/")[-1]
            
            #bucket_name = "inmap-uw-dev1"
            #bucket = self.client.get_bucket(bucket_name)
            #blob = bucket.blob(filepath)
            #blob.download_to_filename(destination)
            #print(f"{filepath} downloaded to {destination}.")
        else:
            destination = f"""/home/yuzhou/Downloads/InMAP/{filepath.split("/")[-1]}"""
            print(f"file already exists in {destination}")
        return destination
    
    # def delete(self,filepath):

class WhiteBeltService:
    ## select specific isrm slice
    def select_slice(self,stack_height: float, pollutant: str):
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

        return filename
    ## read file
    #    isrm_slice_file = Dataset(filename, mode='r')
    #    isrm_slice = isrm_slice_file.variables[pollutant][0]

    ## conversion from latitude longitude to isrm grid value  
    def latlon_to_isrm(self, lat:float, lon:float):
        # create point from latitude and longitude
        pt = Point(lon, lat)
        
        # file down potential isrm grid matches with bounds
        if(self.latlon_cross['lat0'].dtype != 'float64'):
            self.latlon_cross['lat0'] = self.latlon_cross['lat0'].apply(pd.to_numeric, downcast='float', errors='coerce')
        if(self.latlon_cross['lon0'].dtype != 'float64'):
            self.latlon_cross['lon0'] = self.latlon_cross['lon0'].apply(pd.to_numeric, downcast='float', errors='coerce')

        sm_latlon = self.latlon_cross[self.latlon_cross['lon0'] > lon - 1]
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
    def emission_concentration(self, isrm_slice: List, source_lat: float, source_lon: float, receptor_lat: float, receptor_lon: float, reduction_value: float):
        ## Reduction values in tonne/year          
        CONV_CONST = 31710
        source = self.latlon_to_isrm(source_lat, source_lon)
        receptor = self.latlon_to_isrm(receptor_lat, receptor_lon)
                    
        # value given is in t/yr
        isrm_value = isrm_slice[source][receptor]
            
        final_delta = isrm_value * CONV_CONST * reduction_value
        return final_delta   

    def white_belt(self, stack_height: float, pollutant: str, source_lat: float, source_lon: float, receptor_lat: float, receptor_lon: float, reduction_value: float):
        isrm_slice = self.select_slice(stack_height, pollutant)
        concentration_change = self.emission_concentration(isrm_slice, source_lat, source_lon, receptor_lat, receptor_lon, reduction_value)
        return concentration_change

    ## TODO: I don't understand this part, we can discuss about it.
    def __init__(self) -> None:
        # Run all precalculated/reusable operations
        self.latlon_cross = pd.read_csv("./latlon_cross.csv",index_col=0)
        
        # all_slices = []
        # for slice in slices:
        #     slice_name = ...

        #     # TODO: Load data
        #     client = StorageClient()
        #     client.download(f"gs://inmap-uw-dev1/isrm_slice/{slice_name}")
        #     ...

        # slices_combined = self.select_slice(all_slices)

    def calculate(self, stack_height: float, pollutant: str, source_lat: float, source_lon: float, receptor_lat: float, receptor_lon: float, reduction_value: float):
        # Load data depending on stack-height and emission-type
        # Size of slices: 10 GB (Get a 16 GB machine)
        client = StorageClient()
        filename = self.select_slice(stack_height, pollutant)
        full_file_name = client.download(f"isrm_slice/{filename}")
    # read file
        isrm_slice_file = Dataset(full_file_name, mode='r')
        isrm_slice = isrm_slice_file.variables[pollutant][0]
        
        concentration_change = self.emission_concentration(isrm_slice, source_lat, source_lon, receptor_lat, receptor_lon, reduction_value)
        return concentration_change
