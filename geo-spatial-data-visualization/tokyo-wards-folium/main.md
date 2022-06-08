# Map of Tokyo With Yamanote Line Stations


```python
import pandas as pd
```


```python
!pip install folium
```

    Collecting folium
      Downloading folium-0.12.1.post1-py2.py3-none-any.whl (95 kB)
    [2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m95.0/95.0 KB[0m [31m816.8 kB/s[0m eta [36m0:00:00[0m [36m0:00:01[0m
    [?25hCollecting branca>=0.3.0
      Downloading branca-0.5.0-py3-none-any.whl (24 kB)
    Requirement already satisfied: jinja2>=2.9 in /opt/conda/lib/python3.9/site-packages (from folium) (3.1.2)
    Requirement already satisfied: numpy in /opt/conda/lib/python3.9/site-packages (from folium) (1.19.5)
    Requirement already satisfied: requests in /opt/conda/lib/python3.9/site-packages (from folium) (2.27.1)
    Requirement already satisfied: MarkupSafe>=2.0 in /opt/conda/lib/python3.9/site-packages (from jinja2>=2.9->folium) (2.1.1)
    Requirement already satisfied: certifi>=2017.4.17 in /opt/conda/lib/python3.9/site-packages (from requests->folium) (2021.10.8)
    Requirement already satisfied: charset-normalizer~=2.0.0 in /opt/conda/lib/python3.9/site-packages (from requests->folium) (2.0.12)
    Requirement already satisfied: urllib3<1.27,>=1.21.1 in /opt/conda/lib/python3.9/site-packages (from requests->folium) (1.26.9)
    Requirement already satisfied: idna<4,>=2.5 in /opt/conda/lib/python3.9/site-packages (from requests->folium) (3.3)
    Installing collected packages: branca, folium
    Successfully installed branca-0.5.0 folium-0.12.1.post1



```python
import folium
```


```python
def get_tokyo_wards_map_cartodb(df):
    geojson_path = '../data/tokyo23.json'
    geojson = gpd.read_file(geojson_path)
    map = folium.Map(location=[36, 140], tiles='cartodbpositron', zoom_start=9)
    folium.Choropleth(geo_data=geojson, name='choropleth').add_to(map)
    return map
```


```python
def get_tokyo_yamanote_line_map(df):
    map_tokyo = folium.Map(location=[35.6828387, 139.7594549], zoom_start=12)
    for lat, lng, label in zip(df['lat'], df['lon'], df['station']):
        label = folium.Popup(label, parse_html=True)
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
```


```python
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
map   
```




<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;"><span style="color:#565656">Make this Notebook Trusted to load map: File -> Trust Notebook</span><iframe srcdoc="&lt;!DOCTYPE html&gt;
&lt;head&gt;    
    &lt;meta http-equiv=&quot;content-type&quot; content=&quot;text/html; charset=UTF-8&quot; /&gt;

        &lt;script&gt;
            L_NO_TOUCH = false;
            L_DISABLE_3D = false;
        &lt;/script&gt;

    &lt;style&gt;html, body {width: 100%;height: 100%;margin: 0;padding: 0;}&lt;/style&gt;
    &lt;style&gt;#map {position:absolute;top:0;bottom:0;right:0;left:0;}&lt;/style&gt;
    &lt;script src=&quot;https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.js&quot;&gt;&lt;/script&gt;
    &lt;script src=&quot;https://code.jquery.com/jquery-1.12.4.min.js&quot;&gt;&lt;/script&gt;
    &lt;script src=&quot;https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js&quot;&gt;&lt;/script&gt;
    &lt;script src=&quot;https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js&quot;&gt;&lt;/script&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css&quot;/&gt;

            &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width,
                initial-scale=1.0, maximum-scale=1.0, user-scalable=no&quot; /&gt;
            &lt;style&gt;
                #map_19ad840c9a740602c7f757a6d9d71edf {
                    position: relative;
                    width: 100.0%;
                    height: 100.0%;
                    left: 0.0%;
                    top: 0.0%;
                }
            &lt;/style&gt;

&lt;/head&gt;
&lt;body&gt;    

            &lt;div class=&quot;folium-map&quot; id=&quot;map_19ad840c9a740602c7f757a6d9d71edf&quot; &gt;&lt;/div&gt;

&lt;/body&gt;
&lt;script&gt;    

            var map_19ad840c9a740602c7f757a6d9d71edf = L.map(
                &quot;map_19ad840c9a740602c7f757a6d9d71edf&quot;,
                {
                    center: [35.6828387, 139.7594549],
                    crs: L.CRS.EPSG3857,
                    zoom: 12,
                    zoomControl: true,
                    preferCanvas: false,
                }
            );





            var tile_layer_0ff1ee175a0fe69ad1354a69f8e63df9 = L.tileLayer(
                &quot;https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png&quot;,
                {&quot;attribution&quot;: &quot;Data by \u0026copy; \u003ca href=\&quot;http://openstreetmap.org\&quot;\u003eOpenStreetMap\u003c/a\u003e, under \u003ca href=\&quot;http://www.openstreetmap.org/copyright\&quot;\u003eODbL\u003c/a\u003e.&quot;, &quot;detectRetina&quot;: false, &quot;maxNativeZoom&quot;: 18, &quot;maxZoom&quot;: 18, &quot;minZoom&quot;: 0, &quot;noWrap&quot;: false, &quot;opacity&quot;: 1, &quot;subdomains&quot;: &quot;abc&quot;, &quot;tms&quot;: false}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


            var circle_bdcb628bd8b4de5e1444348b377f5861 = L.circle(
                [35.628611, 139.739167],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_b93b955be3fe7f84294f9c8a37c49628 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_9745fffae68ca92a3867dbaec71781a3 = $(`&lt;div id=&quot;html_9745fffae68ca92a3867dbaec71781a3&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Shinagawa&lt;/div&gt;`)[0];
            popup_b93b955be3fe7f84294f9c8a37c49628.setContent(html_9745fffae68ca92a3867dbaec71781a3);


        circle_bdcb628bd8b4de5e1444348b377f5861.bindPopup(popup_b93b955be3fe7f84294f9c8a37c49628)
        ;




            var circle_d7eded6c9b2ec79c3edf34c15ef9bcc0 = L.circle(
                [35.6197, 139.72855],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_379cb3ea624bcea20c6f6c97b491e1b2 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_ac4bdafe0fad1c92fdd7f937e4b590ed = $(`&lt;div id=&quot;html_ac4bdafe0fad1c92fdd7f937e4b590ed&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Ōsaki&lt;/div&gt;`)[0];
            popup_379cb3ea624bcea20c6f6c97b491e1b2.setContent(html_ac4bdafe0fad1c92fdd7f937e4b590ed);


        circle_d7eded6c9b2ec79c3edf34c15ef9bcc0.bindPopup(popup_379cb3ea624bcea20c6f6c97b491e1b2)
        ;




            var circle_5b2b64cad64f8e377a77591915de949d = L.circle(
                [35.62645, 139.7234],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_b75a20c982d47728f2e91fd9ad1972ac = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_2a0aaa1bb0504f99dc4c4303517cba03 = $(`&lt;div id=&quot;html_2a0aaa1bb0504f99dc4c4303517cba03&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Gotanda&lt;/div&gt;`)[0];
            popup_b75a20c982d47728f2e91fd9ad1972ac.setContent(html_2a0aaa1bb0504f99dc4c4303517cba03);


        circle_5b2b64cad64f8e377a77591915de949d.bindPopup(popup_b75a20c982d47728f2e91fd9ad1972ac)
        ;




            var circle_58b9916f7991ec3fc454011c992fad56 = L.circle(
                [35.633983, 139.716],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_b679059758e8334c5ef2071ee161316d = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_68544323544f37157ed2bec9d855c6da = $(`&lt;div id=&quot;html_68544323544f37157ed2bec9d855c6da&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Meguro&lt;/div&gt;`)[0];
            popup_b679059758e8334c5ef2071ee161316d.setContent(html_68544323544f37157ed2bec9d855c6da);


        circle_58b9916f7991ec3fc454011c992fad56.bindPopup(popup_b679059758e8334c5ef2071ee161316d)
        ;




            var circle_b521482df59afa116a314bc52c435c74 = L.circle(
                [35.646643, 139.710045],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_0c22d725dd84fb52e3dce0c25324c442 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_78d716ae43a5f311c22326acf85d5bff = $(`&lt;div id=&quot;html_78d716ae43a5f311c22326acf85d5bff&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Ebisu&lt;/div&gt;`)[0];
            popup_0c22d725dd84fb52e3dce0c25324c442.setContent(html_78d716ae43a5f311c22326acf85d5bff);


        circle_b521482df59afa116a314bc52c435c74.bindPopup(popup_0c22d725dd84fb52e3dce0c25324c442)
        ;




            var circle_39c44dd8a554d71834a71aefea26dadd = L.circle(
                [35.658514, 139.70133],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_9f8ea79c2690364c172ad87f4bdc0259 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_654e4c2652f5036db9e16a5bffcde0c2 = $(`&lt;div id=&quot;html_654e4c2652f5036db9e16a5bffcde0c2&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Shibuya&lt;/div&gt;`)[0];
            popup_9f8ea79c2690364c172ad87f4bdc0259.setContent(html_654e4c2652f5036db9e16a5bffcde0c2);


        circle_39c44dd8a554d71834a71aefea26dadd.bindPopup(popup_9f8ea79c2690364c172ad87f4bdc0259)
        ;




            var circle_6510e81ab133840c9dd139a9b2500942 = L.circle(
                [35.66883333333333, 139.70166666666665],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_391594f6ec71f98da72d1a3d62a95554 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_26316b5039a4c756a9c9381f5b8a188f = $(`&lt;div id=&quot;html_26316b5039a4c756a9c9381f5b8a188f&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Harajuku&lt;/div&gt;`)[0];
            popup_391594f6ec71f98da72d1a3d62a95554.setContent(html_26316b5039a4c756a9c9381f5b8a188f);


        circle_6510e81ab133840c9dd139a9b2500942.bindPopup(popup_391594f6ec71f98da72d1a3d62a95554)
        ;




            var circle_aecadb1e4e793c55309e06ed958d2c5e = L.circle(
                [35.683828, 139.70232],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_24365ce6b1e674734f7c421e28119ea8 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_12e27a2b79542e14d5702ff708a4d90c = $(`&lt;div id=&quot;html_12e27a2b79542e14d5702ff708a4d90c&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Yoyogi&lt;/div&gt;`)[0];
            popup_24365ce6b1e674734f7c421e28119ea8.setContent(html_12e27a2b79542e14d5702ff708a4d90c);


        circle_aecadb1e4e793c55309e06ed958d2c5e.bindPopup(popup_24365ce6b1e674734f7c421e28119ea8)
        ;




            var circle_659838d0e08dda22961c2f99412d2855 = L.circle(
                [35.689475, 139.700349],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_028e5cf33cb0386003ce948320b02e82 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_e2ae0e04f5cd493991124e7b4bfcd74a = $(`&lt;div id=&quot;html_e2ae0e04f5cd493991124e7b4bfcd74a&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Shinjuku&lt;/div&gt;`)[0];
            popup_028e5cf33cb0386003ce948320b02e82.setContent(html_e2ae0e04f5cd493991124e7b4bfcd74a);


        circle_659838d0e08dda22961c2f99412d2855.bindPopup(popup_028e5cf33cb0386003ce948320b02e82)
        ;




            var circle_60518ad71d689929de860a759ddf17b5 = L.circle(
                [35.701063, 139.700228],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_1f95c59ced5b1f5ac12045851ac1a758 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_7643e45684fbde7a8902d093051f56a6 = $(`&lt;div id=&quot;html_7643e45684fbde7a8902d093051f56a6&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Shin-Ōkubo&lt;/div&gt;`)[0];
            popup_1f95c59ced5b1f5ac12045851ac1a758.setContent(html_7643e45684fbde7a8902d093051f56a6);


        circle_60518ad71d689929de860a759ddf17b5.bindPopup(popup_1f95c59ced5b1f5ac12045851ac1a758)
        ;




            var circle_0a4b4fa5e00476dd75e4cea66b8055ab = L.circle(
                [35.70766666666667, 139.70233333333334],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_b4fa30a3889dc61202e3e21f1f7281f6 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_144d24a43c788b0af3dd9a8f7ce7a4e6 = $(`&lt;div id=&quot;html_144d24a43c788b0af3dd9a8f7ce7a4e6&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Takadanobaba&lt;/div&gt;`)[0];
            popup_b4fa30a3889dc61202e3e21f1f7281f6.setContent(html_144d24a43c788b0af3dd9a8f7ce7a4e6);


        circle_0a4b4fa5e00476dd75e4cea66b8055ab.bindPopup(popup_b4fa30a3889dc61202e3e21f1f7281f6)
        ;




            var circle_07eda856fbf00a023e304eacd1637c31 = L.circle(
                [35.720995, 139.70688],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_b02d16b341d11f864d7d478659ad7e3c = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_a09fd84dd47fb51629cc4aad30796bbd = $(`&lt;div id=&quot;html_a09fd84dd47fb51629cc4aad30796bbd&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Mejiro&lt;/div&gt;`)[0];
            popup_b02d16b341d11f864d7d478659ad7e3c.setContent(html_a09fd84dd47fb51629cc4aad30796bbd);


        circle_07eda856fbf00a023e304eacd1637c31.bindPopup(popup_b02d16b341d11f864d7d478659ad7e3c)
        ;




            var circle_fb1386c94022ab37487bf74b782b824d = L.circle(
                [35.724833333333336, 139.70683333333332],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_a635a4093ba733d14fc638d371b2c32a = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_27a6130dc1a6878b42cf0cbcaeb5fb60 = $(`&lt;div id=&quot;html_27a6130dc1a6878b42cf0cbcaeb5fb60&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Ikebukuro&lt;/div&gt;`)[0];
            popup_a635a4093ba733d14fc638d371b2c32a.setContent(html_27a6130dc1a6878b42cf0cbcaeb5fb60);


        circle_fb1386c94022ab37487bf74b782b824d.bindPopup(popup_a635a4093ba733d14fc638d371b2c32a)
        ;




            var circle_af660c5106998844ae534c8825220d62 = L.circle(
                [35.731438, 139.728692],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_a1ae96b22c75c8c6d46f70beed116d90 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_ba329baf2700736f03889311bc93d013 = $(`&lt;div id=&quot;html_ba329baf2700736f03889311bc93d013&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Ōtsuka&lt;/div&gt;`)[0];
            popup_a1ae96b22c75c8c6d46f70beed116d90.setContent(html_ba329baf2700736f03889311bc93d013);


        circle_af660c5106998844ae534c8825220d62.bindPopup(popup_a1ae96b22c75c8c6d46f70beed116d90)
        ;




            var circle_455cef61969d56782480a2ad60a6e4ec = L.circle(
                [35.733345, 139.739496],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_776055000cd47f5894e29326cd78d1ea = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_ac14f6327280c852af0cb635ebd70a1a = $(`&lt;div id=&quot;html_ac14f6327280c852af0cb635ebd70a1a&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Sugamo&lt;/div&gt;`)[0];
            popup_776055000cd47f5894e29326cd78d1ea.setContent(html_ac14f6327280c852af0cb635ebd70a1a);


        circle_455cef61969d56782480a2ad60a6e4ec.bindPopup(popup_776055000cd47f5894e29326cd78d1ea)
        ;




            var circle_28882f2fd828e7b2e5b3479548467038 = L.circle(
                [35.736289, 139.746995],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_25a490030c8aeecdd42ff22adcb90bc9 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_67531601fc9918d00a1119911323ff8d = $(`&lt;div id=&quot;html_67531601fc9918d00a1119911323ff8d&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Komagome&lt;/div&gt;`)[0];
            popup_25a490030c8aeecdd42ff22adcb90bc9.setContent(html_67531601fc9918d00a1119911323ff8d);


        circle_28882f2fd828e7b2e5b3479548467038.bindPopup(popup_25a490030c8aeecdd42ff22adcb90bc9)
        ;




            var circle_445b7c209e2b6898d2c719581bd65b0f = L.circle(
                [35.737909, 139.761254],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_005c40f5edf26e7d0da0986db6736cb0 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_01682555860e1ce6266b018aea482862 = $(`&lt;div id=&quot;html_01682555860e1ce6266b018aea482862&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Tabata&lt;/div&gt;`)[0];
            popup_005c40f5edf26e7d0da0986db6736cb0.setContent(html_01682555860e1ce6266b018aea482862);


        circle_445b7c209e2b6898d2c719581bd65b0f.bindPopup(popup_005c40f5edf26e7d0da0986db6736cb0)
        ;




            var circle_b8cec00646838e45817ac2a2a896111f = L.circle(
                [35.731926, 139.7668],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_932b3435a80a1f575e71f66f33b7a73d = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_3812473c7adc091dfcd17e3ce2b9dc6d = $(`&lt;div id=&quot;html_3812473c7adc091dfcd17e3ce2b9dc6d&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Nishi-Nippori&lt;/div&gt;`)[0];
            popup_932b3435a80a1f575e71f66f33b7a73d.setContent(html_3812473c7adc091dfcd17e3ce2b9dc6d);


        circle_b8cec00646838e45817ac2a2a896111f.bindPopup(popup_932b3435a80a1f575e71f66f33b7a73d)
        ;




            var circle_778116c91a34c61ff508f6bdf7ef0866 = L.circle(
                [35.727588, 139.770781],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_1cf75f4fe1e681afe0a549420921898f = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_c5308822542ba661e53f800405b51c4a = $(`&lt;div id=&quot;html_c5308822542ba661e53f800405b51c4a&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Nippori&lt;/div&gt;`)[0];
            popup_1cf75f4fe1e681afe0a549420921898f.setContent(html_c5308822542ba661e53f800405b51c4a);


        circle_778116c91a34c61ff508f6bdf7ef0866.bindPopup(popup_1cf75f4fe1e681afe0a549420921898f)
        ;




            var circle_88efc7686814947a6fa240bf98561ec6 = L.circle(
                [35.722066, 139.777851],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_d89a88208d94bd4623ebad3a9ee9753d = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_02a195c401a6a57b3a36aebeb50d4b6b = $(`&lt;div id=&quot;html_02a195c401a6a57b3a36aebeb50d4b6b&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Uguisudani&lt;/div&gt;`)[0];
            popup_d89a88208d94bd4623ebad3a9ee9753d.setContent(html_02a195c401a6a57b3a36aebeb50d4b6b);


        circle_88efc7686814947a6fa240bf98561ec6.bindPopup(popup_d89a88208d94bd4623ebad3a9ee9753d)
        ;




            var circle_aac11126c7cbfa1f009f81f66894c8a7 = L.circle(
                [35.713434, 139.776725],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_e191f94625ae59808f6227646abab510 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_37ca123414b88086a915569a26939795 = $(`&lt;div id=&quot;html_37ca123414b88086a915569a26939795&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Ueno&lt;/div&gt;`)[0];
            popup_e191f94625ae59808f6227646abab510.setContent(html_37ca123414b88086a915569a26939795);


        circle_aac11126c7cbfa1f009f81f66894c8a7.bindPopup(popup_e191f94625ae59808f6227646abab510)
        ;




            var circle_afbd27d236c4ba441c90f58131b4bd89 = L.circle(
                [35.707327, 139.774847],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_3c31acbd6dc65bf1996355a2b51f12eb = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_3b4952ceb497330c6a55fec5a74288c3 = $(`&lt;div id=&quot;html_3b4952ceb497330c6a55fec5a74288c3&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Okachimachi&lt;/div&gt;`)[0];
            popup_3c31acbd6dc65bf1996355a2b51f12eb.setContent(html_3b4952ceb497330c6a55fec5a74288c3);


        circle_afbd27d236c4ba441c90f58131b4bd89.bindPopup(popup_3c31acbd6dc65bf1996355a2b51f12eb)
        ;




            var circle_125dea983c3e24fac0cc3c5189503cbf = L.circle(
                [35.69233333333333, 139.7705],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_ccd74f0d80ea14f2b0e875c943c8d278 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_2f54e9999b02b128384c7a9d017d6fc7 = $(`&lt;div id=&quot;html_2f54e9999b02b128384c7a9d017d6fc7&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Akihabara&lt;/div&gt;`)[0];
            popup_ccd74f0d80ea14f2b0e875c943c8d278.setContent(html_2f54e9999b02b128384c7a9d017d6fc7);


        circle_125dea983c3e24fac0cc3c5189503cbf.bindPopup(popup_ccd74f0d80ea14f2b0e875c943c8d278)
        ;




            var circle_ceda82474108c559e111948903a82a63 = L.circle(
                [35.691731, 139.771264],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_7ccd26c0b5a0304940fb2e51fac0c1f7 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_d20dbbd34a9c1d7c98c599ab1e75073a = $(`&lt;div id=&quot;html_d20dbbd34a9c1d7c98c599ab1e75073a&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Kanda&lt;/div&gt;`)[0];
            popup_7ccd26c0b5a0304940fb2e51fac0c1f7.setContent(html_d20dbbd34a9c1d7c98c599ab1e75073a);


        circle_ceda82474108c559e111948903a82a63.bindPopup(popup_7ccd26c0b5a0304940fb2e51fac0c1f7)
        ;




            var circle_f09d792f696a562e9ef6a46d89ca280e = L.circle(
                [35.67516666666667, 139.76683333333332],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_34f2811b00c944b5731926b221657218 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_4b7dae05d3d6790532fe642a2c21bb3c = $(`&lt;div id=&quot;html_4b7dae05d3d6790532fe642a2c21bb3c&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Tokyo&lt;/div&gt;`)[0];
            popup_34f2811b00c944b5731926b221657218.setContent(html_4b7dae05d3d6790532fe642a2c21bb3c);


        circle_f09d792f696a562e9ef6a46d89ca280e.bindPopup(popup_34f2811b00c944b5731926b221657218)
        ;




            var circle_d522ebadf5856542beb3137bec329122 = L.circle(
                [35.674877, 139.763646],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_0272aff38e517646e68fe3031137fed8 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_697bf08e5983aabb2de8724981868766 = $(`&lt;div id=&quot;html_697bf08e5983aabb2de8724981868766&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Yūrakuchō&lt;/div&gt;`)[0];
            popup_0272aff38e517646e68fe3031137fed8.setContent(html_697bf08e5983aabb2de8724981868766);


        circle_d522ebadf5856542beb3137bec329122.bindPopup(popup_0272aff38e517646e68fe3031137fed8)
        ;




            var circle_1437ee0ddf620b97af6b7a09291c234c = L.circle(
                [35.666301, 139.758679],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_b32c585519259f6d708fc2986bcfcf07 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_3e14c2875bfee33c6ad73b3985e9e18a = $(`&lt;div id=&quot;html_3e14c2875bfee33c6ad73b3985e9e18a&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Shimbashi&lt;/div&gt;`)[0];
            popup_b32c585519259f6d708fc2986bcfcf07.setContent(html_3e14c2875bfee33c6ad73b3985e9e18a);


        circle_1437ee0ddf620b97af6b7a09291c234c.bindPopup(popup_b32c585519259f6d708fc2986bcfcf07)
        ;




            var circle_21fcceaa05d9ae2a950fb066705b808d = L.circle(
                [35.65523, 139.757627],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_84ab17504c39226b59c894fe2c270e80 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_46f7bdfa3380b1f1b6ea0a171a6b1e13 = $(`&lt;div id=&quot;html_46f7bdfa3380b1f1b6ea0a171a6b1e13&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Hamamatsuchō&lt;/div&gt;`)[0];
            popup_84ab17504c39226b59c894fe2c270e80.setContent(html_46f7bdfa3380b1f1b6ea0a171a6b1e13);


        circle_21fcceaa05d9ae2a950fb066705b808d.bindPopup(popup_84ab17504c39226b59c894fe2c270e80)
        ;




            var circle_51cb58cb3fa5085bdad893dd3b3601c2 = L.circle(
                [35.645605, 139.7477],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_ef54eaebb48ef7db6c09af2892c19e76 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_f4a0925f9561aa491621135832c7a15b = $(`&lt;div id=&quot;html_f4a0925f9561aa491621135832c7a15b&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Tamachi&lt;/div&gt;`)[0];
            popup_ef54eaebb48ef7db6c09af2892c19e76.setContent(html_f4a0925f9561aa491621135832c7a15b);


        circle_51cb58cb3fa5085bdad893dd3b3601c2.bindPopup(popup_ef54eaebb48ef7db6c09af2892c19e76)
        ;




            var circle_3b2610e4e25b3da687c6cb58919ac838 = L.circle(
                [35.636389, 139.741389],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;blue&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3186cc&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 700, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_19ad840c9a740602c7f757a6d9d71edf);


        var popup_78c8aa9235ac8c7a7a2d0ed9e64ec6e4 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});


            var html_5d1cba0f176836185786f6ebdf99791c = $(`&lt;div id=&quot;html_5d1cba0f176836185786f6ebdf99791c&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Takanawa Gateway&lt;/div&gt;`)[0];
            popup_78c8aa9235ac8c7a7a2d0ed9e64ec6e4.setContent(html_5d1cba0f176836185786f6ebdf99791c);


        circle_3b2610e4e25b3da687c6cb58919ac838.bindPopup(popup_78c8aa9235ac8c7a7a2d0ed9e64ec6e4)
        ;



&lt;/script&gt;" style="position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>




```python

```
