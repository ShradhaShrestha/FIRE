from copy import deepcopy
import datetime as dt
from IPython.display import HTML
import json
import pandas as pd
from arcgis.gis import GIS
import arcgis.network as network
import arcgis.geocoding as geocoding
from arcgis.features import FeatureLayer, FeatureSet, FeatureCollection
import arcgis.features.use_proximity as use_proximity

my_gis = GIS(profile="fire_brickHack")

sample_cities = my_gis.content.search('title:"USA Major Cities" type:Feature Service owner:esri*',
                                      outside_org=True)[9]

stops_cities = ['San Francisco', 'San Jose']
values = "'" + "', '".join(stops_cities) + "'"


#block
stops_cities_fl = FeatureLayer(sample_cities.url + "/0")
type(stops_cities_fl)


stops_cities_fset = stops_cities_fl.query(where="ST in ('CA')  AND NAME IN ({0})".format(values), as_df=False)

def re_order_stop_cities(fset=stops_cities_fset, start_city="Miami", end_city="San Francisco"):
    stops_cities_flist = []
    last_city = None

    for ea in fset:
        if ea.attributes['NAME'] == start_city:
            stops_cities_flist.insert(0, ea)
        elif ea.attributes['NAME'] == end_city:
            last_city = ea
        else:
            stops_cities_flist.append(ea)
    stops_cities_flist.append(last_city)

    return FeatureSet(stops_cities_flist)

re_ordered_stops_cities = list(map(lambda x: x.attributes['NAME'], re_ordered_stops_cities_fset))

#find routes
tart_time = int(dt.datetime.now().timestamp() * 1000)

result = network.analysis.find_routes(re_ordered_stops_cities_fset, time_of_day=start_time,
                                      time_zone_for_time_of_day="UTC",
                                      preserve_terminal_stops="Preserve None",
                                      reorder_stops_to_find_optimal_routes=True,
                                      save_output_na_layer=True)
