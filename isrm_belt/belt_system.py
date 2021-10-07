# Import package
import geopandas as gpd
from shapely.geometry import Point, Polygon, LinearRing
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import time

# Preperation functions
## Combine layers
def combine_layers(layer_0, layer_1, layer_2, varname):
    
    # validate parameters
    emis_type = ["SOA", "PrimaryPM25", "pNH4", "pSO4", "pNO3"]
    if varname not in emis_type:
        raise Exception("varname not a valid emission type")
    
    # read in netCDF4 Datasets
    isrm0 = Dataset(layer_0, mode='r')
    isrm1 = Dataset(layer_1, mode='r')
    isrm2 = Dataset(layer_2, mode='r')
    
    # convert to masked arrays
    isrm0_arr = isrm0[varname][0]
    isrm1_arr = isrm1[varname][0]
    isrm2_arr = isrm2[varname][0]
    
    # combine so that isrm[layer][source][receptor]
    isrm = []
    isrm.append(isrm0_arr)
    isrm.append(isrm1_arr)
    isrm.append(isrm2_arr)
    
    return isrm

## latlon to isrm grid
def latlon_to_isrm(lat, lon, latlon_crosswalk, emis_nei):
    # create point from latitude and longitude
    pt = Point(lon, lat)
    
    # file down potential isrm grid matches with bounds
    if(latlon_crosswalk['lat0'].dtype != 'float64'):
        latlon_crosswalk['lat0'] = latlon_crosswalk['lat0'].apply(pd.to_numeric, downcast='float', errors='coerce')
    if(latlon_crosswalk['lon0'].dtype != 'float64'):
        latlon_crosswalk['lon0'] = latlon_crosswalk['lon0'].apply(pd.to_numeric, downcast='float', errors='coerce')

    sm_latlon = latlon_crosswalk[latlon_crosswalk['lon0'] > lon - 1]
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

# White Belt
######################################################################################################
# white_belt: this function calculates the change in concentration of PM2.5 at a receptor location
#             based on a change in some change in concentration of an emission at a source location in t/yr
#
# Parameters: isrm - slice of isrm with desired emission at all 3 layers, such as that from combine_layers
#             emis_type - [SOA, PM25, NH4, SO4, NO3]
#             sector - ['all', 'afdust', 'othafdust', 'ag', 'othpt', 'othar', 'cmv', 'agfire', 'ptagfire', 
#                       'np_oilgas', 'onroad', 'ptnonipm', 'pt_oilgas', 'ptegu', 'rwc']
#             source_lat, source_lon - isrm source latitude and longitude
#             receptor_lat, receptor_lon - isrm source latitude and longitude
#             value - double value for change in emissions at source (if percent is True, 5% = 0.05)
#             emis_nei - geopandas dataframe of emissions (NEI Data) needed 
#             latlon_cross - pandas dataframe crosswalk btw isrm grid and latitude longitude geometry points
#             percent - boolean value: true if param value is a percentage, false if it is absolute (t/yr)
#                       default False
#             stack_height - stack height in m for layer. default 0
# 
# Returns: double value that is change in emissions at receptor location in t/yr
######################################################################################################
 
def white_belt(isrm, emis_type, source_lat, source_lon, receptor_lat, receptor_lon, value, emis_nei, 
               latlon_cross,sector = "all",percent=False, stack_height=0):
    
    # error checks for emis_type: make sure it is a valid value
    emis_types = ["SOA", "PM25", "NH4", "SO4", "NO3"]
    if emis_type not in emis_types:
        raise Exception("emis_type not a valid emission type")
    
    CONV_CONST = 28767
    isrm_delta = 0
    layer = 0
        
    source = latlon_to_isrm(source_lat, source_lon, latlon_cross, emis_nei)
    receptor = latlon_to_isrm(receptor_lat, receptor_lon, latlon_cross, emis_nei)
    
    # determine layer based on stack height
    if stack_height < 57:
        layer = 0
    elif stack_height < 379:
        layer = 1
    else:
        layer = 2
    
    # value given is a percentage, access nei to calculate value in t/yr
    if percent:
        
        # drop all emis rows where value of emis_type is 0
        if emis_type == "SOA":
            varname = "VOC"
        elif emis_type == "PM25":
            varname = "PM25"
        elif emis_type == "NH4":
            varnme = "NH3"
        elif emis_type == "SO3":
            varname = "SOx"
        else:
            varname = "NOx"
        
        
        sm_emis_nei = emis_nei[emis_nei[varname] != 0]             # file by emission
        sm_emis_nei = sm_emis_nei[sm_emis_nei['isrm'] == source]   # file by source grid
        
        if(sector != 'all'):
            sm_emis_nei = sm_emis_nei[sm_emis_nei['Sector'] == sector]
   
        # file down by height
        if(layer == 0):
            sm_emis_nei = sm_emis_nei[sm_emis_nei['Height'] < 57]
        elif(layer == 1):
            sm_emis_nei = sm_emis_nei[sm_emis_nei['Height'] >= 57]
            sm_emis_nei = sm_emis_nei[sm_emis_nei['Height'] < 379]
        else:
            sm_emis_nei = sm_emis_nei[sm_emis_nei['Height'] > 379]

        # reset value to be t/yr
        value *= sm_emis_nei[varname].sum()
         
    # value given is in t/yr
    isrm_delta = isrm[layer][source][receptor]
        
    final_delta = isrm_delta * CONV_CONST * value
    return final_delta

