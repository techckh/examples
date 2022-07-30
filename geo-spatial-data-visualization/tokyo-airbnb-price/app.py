import pandas as pd
import geopandas as gpd
import folium
import webbrowser


def convert_wards_data():
    df = pd.read_pickle('../data/tokyo_wards.pkl')
    df['code'] = df['No.'].apply(lambda x: '131%s' % x)
    df['Name'] = df['Name'].apply(lambda x: '%s Ku' % x)
    df[['code', 'Name', 'Kanji']].to_csv('../data/tokyo_ward_codes.csv', index=False)
    print(df.head())


def add_code(d, key, val):
    d[key] = val


def create_map(df):
    geojson_path = '../data/tokyo23.json'
    geojson = gpd.read_file(geojson_path)

    bins = list(df["price"].quantile([0, 0.25, 0.5, 0.75, 1]))
    map = folium.Map(location=[36, 140], tiles='cartodbpositron', zoom_start=9)
    folium.Choropleth(geo_data=geojson,
                      name='choropleth',
                      data=df,
                      columns=['geo_json_code', 'price'],
                      key_on='feature.properties.N03_007',
                      fill_opacity=0.7,
                      line_opacity=0.2,
                      line_color='red',
                      legend_name="Tokyo Airbnb Prices",
                      fill_color='YlGn').add_to(map)
    folium.LayerControl().add_to(map)
    return map


if __name__ == '__main__':

    #convert_wards_data()

    df = pd.read_csv('../data/tokyo_ward_codes.csv')
    code_table = dict()
    df.apply(lambda x: add_code(code_table, x.Name, x.Code), axis=1)
    print(code_table)
    assert len(code_table) == 23, 'error count'

    df = pd.read_csv('../data/airbnb/neighbourhoods.csv')
    print(df.head())

    df = df[df['neighbourhood'].isin([*code_table])]
    df['geo_json_code'] = df['neighbourhood'].apply(lambda x: code_table[x])
    df['geo_json_code'] = df['geo_json_code'].astype('str')

    tmp = pd.read_csv('../data/airbnb/listings_summary.csv')
    df_listings = tmp[['id', 'name', 'neighbourhood', 'latitude', 'longitude', 'price']]
    df_listings = df_listings.merge(df, on=['neighbourhood'])

    map = create_map(df_listings)
    map.save("map_tokyo_airbnb_prices.html")
    webbrowser.open("map_tokyo_airbnb_prices.html")
    print('done')
