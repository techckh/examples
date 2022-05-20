import gmplot


place_name = 'meguro'
apikey = ''

lat = 35.633983
lon = 139.716

gmap = gmplot.GoogleMapPlotter(lat, lon, 14, apikey=apikey)
attractions_lats, attractions_lngs = zip(*[(lat, lon)])
gmap.scatter(attractions_lats, attractions_lngs, color='#a8dfff', size=40, marker=False)
gmap.circle(lat, lon, 800, face_alpha=0.05, edge_color='#a8dfff', fc='b')


gmap.draw('{}_map.html'.format(place_name))
