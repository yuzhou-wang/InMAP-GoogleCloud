# from isrm_belt import belt_system
# import geopandas as gpd

# emis_nei = gpd.read_file('Data/nei_isrm.shp')
# isrm_pm25 = belt_system.combine_layers('Data/isrm_slice/PM25L0.nc', 'Data/isrm_slice/PM25L1.nc', 
#                            'Data/isrm_slice/PM25L2.nc', 'PrimaryPM25')
# isrm_crosswalk = gpd.read_file("Data/isrm_boundaries_latlons.csv")

from white_belt import WhiteBeltService

temp = WhiteBeltService.WhiteBeltService()
conc_change = temp.calculate(0,"pNO3",47.6097, -122.3422, 47.6555, -122.3032,1)
print(conc_change)