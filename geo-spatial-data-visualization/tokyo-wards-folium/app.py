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


def get_tokyo_yamanote_line_map(df):
    map_tokyo = folium.Map(location=[35.6828387, 139.7594549], zoom_start=11)
    for lat, lng, label in zip(df['lat'], df['lon'], df['station']):
        label = folium.Popup(label, parse_html=True)
        """
        folium.CircleMarker(
            [lat, lng],
            radius=5,
            popup=label,
            color='blue',
            fill=True,
            fill_color='#3186cc',
            fill_opacity=0.2,
            parse_html=False).add_to(map_tokyo)
        """

        folium.Circle(
            [lat, lng],
            radius=700,
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

    """
    df = pd.read_pickle('../data/tokyo_wards.pkl')
    map = get_tokyo_wards_map(df)
    #map = get_tokyo_wards_map_cartodb(df)
    map.save("map.html")
    webbrowser.open("map.html")
    """

    df = pd.read_pickle('../data/tokyo_yamanote_line.pkl')
    # corrections
    # TODO: tokyo akihabara
    df.loc[df.station == 'Shinagawa', 'lat'] = 35.628611
    df.loc[df.station == 'Shinagawa', 'lon'] = 139.739167
    df.loc[df.station == 'Ebisu', 'lat'] = 35.646643
    df.loc[df.station == 'Ebisu', 'lon'] = 139.710045
    df.loc[df.station == 'Shibuya', 'lat'] = 35.658514
    df.loc[df.station == 'Shibuya', 'lon'] = 139.70133
    df.loc[df.station == 'Gotanda', 'lat'] = 35.62645
    df.loc[df.station == 'Gotanda', 'lon'] = 139.7234
    df.loc[df.station == 'Meguro', 'lat'] = 35.633983
    df.loc[df.station == 'Meguro', 'lon'] = 139.716
    map = get_tokyo_yamanote_line_map(df)
    map.save("map_yamanote.html")
    webbrowser.open("map_yamanote.html")
