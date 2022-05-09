import geopandas as gpd
import country_converter as coco
import pandas as pd
import json
import folium

import pandas as pd
pd.set_option('display.max_columns', 500)
import numpy as np
import plotly.express as px
import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry import Point
from matplotlib import pyplot as plt
import folium


def convert_country_names_to_codes(df, input_col_name, output_col_name):
    #df['code'] = coco.convert(names=list(df['Country or region']), to='ISO3')
    df[output_col_name] = coco.convert(names=list(df[input_col_name]), to='ISO3')


def merge_country_geometry_data(df):
    shapefile = 'data/ne_50m_admin_0_countries.shp'
    gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    gdf.columns = ['country', 'country_code', 'geometry']
    merged = gdf.merge(df, left_on='country_code', right_on='code')
    return merged


datafile = 'data/2019.csv'
gdf_worldhappiness = pd.read_csv(datafile)
convert_country_names_to_codes(gdf_worldhappiness, 'Country or region', 'code')
merged = merge_country_geometry_data(gdf_worldhappiness)

gdf_worldhappiness_point = merged.copy()
gdf_worldhappiness_point['geometry'] = gdf_worldhappiness_point['geometry'].centroid
#gdf_worldhappiness_point["lat"] = gdf_worldhappiness_point.center.map(lambda p: p.x)
#gdf_worldhappiness_point["long"] = gdf_worldhappiness_point.center.map(lambda p: p.y)

#gdf_worldhappiness_2019 = gdf_worldhappiness[gdf_worldhappiness['year'] == 2019]
#gdf_worldhappiness_point_2019 = gdf_worldhappiness_point[gdf_worldhappiness_point['year'] == 2019]

"""
fig, ax = plt.subplots(figsize=(16,16))
marker = gdf_worldhappiness_point['GDP per capita']
merged.plot(ax=ax, color="lightgray", edgecolor="grey", linewidth=0.4)
gdf_worldhappiness_point.plot(ax=ax, color="#07424A", markersize=marker, alpha=0.7, categorical=False, legend=True)
plt.axis('equal')
plt.show()
"""

fig = px.scatter_mapbox(gdf_worldhappiness_point.dropna(subset=['GDP per capita']),
                        lat=gdf_worldhappiness_point.geometry.y,
                        lon=gdf_worldhappiness_point.geometry.x,
                        color_continuous_scale=px.colors.cyclical.IceFire,
                        size_max=15,
                        hover_name='country',
                        mapbox_style="carto-darkmatter",
                        zoom=1)
fig.show()
