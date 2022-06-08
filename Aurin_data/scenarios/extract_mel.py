import json
from geojson import dump, FeatureCollection, Feature, Polygon, MultiPolygon
import pandas as pd

with open("Australia_sa3.json") as f:
    data = json.load(f)

filtered_feature = []
features = data['features']

# find areas within greater melbourne area
for i in features:
    if i['properties']['GCC_NAME16'] == 'Greater Melbourne':
        coordinates = i['geometry']['coordinates']
        properties = i['properties']
        data_type = i['geometry']['type']
        # find polygons
        if data_type == 'Polygon':
            polygon = Polygon(coordinates)
            single_feature = Feature(geometry=polygon, properties=properties)
            filtered_feature.append(single_feature)
        # find multipolygons
        elif data_type == 'MultiPolygon':
            multi = MultiPolygon(coordinates)
            single_feature = Feature(geometry=multi, properties=properties)
            filtered_feature.append(single_feature)

feature_collection = FeatureCollection(filtered_feature)

# export
with open('melbourne_division.geojson', 'w') as f:
    json.dump(feature_collection, f)