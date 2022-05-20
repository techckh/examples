import geopandas as gpd
import country_converter as coco
import pandas as pd
pd.set_option('display.max_columns', 500)
import plotly.express as px


def convert_country_names_to_codes(df, input_col_name, output_col_name):
    df[output_col_name] = coco.convert(names=list(df[input_col_name]), to='ISO3')


def merge_country_geometry_data(df):
    shapefile = 'data/ne_50m_admin_0_countries.shp'
    gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    gdf.columns = ['country', 'country_code', 'geometry']
    merged = gdf.merge(df, left_on='country_code', right_on='code')
    return merged


gdp_file = 'data/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_4019678.csv'
df_gdp = pd.read_csv(gdp_file)
df_gdp = df_gdp[['Country Name', 'Country Code', '2019']]
df_gdp.columns = ['Country Name', 'code', '2019']

datafile = 'data/2019.csv'
gdf_worldhappiness = pd.read_csv(datafile)
convert_country_names_to_codes(gdf_worldhappiness, 'Country or region', 'code')
merged = merge_country_geometry_data(gdf_worldhappiness)

merged = merged.merge(df_gdp[['code', '2019']], left_on='code', right_on='code')

gdf_worldhappiness_point = merged.copy()
gdf_worldhappiness_point['geometry'] = gdf_worldhappiness_point['geometry'].centroid

df = gdf_worldhappiness_point.dropna(subset=['2019']).copy()
fig = px.scatter_mapbox(df,
                        lat=df.geometry.y,
                        lon=df.geometry.x,
                        color_continuous_scale=px.colors.cyclical.IceFire,
                        size='2019',
                        size_max=15,
                        hover_name='country',
                        mapbox_style="carto-darkmatter",
                        zoom=1)
fig.show()
