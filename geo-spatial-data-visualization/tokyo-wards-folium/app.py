import pandas as pd
import folium
import geopandas as gpd
from geopy.geocoders import Nominatim
import webbrowser


def download_process_tokyo_wards_data():
    df = pd.read_html('https://en.wikipedia.org/wiki/Special_wards_of_Tokyo#List_of_special_wards')[3]
    geolocator = Nominatim(user_agent='test_tokyo_wards_data')
    df['city_coord'] = df['Name'].apply(geolocator.geocode).apply(lambda x: (x.latitude, x.longitude))
    df[['Latitude', 'Longitude']] = df['city_coord'].apply(pd.Series)
    df.drop(['Flag', 'city_coord'], axis=1, inplace=True)
    print(df.head())

    df.to_pickle('../data/tokyo_wards.pkl')


def get_tokyo_wards_map(df):
    map_tokyo = folium.Map(location=[35.6828387, 139.7594549], zoom_start=11)
    for lat, lng, label in zip(df['Latitude'], df['Longitude'], df['Name']):
        label = folium.Popup(label, parse_html=True)
        folium.CircleMarker(
            [lat, lng],
            radius=5,
            popup=label,
            color='blue',
            fill=True,
            fill_color='#3186cc',
            fill_opacity=0.2,
            parse_html=False).add_to(map_tokyo)
    return map_tokyo


def get_tokyo_wards_map_cartodb(df):
    #geojson_path = '../data/tokyo13.json'
    geojson_path = '../data/tokyo23.json'
    geojson = gpd.read_file(geojson_path)

    map = folium.Map(location=[36, 140], tiles='cartodbpositron', zoom_start=9)
    folium.Choropleth(geo_data=geojson, name='choropleth').add_to(map)
    return map


if __name__ == '__main__':

    #download_process_tokyo_wards_data()

    df = pd.read_pickle('../data/tokyo_wards.pkl')
    map = get_tokyo_wards_map(df)
    #map = get_tokyo_wards_map_cartodb(df)
    map.save("map.html")
    webbrowser.open("map.html")
