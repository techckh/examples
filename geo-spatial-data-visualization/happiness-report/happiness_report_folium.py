import geopandas as gpd
import country_converter as coco
import pandas as pd
import json
import folium


shapefile = 'data/ne_50m_admin_0_countries.shp'
gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
gdf.columns = ['country', 'country_code', 'geometry']

datafile = 'data/2019.csv'
df = pd.read_csv(datafile)
df['code'] = coco.convert(names=list(df['Country or region']), to='ISO3')

merged = gdf.merge(df, left_on='country_code', right_on='code')
merged.head()
merged_json = json.loads(merged.to_json())
json_data = json.dumps(merged_json)

m = folium.Map(location=[48, -102], zoom_start=3)
list_of_index = ['Score',
                 'GDP per capita',
                 'Social support',
                 'Healthy life expectancy',
                 'Freedom to make life choices',
                 'Generosity',
                 'Perceptions of corruption']
for x in list_of_index:
    folium.Choropleth(
        geo_data=json_data,
        name=x,
        data=merged,
        columns=['Country or region', x],
        key_on='feature.properties.Country or region',
        fill_color='RdBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=x).add_to(m)
folium.LayerControl(collapsed=False).add_to(m)
m.save('folium_map.html')
